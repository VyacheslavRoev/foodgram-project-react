from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewset, RecipeViewSet, TagViewSet

app_name = 'recipes'

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewset, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls))
]

