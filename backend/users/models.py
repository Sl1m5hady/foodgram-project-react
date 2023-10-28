from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='followed_by')
