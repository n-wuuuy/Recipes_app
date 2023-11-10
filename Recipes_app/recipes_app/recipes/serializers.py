from rest_framework import serializers

from recipes.models import Category, Product, Recipe, CookingSteps


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
