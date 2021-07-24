from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from model_utils.models import TimeStampedModel


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.first_name

class Tweet(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    content = models.CharField(max_length=140)

    def __str__(self):
        return self.content + " by " + self.user.username

class Relationship(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return self.user.first_name + " follows " + self.following_user.first_name

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
