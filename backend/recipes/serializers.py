import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Favorite, Ingredient, IngredientRecipe, Recipe, ShoppingCart, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="ingredient.name")
    id = serializers.ReadOnlyField(source="ingredient.id")
    measurement_unit = serializers.ReadOnlyField(source="ingredient.measurement_unit")
    amount = serializers.ReadOnlyField()

    class Meta:
        model = IngredientRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ["id", "amount"]


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = AddIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ("name", "text", "cooking_time", "ingredients", "image", "tags")

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            ingredient["ingredient_id"] = ingredient.pop("id")
            ingredient["recipe_id"] = recipe.pk
            IngredientRecipe.objects.create(**ingredient)
        return recipe

    def update(self, recipe, validated_data):
        recipe.tags.clear()
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe.tags.set(tags)
        IngredientRecipe.objects.filter(recipe=recipe).delete()
        for ingredient in ingredients:
            ingredient["ingredient_id"] = ingredient.pop("id")
            ingredient["recipe_id"] = recipe.pk
            IngredientRecipe.objects.create(**ingredient)
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        context = {"request": self.context.get("request")}
        return GetRecipeSerializer(instance, context=context).data


class RecipeLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class GetRecipeSerializer(serializers.ModelSerializer):
    from users.serializers import UserSerializer

    ingredients = IngredientInRecipeSerializer(
        many=True, read_only=True, source="ingredientrecipe_set"
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "author",
            "name",
            "text",
            "cooking_time",
            "ingredients",
            "image",
            "tags",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def get_is_favorited(self, recipe):
        request = self.context.get("request")
        if request:
            user = self.context["request"].user
            if user.is_authenticated:
                return Favorite.objects.filter(recipe=recipe, user=user).exists()
        return False

    def get_is_in_shopping_cart(self, recipe):
        request = self.context.get("request")
        if request:
            user = self.context["request"].user
            if user.is_authenticated:
                return ShoppingCart.objects.filter(recipe=recipe, user=user).exists()
        return False


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("user", "recipe")
        validators = [
            serializers.UniqueTogetherValidator(
                fields=("user", "recipe"),
                queryset=Favorite.objects.all(),
                message="Этот рецепт уже находится в избранном!",
            )
        ]

    def to_representation(self, instance):
        recipe = Recipe.objects.get(id=instance.recipe_id)
        return RecipeLightSerializer(recipe).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ("user", "recipe")
        validators = [
            serializers.UniqueTogetherValidator(
                fields=("user", "recipe"),
                queryset=ShoppingCart.objects.all(),
                message="Этот рецепт уже находится в покупках!",
            )
        ]

    def to_representation(self, instance):
        recipe = Recipe.objects.get(id=instance.recipe_id)
        return RecipeLightSerializer(recipe).data
