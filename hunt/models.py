import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
        
class Answer(models.Model):
    answer_text = models.CharField(max_length=400)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    right = models.BooleanField(default=False)
    made_on = models.DateTimeField('answer date', null=True, blank=True)


class Question(models.Model):
    question_text = models.CharField(max_length=400)
    answer1 = models.CharField(max_length=200)
    answer2 = models.CharField(max_length=200, null=True, blank=True)
    answer3 = models.CharField(max_length=200, null=True, blank=True)
    times_solved = models.IntegerField(default=0)
    number = models.IntegerField(default=1, unique=True)
    answers = models.ForeignKey(Answer, blank=True, null=True, on_delete=models.CASCADE)
        
    class Meta:
        ordering = ['number']

    def __str__(self):
        return self.question_text

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    captain = models.CharField(max_length=100)
    team_member2 = models.CharField(max_length=100, null=True, blank=True)
    team_member3 = models.CharField(max_length=100, null=True, blank=True)
    team_member4 = models.CharField(max_length=100, null=True, blank=True)
    team_member5 = models.CharField(max_length=100, null=True, blank=True)
    questions_answered = models.ManyToManyField(Question, blank=True, null=True)
    last_wrong_answer_made_on = models.DateTimeField('last wrong answer date', null=True, blank=True)

    def __str__(self):
        return self.user.username
        
    # def next_question_number(self):
    #     current_question_number = self.questions_answered.last().number
    #     return Question.objects.get(number = current_question_number + 1)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
