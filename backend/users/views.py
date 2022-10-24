from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import User
from .serializers import UserSerializer


class CustomUserViewset(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
