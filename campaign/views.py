from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.http import JsonResponse
from campaign.models import *
from campaign.forms import *
# Create your views here.
def index(request):
    posts = Post.objects.all()
    videos = Video.objects.all()
    loginForm = LoginForm()
    #return render(request, 'campaign/partials/home.html', {'web':web, 'speeches':speeches, 'featured_items':speeches})
    return render(request, 'campaign/partials/home.html', {"loginform":loginForm,"featured_items":posts,"post":{"pk":0}, "latest_videos":videos})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form)
            return JsonResponse({"status":""})
    else:
        form = CommentForm()
        print(form)
        return JsonResponse({"form":form})


def logout(request):
    return JsonResponse({"status":"You're logged out"})

def invalid_login(request):
    return JsonResponse({"status":"Sorry you failed to login"})


def details(request, pk):
    loginForm = LoginForm()
    post = get_object_or_404(Post, pk=pk)
    post_comments = Comment.objects.filter(post=pk, approved=True)
    posts = Post.objects.all()
    form = CommentForm()
    return render(request, 'campaign/partials/details.html',{"loginform":loginForm,"post":post, "latest_posts":posts, "post_comments":post_comments,"form":form})

def contact(request):
    loginForm = LoginForm()
    contact_info = {
        "emails":["boolow5@gmail.com",],
        "phones":["+252-618-270616","+252-698-270616",],
        "websites":["jabril.so",],
        "facebookPages":["http://facebook.com/jabril-official",],
        "youtubeChannels":["http://youtube.com/jabril-official",],
        "twitter":["http:twitter.com/jabril-official",],
    }
    return render(request, 'campaign/partials/contacts.html',{"loginform":loginForm,"contacts":contact_info, "post":{"pk":0}})


def watch(request, pk):
    loginForm = LoginForm()
    video = get_object_or_404(Video,videoId=pk)
    post =  post = Post.objects.filter(video_id=video.pk)
    return render(request, 'campaign/partials/watch.html',{"loginform":loginForm,"video":video, "post":{"pk":0}})

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
    loginForm = LoginForm()
    posts = Post.objects.all()
    return render(request, 'campaign/partials/feeds.html',{"loginform":loginForm,"posts":posts, "post":{"pk":0}})

def feedback(request):
    loginForm = LoginForm()
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            return JsonResponse({"feedback":feedback})
    else:
        form = FeedbackForm()
        return render(request, 'campaign/partials/feedback.html',{"loginform":loginForm,'form':form, "post":{"pk":0}})


def events(request):
    loginForm = LoginForm()
    posts = Post.objects.filter(category__name="Events")
    return render(request, 'campaign/partials/events.html',{"loginform":loginForm,"posts":posts, "post":{"pk":0}})

def bio(request):
    loginForm = LoginForm()
    posts = get_object_or_404(Post, category__name="bio")
    return render(request, 'campaign/partials/details.html',{"loginform":loginForm,"post":posts})

def issues(request):
    loginForm = LoginForm()
    #posts = get_object_or_404(Post, category__name="issues")
    posts = Post.objects.filter(category__name="Issues")
    return render(request, 'campaign/partials/issues.html',{"loginform":loginForm,"posts":posts, "post":{"pk":0}})

def faq(request):
    loginForm = LoginForm()
    posts = get_object_or_404(Post, category__name="faq")
    return render(request, 'campaign/partials/details.html',{"loginform":loginForm,"post":posts})


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
    if user.is_authenticated():
        dislikes = Dislike.objects.filter(disliked_post_id=pk, user=request.user)
    else:
        dislikes = []
    post = Post.objects.get(pk=pk)
    if not len(dislikes) > 0:
        new_dislike = Dislike()
        new_dislike.disliked_post_id = pk
        if user.is_authenticated():
            new_dislike.user = request.user
        else:
            new_dislike.user = None
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

def AmIIn(request):
    return JsonResponse({"status":user.is_authenticated()})

def changeLanguage(request, language):
    if language == 'so' or language == 'en':
        request.session["language"] = language
        return redirect("index")
    else:
        posts = Post.objects.all()
        videos = Video.objects.all()
        loginForm = LoginForm()
        return render(request, 'campaign/partials/home.html', {"error":"Sorry \""+language+"\" is an invalid language. \"so\"(for Somali) and \"en\"(for English) are available","loginform":loginForm,"featured_items":posts,"post":{"pk":0}, "latest_videos":videos})
