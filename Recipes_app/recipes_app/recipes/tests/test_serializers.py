from django.test import TestCase

from recipes.models import Category, Product
from recipes.serializers import CategorySerializer, ProductSerializer


class CategorySerializerTestCase(TestCase):
    def test_serializer(self):
        category1 = Category.objects.create(name='Soup')
        category2 = Category.objects.create(name='Meat')
        categories_obj = Category.objects.all()
        data = CategorySerializer(categories_obj, many=True).data
        exected_data = [
            {
                'id': category1.id,
                'name': 'Soup'
            },
            {
                'id': category2.id,
                'name': 'Meat'
            }
        ]
        self.assertEqual(exected_data, data)
