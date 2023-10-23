from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Favorite, Ingredient, Recipe, Tag, ShoppingCart
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer,
                          ShoppingCartSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST', 'DELETE'])
    # errors not non_field_error
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        data = {'user': user.id, 'recipe': recipe.pk}
        if request.method == 'POST':
            serializer = FavoriteSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        if (request.method == 'DELETE'
                and Favorite.objects.filter(**data).exists()):
            Favorite.objects.get(**data).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data={'errors': 'Подписки не существует'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        data = {'user': user.id, 'recipe': recipe.pk}
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        if (request.method == 'DELETE'
                and ShoppingCart.objects.filter(**data).exists()):
            ShoppingCart.objects.get(**data).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            data={'errors': 'Этот рецепт отсутствует в списке покупок'},
            status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
