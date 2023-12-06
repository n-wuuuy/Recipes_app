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


class RecipeListSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField()
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('title', 'picture', 'cooking_time', 'portion', 'category', 'product_count')


class CookingStepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingSteps
        fields = '__all__'


class RecipeDitailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    steps = CookingStepsSerializer(many=True)
    products = ProductSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'
