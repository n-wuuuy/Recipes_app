from datetime import datetime
import json

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Count
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from recipes.models import Category, Product, CookingSteps, Recipe
from recipes.serializers import CategorySerializer, ProductSerializer, CookingStepsSerializer, RecipeListSerializer, \
    RecipeDitailSerializer


class CategoryApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username', is_staff=True)
        self.user2 = User.objects.create(username='test_username2')
        self.category1 = Category.objects.create(name='Soup')
        self.category2 = Category.objects.create(name='Meat')

    def test_get(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.client.force_login(self.user)
        categories = Category.objects.all()
        serializer_data = CategorySerializer(categories, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        url = reverse('category-list')
        data = {
            'name': 'Vegetables'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Category.objects.all().count())

    def test_update(self):
        url = reverse('category-detail', args=(self.category1.id,))
        data = {
            "name": 'Fish',
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data,
                                   content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.category1.refresh_from_db()
        self.assertEqual('Fish', self.category1.name)

    def test_delete(self):
        self.assertEqual(2, Category.objects.all().count())
        url = reverse('category-detail', args=(self.category1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url, data={'id': self.category1.id})
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Category.objects.all().count())

    def test_update_not_staff(self):
        url = reverse('category-detail', args=(self.category1.id,))
        data = {
            "name": 'Fish',
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data,
                                   content_type="application/json")
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this '
                                                                      'action.',
                                                               code='permission_denied')})
        self.category1.refresh_from_db()
        self.assertNotEquals('Fish', self.category1.name)

    def test_delete_not_admin(self):
        self.assertEqual(2, Category.objects.all().count())
        url = reverse('category-detail', args=(self.category1.id,))
        self.client.force_login(self.user2)
        response = self.client.delete(url, data={'id': self.category1.id})
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(2, Category.objects.all().count())


class ProductApiTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_username', is_staff=True)
        self.user2 = User.objects.create(username='test_username2', is_staff=False)
        self.user3 = User.objects.create(username='test_username3', is_staff=False)
        self.product1 = Product.objects.create(name='Cucumber', weight=500, owner=self.user2)
        self.product2 = Product.objects.create(name='Pumpkin', weight=250, owner=self.user2)

    def test_get(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.client.force_login(self.user3)
        products = Product.objects.all()
        serializer_data = ProductSerializer(products, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        url = reverse('product-list')
        data = {
            'name': 'Cabbage',
            'weight': 350,
            'owner': self.user2.id
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.post(url, data=json_data,
                                    content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Product.objects.all().count())

    def test_update(self):
        url = reverse('product-detail', args=(self.product1.id,))
        data = {
            'name': 'Cucumber',
            'weight': 350,
            'owner': self.user2.id
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data,
                                   content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.product1.refresh_from_db()
        self.assertEqual(350, self.product1.weight)

    def test_delete(self):
        self.assertEqual(2, Product.objects.all().count())
        url = reverse('product-detail', args=(self.product1.id,))
        self.client.force_login(self.user2)
        response = self.client.delete(url, data={'id': self.product1.id})
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Product.objects.all().count())

    def test_update_not_staff(self):
        url = reverse('product-detail', args=(self.product1.id,))
        data = {
            'name': 'Fish',
            'weight': 350,
            'owner': self.user2.id
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user3)
        response = self.client.put(url, data=json_data,
                                   content_type="application/json")
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this '
                                                                      'action.',
                                                               code='permission_denied')})
        self.product1.refresh_from_db()
        self.assertNotEquals('Fish', self.product1.name)

    def test_delete_not_staff(self):
        self.assertEqual(2, Product.objects.all().count())
        url = reverse('product-detail', args=(self.product1.id,))
        self.client.force_login(self.user3)
        response = self.client.delete(url, data={'id': self.product1.id})
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(2, Product.objects.all().count())

