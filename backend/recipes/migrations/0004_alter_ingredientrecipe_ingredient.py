# Generated by Django 3.2.3 on 2023-09-14 09:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_ingredientrecipe_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient'),
        ),
    ]
