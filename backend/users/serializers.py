from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer as BaseSerializer
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from recipes.models import Recipe
from users.models import Subscribtions, User


class UserRegistrationSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribtions.objects.filter(user=user, author=obj.id).exists()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')


class RecipeSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField(read_only=True)

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Subscribtions.objects.filter(
            author=obj, user=self.context['request'].user
        ).exists()

    def get_recipes(self, obj):
        request = self.context['request']
        limit = request.GET.get('recipes_limit')
        author = get_object_or_404(User, id=obj.pk)
        recipes = author.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeSubscriptionSerializer(
            recipes,
            many=True,
            context={'request': request}
        )
        return serializer.data

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
        default=CurrentUserDefault(),
    ),
    author = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all())

    def validate(self, data):
        user = data['following']
        author = data['follower']
        if self.context['request'].method == 'POST' and user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return data

    class Meta:
        model = Subscribtions
        fields = ('user', 'author')
