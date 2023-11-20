import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from recipes.models import Category
from recipes.serializers import CategorySerializer


class CategoryApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username', is_staff=True)
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
        self.user2 = User.objects.create(username='test_username2')
        url = reverse('category-detail', args=(self.category1.id, ))
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
