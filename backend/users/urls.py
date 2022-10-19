from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscribeListView, SubscribeView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

app_name = 'users'

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
