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


class ProductSerializerTestCase(TestCase):
    def test_serializer(self):
        product1 = Product.objects.create(name='Cucumber', weight=250)
        product2 = Product.objects.create(name='Patato', weight=500)
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        exected_data = [
            {
                'id': product1.id,
                'name': 'Cucumber',
                'weight': 250
            },
            {
                'id': product2.id,
                'name': 'Patato',
                'weight': 500
            }
        ]
        self.assertEqual(exected_data, data)
