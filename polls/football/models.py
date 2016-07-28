from django.db import models
# Create your models here.
from django.utils import  timezone
import  datetime


class Question (models.Model):

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    # def published_date(self):
    #
    #     return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def published_date(self):
        now = timezone.now()
        return now-datetime.timedelta(days=1) < self.pub_date <=now
    published_date.admin_order_field = 'pub_date'
    published_date.boolean = True
    published_date.short_description = "Published Recently??"


class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
