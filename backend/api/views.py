import io

from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from recipes.serializers import (FavoriteSerializer, IngredientSerializer,
                                 RecipeSerializer, ShoppingCartSerializer,
                                 TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['post', 'get', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST', 'DELETE'])
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

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
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

    @action(detail=False, methods=['GET'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        timesb = TTFont("TimesB", "data/timesbd.ttf")
        times = TTFont("Times", "data/times.ttf")
        pdfmetrics.registerFont(timesb)
        pdfmetrics.registerFont(times)
        p.setFont("TimesB", 20)
        y = 800
        p.drawString(50, y, "Список покупок:")

        ingredients = (
            IngredientRecipe.objects.filter(
                recipe__in_shopping_cart__user=request.user)
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(value=Sum("amount"))
        )

        for ingredient in ingredients:
            p.setFont("Times", 16)
            line = (
                f'{ingredient["ingredient__name"]}: '
                f'{ingredient["ingredient__measurement_unit"]} '
                f'{ingredient["value"]}'
            )
            y = y - 40
            p.drawString(50, y, line)

        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="file.pdf")

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
