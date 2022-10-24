from django.urls import path
from subscriptions.views import SubscribeListView, SubscribeView


app_name = 'subscriptions'

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
]
