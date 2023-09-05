from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import include, path
from recipes.views import RecipeViewSet, TagViewSet, IngredientViewSet

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('api/auth/', include('djoser.urls.authtoken')),
]
