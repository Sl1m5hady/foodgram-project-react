# Generated by Django 3.2.3 on 2023-09-12 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0002_rename_recipy_ingredientrecipe_recipe"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredientrecipe",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredietrecipe",
                to="recipes.ingredient",
            ),
        ),
    ]
