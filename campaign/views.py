from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.http import JsonResponse
from campaign.models import *
from campaign.forms import *
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
    return render(request, 'campaign/partials/home.html', {"featured_items":posts,"post":{"pk":0}, "latest_videos":videos})

def details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post_comments = Comment.objects.filter(post=pk)
    posts = Post.objects.all()
    form = CommentForm()
    return render(request, 'campaign/partials/details.html',{"post":post, "latest_posts":posts, "post_comments":post_comments,"form":form})

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
    video = get_object_or_404(Video,videoId=pk)
    post =  post = Post.objects.filter(video_id=video.pk)
    return render(request, 'campaign/partials/watch.html',{"video":video, "post":{"pk":0}})

def addReply(request, post, parent):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            comment.post = post
            comment.parent = parent
            comment.date = timezone.now()
            return JsonResponse({"comment":comment})
    else:
        form = CommentForm()
        return JsonResponse({"form":form})

def addComment(request, post):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post
            comment.user = request.user
            comment.date = timezone.now()
            comment.save()
            return JsonResponse({"comment":comment.text, 'commentId':int(comment.pk),'username':comment.user.username})
    else:
        form = CommentForm()
        return JsonResponse({"form":form})



def feed(request):
    posts = Post.objects.all()
    return render(request, 'campaign/partials/feeds.html',{"posts":posts, "post":{"pk":0}})

def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            return JsonResponse({"feedback":feedback})
    else:
        form = FeedbackForm()
        return render(request, 'campaign/partials/feedback.html',{'form':form, "post":{"pk":0}})


def events(request):
    posts = Post.objects.filter(category__name="events")
    return render(request, 'campaign/partials/events.html',{"posts":posts, "post":{"pk":0}})

def bio(request):
    posts = get_object_or_404(Post, category__name="bio")
    return render(request, 'campaign/partials/details.html',{"post":posts})

def issues(request):
    #posts = get_object_or_404(Post, category__name="issues")
    posts = Post.objects.filter(category__name="issues")
    return render(request, 'campaign/partials/issues.html',{"posts":posts, "post":{"pk":0}})

def faq(request):
    posts = get_object_or_404(Post, category__name="faq")
    return render(request, 'campaign/partials/details.html',{"post":posts})


##############################
####  JSON BACKEND VIEWS  ####
##############################

#LIKES
def likePost(request, pk):
    likes = Like.objects.filter(liked_post_id=pk, user=request.user)
    post = Post.objects.get(pk=pk)
    if not len(likes) > 0:
        new_like = Like()
        new_like.liked_post_id = pk
        new_like.user = request.user
        new_like.save()
        like_count = Like.objects.filter(liked_post_id=pk).count()
        post.likes = like_count
        post.save()
    return JsonResponse({"likes":post.likes})

def likeComment(request, pk):
    print "called like comment view with id: "+pk
    likes = Like.objects.filter(liked_comment_id=pk, user=request.user)
    comment = Comment.objects.get(pk=pk)
    if not len(likes) > 0:
        print "saving new like record"
        new_like = Like()
        new_like.liked_comment_id = pk
        new_like.user = request.user
        new_like.save()
        like_count = Like.objects.filter(liked_comment_id=pk).count()
        comment.likes = like_count
        comment.save()
    return JsonResponse({"likes":comment.likes})

# DISLIKES
def dislikePost(request, pk):
    dislikes = Dislike.objects.filter(disliked_post_id=pk, user=request.user)
    post = Post.objects.get(pk=pk)
    if not len(dislikes) > 0:
        new_dislike = Dislike()
        new_dislike.disliked_post_id = pk
        new_dislike.user = request.user
        new_dislike.save()
        dislike_count = Dislike.objects.filter(disliked_post_id=pk).count()
        post.dislikes = dislike_count
        post.save()
    return JsonResponse({"dislikes":post.dislikes})

def dislikeComment(request, pk):
    dislikes = Dislike.objects.filter(disliked_comment_id=pk, user=request.user)
    comment = Comment.objects.get(pk=pk)
    if not len(dislikes) > 0:
        new_dislike = Dislike()
        new_dislike.disliked_comment_id = pk
        new_dislike.user = request.user
        new_dislike.save()
        dislike_count = Dislike.objects.filter(disliked_comment_id=pk).count()
        comment.dislikes = dislike_count
        comment.save()
    return JsonResponse({"dislikes":comment.dislikes})
