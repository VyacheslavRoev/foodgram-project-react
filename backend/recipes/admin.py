from django.contrib import admin
from users.models import Subscribtions, User

from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag, TagRecipe)


class IngredientAmountInLine(admin.TabularInline):
    model = IngredientAmount
    extra = 1


class TagRecipeInLine(admin.TabularInline):
    model = TagRecipe
    extra = 1


class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'first_name', 'last_name', 'email')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    empty_value_display = "-пусто-"


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


admin.site.register(User, UsersAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Subscribtions, SubscriptionsAdmin)
