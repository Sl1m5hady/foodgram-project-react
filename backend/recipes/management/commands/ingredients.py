from django.core.management.base import BaseCommand, CommandError
import json
from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        f = open('data/ingredients.json')
        data = json.load(f)
        f.close()

        ingredients = []
        for ingredient in data:
            ingredient = Ingredient(**ingredient)
            ingredients.append(ingredient)

        Ingredient.objects.bulk_create(ingredients)
        self.stdout.write('Ингредиенты добавлены!')
