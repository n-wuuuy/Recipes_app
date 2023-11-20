from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from recipes.models import Category, Product, CookingSteps, Recipe
from recipes.permissions import IsOwnerOrStaffOrReadOnly, IsAdminOrReadOnly
from recipes.serializers import CategorySerializer, ProductSerializer, CookingStepsSerializer, RecipeListSerializer, \
    RecipeDitailSerializer


# Create your views here.

class CategoryModelView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductModelView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]


class CookingStepsModelView(ModelViewSet):
    queryset = CookingSteps.objects.all()
    serializer_class = CookingStepsSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]


class RecipeModelView(ModelViewSet):
    queryset = Recipe.objects.all().annotate(product_count=Count('products')
                                             ).select_related('category').prefetch_related('steps',
                                                                                           'products')
    permission_classes = [IsOwnerOrStaffOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeListSerializer
        else:
            return RecipeDitailSerializer
