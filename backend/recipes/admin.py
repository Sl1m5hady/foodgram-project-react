from django.contrib import admin

from .models import Ingredient, Tag, Recipy


admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipy)
