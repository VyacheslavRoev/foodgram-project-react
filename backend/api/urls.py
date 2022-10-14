from django.urls import include, path
from recipes.views import IngredientViewset, RecipeViewSet, TagViewSet
from rest_framework.routers import DefaultRouter
from users.views import SubscribeListView, SubscribeView, UserViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewset, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'users/subscriptions/',
        SubscribeListView.as_view(),
        name='subscriptions'
    ),
    path(
        'users/<int:user_id>/subscribe/',
        SubscribeView.as_view(),
        name='subscribe'
    ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
