from rest_framework import viewsets
from .serializers import RecipeSerializer, TagSerializer,  AddIngredientSerializer
from .models import Recipe, Ingredient, Tag


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = AddIngredientSerializer
    queryset = Ingredient.objects.all()