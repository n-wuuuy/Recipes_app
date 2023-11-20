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
