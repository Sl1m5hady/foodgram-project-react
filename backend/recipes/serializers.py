import base64
from rest_framework import serializers
from django.core.files.base import ContentFile
from .models import Recipe, Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(required=True, many=True)
    class Meta:
        model = Recipe
        fields = ('name', 'text', 'cooking_time', 'ingredients',
                  'image', 'tags')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
