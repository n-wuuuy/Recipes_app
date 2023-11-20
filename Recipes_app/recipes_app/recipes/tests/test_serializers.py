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


class RecipeSerializerTestCase(TestCase):
    def test_ditail_serializer(self):
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
        recipe1.products.add(product1, product2)
        step = CookingSteps.objects.create(title='Cooking soup',
                                           instruction='120',
                                           picture='',
                                           recipe=recipe1)
        recipe1.save()
        recipe = Recipe.objects.all().annotate(product_count=Count('products')
                                               ).select_related('category').prefetch_related('steps',
                                                                                             'products').order_by('id')
        data = RecipeDitailSerializer(recipe, many=True).data
        exected_data = [
            {
                "id": recipe1.id,
                "category": "Soup",
                "steps": [
                    {
                        "id": step.id,
                        "title": "Cooking soup",
                        "instruction": "120",
                        "picture": None,
                        "recipe": recipe1.id
                    },
                ],
                "products": [
                    'Cucumber-250',
                    'Patato-450'
                ],
                "title": "broth",
                "description": "tasty soup",
                "picture": None,
                "cooking_time": "00:30:00",
                "time_create": datetime.strftime(recipe1.time_create, '%Y-%m-%dT%H:%M:%S.%fZ'),
                "portion": 2,
                "video": "https://www.youtube.com/watch?v=Z2NHP2NQD4k",
                "owner": user1.id
            },
        ]
        self.assertEqual(exected_data, data)

    def test_list_serializer(self):
        user1 = User.objects.create(username='user1',
                                    first_name='Ivan',
                                    last_name='Danilevich')
        product1 = Product.objects.create(name='Cucumber', weight=250)
        product2 = Product.objects.create(name='Patato', weight=450)
        product3 = Product.objects.create(name='Meat', weight=150)
        category1 = Category.objects.create(name='Salad')
        category2 = Category.objects.create(name='Meat')
        recipe1 = Recipe.objects.create(title='Salad',
                                        description='tasty salad',
                                        picture='',
                                        cooking_time='00:30:00',
                                        time_create=datetime.now(),
                                        category=category1,
                                        owner=user1,
                                        portion=5,
                                        video='https://www.youtube.com/watch?v=Z2NHP2NQD4k')
        recipe2 = Recipe.objects.create(title='Meat',
                                        description='tasty meat',
                                        picture='',
                                        cooking_time='01:13:00',
                                        category=category2,
                                        owner=user1,
                                        portion=2)
        recipe1.products.add(product1, product2)
        recipe2.products.add(product1, product2, product3)
        recipes = Recipe.objects.all().annotate(product_count=Count('products')
                                                ).select_related('category').prefetch_related('steps',
                                                                                              'products').order_by('id')
        data = RecipeListSerializer(recipes, many=True).data
        exected_data = [
            {
                "title": "Salad",
                "picture": None,
                "cooking_time": '00:30:00',
                "portion": 5,
                "category": "Salad",
                "product_count": 2
            },
            {
                "title": "Meat",
                "picture": None,
                "cooking_time": '01:13:00',
                "portion": 2,
                "category": "Meat",
                "product_count": 3
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
