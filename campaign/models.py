from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django_countries.fields import CountryField

# Create your models here.
'''
class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    country = CountryField()
    city = models.CharField(max_length=20)

    objects = UserManager()

    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email
'''

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
    #url = models.CharField(max_length=500)
    #photo = models.ImageField(upload_to="static/campaign/images", null=True, blank=True)
    photo = models.ImageField(upload_to = 'images/%Y/%m/%d', default = 'images/None/no-image.png')
    view_counter = models.IntegerField(default=0)
    alt = models.CharField(max_length=30)
    def __unicode__(self):
        return " id:"+str(self.pk) + " alt:"+ self.alt

class Post(models.Model):
    title = models.CharField(max_length=200)
    language = models.CharField(max_length=15, choices=(("en", "English"),
                                        ("so", "Somali"),), default='so')
    description = models.CharField(max_length=350)
    video = models.ForeignKey(Video,blank=True, default=1, null=True)
    content = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    category = models.ForeignKey(Category, blank=False)
    author = models.ForeignKey(User, blank=False)
    featured_image = models.ForeignKey(Image, blank=True, default=1)
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
    approved = models.BooleanField(default=False)

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
    def __unicode__(self):
        return "From: " + self.email

class Location(models.Model):
    user =  models.OneToOneField(User)
    current_country = CountryField()
    current_city = models.CharField(max_length=30)
    region_of_birth = models.CharField(max_length=30, choices=[("Awdal","Awdal"), ("Bakool","Bakoo"), ("Banaadir","Banaadir"), ("Bari","Bari"), ("Bay", "Bay"), ("Galguduud","Galguduud"),("Gedo","Gedo"), ("Hiiraan","Hiiraan"),("Jubada Dhexe","Jubada Dhexe"),("Jubada Hoose","Jubada Hoose"), ("Nugaal","Nugaal"), ("Sanaag","Sanaag"), ("Shabeelaha Dhexe", "Shabeelaha Dhexe"), ("Shabeelaha Hoose","Shabeelaha Hoose"), ("Sool","Sool"), ("Togdheer","Togdheer"), ("Waqooyi Galbeed", "Waqooyi Galbeed")])
    city_of_birth = models.CharField(max_length=30)
    def __str__(self):
        return str(self.user.username)+" lives in " + str(self.current_city) + ", "+ str(self.current_country.name)
