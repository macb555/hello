from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = CharField(max_length=100)
    description = TextField()

class Video(models.Model):
    videoId = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.CharField(max_length=300)

class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=350)
    video = models.ForeignKey(Video,blank=True, default=None)
    content = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    category = models.ForeignKey(Category, blank=False)

class Comment(models.Model):
    user = models.ForeignKey(User, blank=False)
    text = models.TextField(max_length=500)
    date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
