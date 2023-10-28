from django.contrib import admin

from .models import Ingredient, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    list_filter = ['author', 'name', 'tags']
    search_fields = ['name', 'author__username', 'tags__name']
    readonly_fields = ['in_favorite']

    @admin.display(description='В избранном')
    def in_favorite(self, obj):
        return obj.favorited_by.count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']
    search_fields = ['name']


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
