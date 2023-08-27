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


class Recipy(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='recipes',
                               on_delete=models.CASCADE)
    text = models.TextField()
    cooking_time = models.SmallIntegerField()  # добавиьб валицацию >= 1
    image = models.ImageField(upload_to='recipes/images/')
    tags = models.ManyToManyField(Tag, through='TagRecipy')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientRecipy')


class TagRecipy(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipy = models.ForeignKey(Recipy, on_delete=models.CASCADE)


class IngredientRecipy(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipy = models.ForeignKey(Recipy, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()  # валидация
