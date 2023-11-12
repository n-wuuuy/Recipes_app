from django.urls import path
from rest_framework.routers import SimpleRouter

from recipes.views import CategoryModelView, ProductModelView

router = SimpleRouter()
router.register('api/v1/category', CategoryModelView)

urlpatterns = [
    path('api/v1/product', ProductModelView.as_view())
]

urlpatterns += router.urls
