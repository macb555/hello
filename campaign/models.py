from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __unicode__(self):
        return self.name

class VideoType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    def __unicode__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=100, default="The Title")
    videoId = models.CharField(max_length=100)
    type = models.ForeignKey(VideoType, blank=False)
    description = models.CharField(max_length=300)
    def __unicode__(self):
        return str(self.type) + ": "+self.title

class Image(models.Model):
    description = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    alt = models.CharField(max_length=30)
    view_counter = models.IntegerField(default=0)
    def __unicode__(self):
        return " id:"+str(self.pk) + " alt:"+ self.alt

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
    author = models.ForeignKey(User, blank=False)
    featured_image = models.ForeignKey(Image, blank=True)
    view_counter = models.IntegerField(default=0)
    def __unicode__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, blank=True)
    user = models.ForeignKey(User, blank=False)
    text = models.TextField(max_length=500)
    date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.user) + " said " +self.text
