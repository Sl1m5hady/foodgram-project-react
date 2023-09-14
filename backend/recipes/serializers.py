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


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    id = serializers.ReadOnlyField(source='ingredient.id')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')
    amount = serializers.ReadOnlyField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientSerializer(serializers.ModelSerializer):
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
    ingredients = AddIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'cooking_time', 'ingredients',
                  'image', 'tags')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        # recipe.ingredients.set(ingredients)
        for ingredient in ingredients:
            ingredient['ingredient_id'] = ingredient.pop('id')
            # ingredient.pop('id')
            ingredient['recipe_id'] = recipe.pk
            IngredientRecipe.objects.create(**ingredient)
            # recipe.ingredients.set(current_ingredient)
        return recipe
#         # for ingredient in ingredients:

    def update(self, recipe, validated_data):  # Bulk_create
        recipe.tags.clear()
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe.tags.set(tags)
        IngredientRecipe.objects.filter(recipe=recipe).delete()
        for ingredient in ingredients:
            ingredient['ingredient_id'] = ingredient.pop('id')
            # ingredient.pop('id')
            ingredient['recipe_id'] = recipe.pk
            IngredientRecipe.objects.create(**ingredient)
        # recipe.objects.update(**validated_data)
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return GetRecipeSerializer(instance, context=context).data


class GetRecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientInRecipeSerializer(many=True, read_only=True,
                                               source='ingredientrecipe_set')

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'text', 'cooking_time',
                  'ingredients', 'image', 'tags')
        read_only_fields = ('id', 'author')
        # depth = 1
