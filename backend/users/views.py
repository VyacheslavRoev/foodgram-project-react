from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Subscribtions, User
from users.serializers import SubscriptionSerializer, UserSerializer


class CustomUserViewset(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class SubscribeView(APIView):
    """Добавление и удаление подписки."""
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        author = get_object_or_404(User, id=user_id)
        Subscribtions.objects.create(
            user=request.user,
            author_id=user_id
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        subscription = Subscribtions.objects.filter(
            user=request.user,
            author_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeListView(ListAPIView):
    """Просмотр подписок."""
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)
