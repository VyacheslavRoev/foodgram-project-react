from rest_framework.routers import DefaultRouter

from .views import IngredientViewset, RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewset, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

app_name = 'recipes'
