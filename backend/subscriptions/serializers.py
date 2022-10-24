from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.serializers import RecipeSubscriptionSerializer
from users.models import User
from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField(read_only=True)

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Subscription.objects.filter(
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

    def validate(self, data):
        user = data['following']
        author = data['follower']
        if self.context['request'].method == 'POST' and user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        if self.context['request'].method == 'POST' and (
            Subscription.objects.filter(author=author, user=user).exists):
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя!'
            )
        return data

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
