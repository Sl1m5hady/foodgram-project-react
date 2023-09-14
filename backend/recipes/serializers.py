import base64
from rest_framework import serializers
from django.core.files.base import ContentFile
from .models import Recipe, Tag, Ingredient, IngredientRecipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name')
    id = serializers.IntegerField(source='ingredient.id')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')



class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    # name = serializers.ReadOnlyField(source='ingredient.name')
    # measurement_unit = serializers.ReadOnlyField(
    #     source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ['id', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    # tags = TagSerializer(required=True, many=True)
    ingredients = IngredientRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'cooking_time', 'ingredients',
                  'image', 'tags')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        print(ingredients)
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        # recipe.ingredients.set(ingredients)
        for ingredient in ingredients:
            print(ingredient)
            ingredient['ingredient_id'] = ingredient['id']
            ingredient.pop('id')
            ingredient['recipe_id'] = recipe.pk
            IngredientRecipe.objects.create(**ingredient)
            # recipe.ingredients.set(current_ingredient)
        return recipe
#         # for ingredient in ingredients:

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return RecipeGetSerializer(instance, context=context).data


class RecipeGetSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True,
                                       source='ingredientrecipe_set')

    class Meta:
        model = Recipe
        fields = ('author', 'id', 'name', 'text', 'cooking_time',
                  'ingredients', 'image', 'tags')
        depth = 1
