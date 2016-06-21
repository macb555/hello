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
    photo = models.ImageField(upload_to="static/campaign/images", null=True, blank=True)
    view_counter = models.IntegerField(default=0)
    alt = models.CharField(max_length=30)
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
    dislikes = models.IntegerField(default=0)
    category = models.ForeignKey(Category, blank=False)
    author = models.ForeignKey(User, blank=False)
    featured_image = models.ForeignKey(Image, blank=True)
    view_counter = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name="comment", null=True, blank=True)
    parent = models.ForeignKey('self', null=True, related_name="replies")
    user = models.ForeignKey(User, blank=False)
    text = models.TextField(max_length=500)
    date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.user) + " said " +self.text

class Like(models.Model):
    liked_post = models.ForeignKey(Post, related_name="liked_post", null=True, blank=True)
    liked_comment = models.ForeignKey(Comment, related_name="liked_comment", null=True, blank=True)
    user = models.ForeignKey(User, blank=False, null=True)
    def __unicode__(self):
        if self.liked_post == None:
            if self.liked_comment != None:
                return self.user.username+ " liked comment: " +str(self.liked_comment.pk)
        elif self.liked_comment == None:
            if self.liked_post != None:
                return self.user.username+ " liked post: "+ str(self.liked_post.pk)
        else:
            return "Maybe this was added by a hacker."

class Dislike(models.Model):
    disliked_post = models.ForeignKey(Post, related_name="disliked_post", null=True, blank=True)
    disliked_comment = models.ForeignKey(Comment, related_name="disliked_comment", null=True, blank=True)
    reason = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, blank=False)
    def __unicode__(self):
        if self.disliked_post:
            return self.user.username + "disliked post: "+str(self.disliked_post)
        elif self.disliked_comment:
            return self.user.username + "disliked post: "+str(self.disliked_post)

class Message(models.Model):
    email = models.EmailField(blank=False, null=False)
    message = models.TextField(max_length=500)
    date = models.DateTimeField(default=timezone.now)
