from django.urls import path
from rest_framework.routers import SimpleRouter

from recipes.views import CategoryModelView, ProductListModelView

router = SimpleRouter()
router.register('api/v1/category', CategoryModelView)
router.register('api/v1/product', ProductListModelView)

urlpatterns = [
]

urlpatterns += router.urls
