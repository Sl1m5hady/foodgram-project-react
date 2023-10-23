from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import Follow
from recipes.models import Recipe
from recipes.serializers import RecipeLightSerializer


User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password')
        read_only_fields = ('id',)


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed']

    def get_is_subscribed(self, instance):
        print(self.context)
        user = self.context.get('request').user
        print(self.context.get('request'))
        return Follow.objects.filter(follower=user,
                                     following=instance).exists()


class UserWithRecipesSerializer(UserSerializer):
    recipes = RecipeLightSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['recipes', 'recipes_count']

    def get_recipes_count(self, instance):
        return instance.recipes.count()


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
        print(self.context)
        context = {'request': self.context.get('request')}
        user = User.objects.get(pk=instance.following_id)
        return UserWithRecipesSerializer(user, context=context).data
