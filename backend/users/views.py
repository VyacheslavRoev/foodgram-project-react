from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Subscribtions, User
from users.serializers import (SubscriptionCreateSerializer,
                               SubscriptionSerializer, UserSerializer)


class CustomUserViewset(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class SubscribeView(APIView): 
    """Добавление и удаление подписки.""" 
    serializer_class = SubscriptionSerializer 
    permission_classes = (IsAuthenticated,) 

    def post(self, request, *args, **kwargs): 
        id = kwargs.get('pk')
        user = self.request.user
        author = get_object_or_404(User, id=id)
        data = {'user': user.id, 'author': id}
        serializer = SubscriptionCreateSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        follow = Subscribtions.objects.create(user=user, author=author)
        serializer = SubscriptionCreateSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        user = self.request.user
        author = get_object_or_404(User, id=id)
        follow = Subscribtions.objects.filter(user=user, author=author)
        if follow.exists():
            follow.delete()
            return Response(
                {'detail': 'Вы отписались от автора'},
                status=status.HTTP_204_NO_CONTENT
            )


class SubscribeListView(ListAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)
