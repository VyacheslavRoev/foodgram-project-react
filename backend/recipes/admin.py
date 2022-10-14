from django.contrib import admin
from users.models import User

from recipes.models import Ingredient, IngredientAmount, Recipe, Tag, TagRecipe


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
        return obj.favorite_recipes.count()

    count_of_favorites.short_description = 'Добавление в избранное'


admin.site.register(User, UsersAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
