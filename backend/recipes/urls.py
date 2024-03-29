from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewset, RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewset, basename='ingredients')
router.register(r'recipes', RecipeViewSet)

app_name = 'recipes'

urlpatterns = [
    path('', include(router.urls)),
]
