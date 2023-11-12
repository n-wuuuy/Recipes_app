from django.urls import path
from rest_framework.routers import SimpleRouter

from recipes.views import CategoryModelView, ProductModelView, CookingStepsModelView

router = SimpleRouter()
router.register('api/v1/category', CategoryModelView)
router.register('api/v1/product', ProductModelView)
router.register('api/v1/steps', CookingStepsModelView)

urlpatterns = [
]

urlpatterns += router.urls
