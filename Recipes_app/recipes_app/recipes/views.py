from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from recipes.models import Category, Product
from recipes.serializers import CategorySerializer, ProductSerializer


# Create your views here.

class CategoryModelView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)


class ProductModelView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
