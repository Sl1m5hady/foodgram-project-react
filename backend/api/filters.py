import django_filters.rest_framework as df

from recipes.models import Recipe


class RecipeFilter(df.FilterSet):
    # author = df.CharFilter(field_name='author')
    tags = df.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = df.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = df.BooleanFilter(method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, field_name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorited_by__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, field_name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(in_shopping_cart__user=self.request.user)
        return queryset
