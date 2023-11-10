from rest_framework import serializers

from recipes.models import Category, Product, Recipe, CookingSteps


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class CookingStepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingSteps
        fields = '__all__'
