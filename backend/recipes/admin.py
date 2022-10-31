from django.contrib import admin
from rest_framework.authtoken.models import Token
from django.conf import settings
from users.models import User
from subscriptions.models import Subscription
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag, TagRecipe)


class IngredientAmountInLine(admin.TabularInline):
    model = IngredientAmount
    extra = 1


class TagRecipeInLine(admin.TabularInline):
    model = TagRecipe
    extra = 1


class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 1


class SubscriptionsInLine(admin.TabularInline):
    model = Subscription
    fk_name = 'user'
    extra = 1


class ShoppingInline(admin.TabularInline):
    model = ShoppingCart
    extra = 1


class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'first_name', 'last_name', 'email')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    inlines = [
        FavoriteInline,
        SubscriptionsInLine,
        ShoppingInline
    ]
    empty_value_display = "-пусто-"
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        if not is_superuser:
            disabled_fields |= {
                'is_superuser',
                'user_permissions',
            }
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_of_favorites',)
    list_filter = ('name', 'author', 'tags',)
    search_fields = ('name', 'author', 'tags',)
    inlines = [
        IngredientAmountInLine,
        TagRecipeInLine
    ]
    readonly_fields = ('count_of_favorites',)

    def count_of_favorites(self, obj):
        return obj.favorites.count()

    count_of_favorites.short_description = 'Добавление в избранное'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    empty_value_display = '-пусто-'


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    list_filter = ('user', 'author',)
    search_fields = ('user', 'author',)
    empty_value_display = '-пусто-'


class TokenProxy(Token):
    """
    Proxy mapping pk to user pk for use in admin.
    """
    @property
    def pk(self):
        return self.user_id

    class Meta:
        proxy = 'rest_framework.authtoken' in settings.INSTALLED_APPS
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = "Токен"
        verbose_name_plural = "Токены"


admin.site.register(User, UsersAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Subscription, SubscriptionsAdmin)
