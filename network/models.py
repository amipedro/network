from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    # Create your models here.
    following = models.ManyToManyField(
        'self', blank=True, symmetrical=False, related_name='followers')


class Woof(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    likes = models.ManyToManyField(User, blank=True, related_name='liked_by')

    class Meta:
        ordering = ('-created_at', '-updated_at')

    def __str__(self):
        return self.text


# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_liked")
#     post = models.ForeignKey(Woof, on_delete=models.CASCADE, null=True, blank=True, related_name="post_liked")


"""
class Following(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower', to_field="username")
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following', to_field="username")

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return '%s %s' % (self.user, self.following)
"""
