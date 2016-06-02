from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.http import JsonResponse
from campaign.models import *
# Create your views here.
def index(request):
    posts = Post.objects.all()
    videos = Video.objects.all()
    web = {
    'topbanner':'New down for Somalia',
    'name':'JABRIL CAMPAIGN',
    'moto':"Let's build",
    }

    #return render(request, 'campaign/partials/home.html', {'web':web, 'speeches':speeches, 'featured_items':speeches})
    return render(request, 'campaign/partials/home.html', {"featured_items":posts, "latest_videos":videos})

def details(request, pk):
    post = Post.objects.get(pk=pk)
    post_comments = Comment.objects.filter(post=pk)
    posts = Post.objects.all()
    return render(request, 'campaign/partials/details.html',{"post":post, "latest_posts":posts, "post_comments":post_comments})

def contacts(request):
    contact_info = {
        "emails":["boolow5@gmail.com",],
        "phones":["+252-618-270616","+252-698-270616",],
        "websites":["jabril.so",],
        "facebookPages":["http://facebook.com/jabril-official",],
        "youtubeChannels":["http://youtube.com/jabril-official",],
        "twitter":["http:twitter.com/jabril-official",],
    }
    return render(request, 'campaign/partials/contacts.html',{"contacts":contact_info})


def watch(request, pk):
    video = Video.objects.get(pk=pk)
    return render(request, 'campaign/partials/watch.html',{"video":video})














def feed(request):
    return render(request, 'campaign/partials/details.html',{"postTitle":"Demo Titile One", "id":1})

def feedback(request):
    return render(request, 'campaign/partials/details.html',{"postTitle":"Demo Titile One", "id":1})


def events(request):
    return render(request, 'campaign/partials/details.html',{"postTitle":"Demo Titile One", "id":1})

def bio(request):
    return render(request, 'campaign/partials/details.html',{"postTitle":"Demo Titile One", "id":1})

def issues(request):
    return render(request, 'campaign/partials/details.html',{"postTitle":"Demo Titile One", "id":1})

def faq(request):
    return render(request, 'campaign/partials/details.html',{"postTitle":"Demo Titile One", "id":1})


 ############################
# BACKEND VIEWS            #
###########################
def likePost(request, pk):
    post = Post.objects.get(pk=pk)
    post.likes += 1
    post.save()
    return JsonResponse({"likes":post.likes})

def likeComment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.likes += 1
    comment.save()
    return JsonResponse({"likes":comment.likes})
