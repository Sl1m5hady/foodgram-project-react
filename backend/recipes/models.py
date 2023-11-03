from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField("Название", max_length=200)
    measurement_unit = models.CharField("Еденица измерения", max_length=200)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField("Название", max_length=200)
    color = models.CharField(
        "Цвет",
        max_length=15,
        blank=True,
        validators=[
            RegexValidator(
                regex="^#([a-fA-f0-9]{6}|[a-fA-f0-9]{3})$",
                message="Неверный цвет",
            )
        ],
    )
    slug = models.SlugField("Слаг", max_length=200)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField("Название", max_length=200)
    author = models.ForeignKey(
        User,
        related_name="recipes",
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    text = models.TextField("Текст")
    cooking_time = models.SmallIntegerField(
        "Время приготовления", validators=[MinValueValidator(1)]
    )
    image = models.ImageField("Изображение", upload_to="recipes/images/")
    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
        verbose_name="Теги",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientRecipe",
        verbose_name="Ингредиенты",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.SmallIntegerField()


class Favorite(models.Model):
    user = models.ForeignKey(
        User, related_name="favorite", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, related_name="favorited_by", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_favorite"
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, related_name="shopping_cart", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, related_name="in_shopping_cart", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_in_shopping_cart"
            )
        ]
