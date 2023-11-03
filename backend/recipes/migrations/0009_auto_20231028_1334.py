# Generated by Django 3.2.3 on 2023-10-28 13:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0008_shoppingcart_unique_in_shopping_cart"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ingredient",
            options={
                "verbose_name": "Ингредиент",
                "verbose_name_plural": "Ингредиенты",
            },
        ),
        migrations.AlterModelOptions(
            name="recipe",
            options={
                "verbose_name": "Рецепт",
                "verbose_name_plural": "Рецепты",
            },
        ),
        migrations.AlterModelOptions(
            name="tag",
            options={"verbose_name": "Тег", "verbose_name_plural": "Теги"},
        ),
        migrations.AlterField(
            model_name="tag",
            name="color",
            field=models.CharField(
                blank=True,
                max_length=7,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Неверный цвет",
                        regex="^#([a-fA-f0-9]{6}|[a-fA-f0-9]{3})$",
                    )
                ],
            ),
        ),
    ]
