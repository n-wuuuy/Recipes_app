from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Count
from django.test import TestCase

from recipes.models import Category, Product, CookingSteps, Recipe
from recipes.serializers import CategorySerializer, ProductSerializer, CookingStepsSerializer, RecipeDitailSerializer, \
    RecipeListSerializer


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


class CookingStepsSerializerTestCase(TestCase):
    def test_serializer(self):
        user1 = User.objects.create(username='user1',
                                    first_name='Ivan',
                                    last_name='Danilevich')
        product1 = Product.objects.create(name='Cucumber', weight=250)
        product2 = Product.objects.create(name='Patato', weight=450)
        category1 = Category.objects.create(name='Soup')
        recipe1 = Recipe.objects.create(title='broth',
                                        description='tasty soup',
                                        picture='',
                                        cooking_time='00:30:00',
                                        time_create=datetime.now(),
                                        category=category1,
                                        owner=user1,
                                        portion=2,
                                        video='https://www.youtube.com/watch?v=Z2NHP2NQD4k')
        recipe1.save()
        recipe1.products.add(product1, product2)
        step1 = CookingSteps.objects.create(title='Cooking soup',
                                            instruction='120',
                                            picture='',
                                            recipe=recipe1)
        step2 = CookingSteps.objects.create(title='Wait',
                                            instruction='Wait about 1:00:00',
                                            picture='',
                                            recipe=recipe1)
        steps = CookingSteps.objects.all()
        data = CookingStepsSerializer(steps, many=True).data
        exected_data = [
            {
                'id': step1.id,
                'title': 'Cooking soup',
                'instruction': '120',
                'picture': None,
                'recipe': recipe1.id
            },
            {
                'id': step2.id,
                'title': 'Wait',
                'instruction': 'Wait about 1:00:00',
                'picture': None,
                'recipe': recipe1.id
            }
        ]
        self.assertEqual(exected_data, data)
