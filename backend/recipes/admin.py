from django.contrib import admin
from django.contrib.admin.utils import quote
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from users.models import User, MyTokenProxy, MyToken
from subscriptions.models import Subscription
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag, TagRecipe)

User = get_user_model()


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


class TokenChangeList(ChangeList):
    """Map to matching User id"""
    def url_for_result(self, result):
        pk = result.user.pk
        return reverse('admin:%s_%s_change' % (self.opts.app_label,
                                               self.opts.model_name),
                       args=(quote(pk),),
                       current_app=self.model_admin.admin_site.name)


class MyTokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    fields = ('user',)
    ordering = ('-created',)
    actions = None

    def get_changelist(self, request, **kwargs):
        return TokenChangeList

    def get_object(self, request, object_id, from_field=None):
        queryset = self.get_queryset(request)
        field = User._meta.pk
        try:
            object_id = field.to_python(object_id)
            user = User.objects.get(**{field.name: object_id})
            return queryset.get(user=user)
        except (queryset.model.DoesNotExist, User.DoesNotExist, ValidationError, ValueError):
            return None

    def delete_model(self, request, obj):
        token = MyToken.objects.get(key=obj.key)
        return super().delete_model(request, token)


admin.site.register(MyTokenProxy, MyTokenAdmin)
admin.site.register(User, UsersAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Subscription, SubscriptionsAdmin)
