from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User',related_name='questions' ,on_delete=models.CASCADE, null=True)

    @admin.display(boolean=True,ordering='pub_date',description='최근생성')
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        if self.was_published_recently():
            new_badge = 'NEW!!!'
        else:
            new_badge = ''
        return f'{new_badge} 제목: {self.question_text}, 날짜: {self.pub_date}'
    
    # was_published_recently.admin_order_field = 'pub_date'
    # was_published_recently.boolean = True 
    # was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question,related_name='choices',on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"[{self.question.question_text}]{self.choice_text}"
    
class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'voter'], name='unique_voter_for_questions')
        ]