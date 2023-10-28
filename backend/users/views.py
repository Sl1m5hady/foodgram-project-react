from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Follow
from users.serializers import FollowSerializer, UserWithRecipesSerializer
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    @action(detail=False, methods=['GET'],
            permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        data = {'follower': user.pk, 'following': author.pk}
        if request.method == 'POST':
            serializer = FollowSerializer(data=data, context={
                'request': request
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        if (request.method == 'DELETE'
                and Follow.objects.filter(**data).exists()):
            Follow.objects.get(**data).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            data={'errors': 'Подписки не существует'},
            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET',],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        paginator = self.paginator
        following = User.objects.filter(followed_by__follower=user)
        result = paginator.paginate_queryset(
            queryset=following, request=request
        )
        context = {'request': request}
        serializer = UserWithRecipesSerializer(
            result, many=True, context=context
        )
        return self.get_paginated_response(serializer.data)
