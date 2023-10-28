from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import Recipe
from recipes.serializers import RecipeLightSerializer
from users.models import Follow

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password')
        read_only_fields = ('id',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Запрещенное имя пользователя')
        return value


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed']

    def get_is_subscribed(self, instance):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(follower=user,
                                     following=instance).exists()


class UserWithRecipesSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['recipes', 'recipes_count']

    def get_recipes_count(self, instance):
        return instance.recipes.count()

    def get_recipes(self, instance):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=instance)
        if limit:
            recipes = recipes[:int(limit)]
        return RecipeLightSerializer(recipes, many=True, read_only=True).data


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('follower', 'following')
        validators = [
            serializers.UniqueTogetherValidator(
                fields=('follower', 'following'),
                queryset=Follow.objects.all(),
                message='Подписка уже существует.'
            )
        ]

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        user = User.objects.get(pk=instance.following_id)
        return UserWithRecipesSerializer(user, context=context).data
