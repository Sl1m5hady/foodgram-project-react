from rest_framework import viewsets
from .serializers import RecipeSerializer, TagSerializer
from .models import Recipe, Ingredient, Tag


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = Ingredient
    queryset = Ingredient.objects.all()