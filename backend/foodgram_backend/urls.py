from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.conf import settings

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import CustomUserViewSet
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'users', CustomUserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
