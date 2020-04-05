import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Question(models.Model):
    question_text = models.CharField(max_length=400)
    answer1 = models.CharField(max_length=200)
    answer2 = models.CharField(max_length=200, null=True)
    answer3 = models.CharField(max_length=200, null=True)
    times_solved = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text

class Profile(models.Model):
    team = models.OneToOneField(User, on_delete=models.CASCADE)
    captain = models.CharField(max_length=100)
    team_member2 = models.CharField(max_length=100, null=True, blank=True)
    team_member3 = models.CharField(max_length=100, null=True, blank=True)
    team_member4 = models.CharField(max_length=100, null=True, blank=True)
    team_member5 = models.CharField(max_length=100, null=True, blank=True)
    last_question_answered = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    last_wrong_answered_made_on = models.DateTimeField('last wrong answer date', null=True, blank=True)

    def __str__(self):
        return self.user.username

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
