from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, blank=True)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='recipes',
                               on_delete=models.CASCADE)
    text = models.TextField()
    cooking_time = models.SmallIntegerField()  # добавиьб валицацию >= 1
    image = models.ImageField(upload_to='recipes/images/')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientRecipe')


# class TagRecipe(models.Model):
#     tag = models.ForeignKey(Tag, related_name='recipes',
#                             on_delete=models.CASCADE)
#     recipy = models.ForeignKey(Recipe, related_name='tags',
#                                on_delete=models.CASCADE)


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.SmallIntegerField()  # валидация
