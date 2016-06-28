from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.http import JsonResponse
from campaign.models import *
from campaign.forms import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db.models import Q
# Create your views here.
def index(request):
    language = request.session.setdefault('language','so')

    posts = Post.objects.filter(language=request.session.get('language')).exclude(category__name='About').order_by('-date_added')
    print(posts)
    videos = Video.objects.all()
    loginForm = LoginForm()
    #return render(request, 'campaign/partials/home.html', {'web':web, 'speeches':speeches, 'featured_items':speeches})
    return render(request, 'campaign/partials/home.html', {"loginform":loginForm,"featured_items":posts,"post":{"pk":0}, "latest_videos":videos})


def loginPage(request):
    loginForm = LoginForm()
    return render(request, 'campaign/partials/login.html', {"nosidebarlogin":True,"loginform":loginForm,"post":{"pk":0}})

def login(request):
    request.session.setdefault('language','so')


    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            msg = {'type':'info','so':"Waad ku guuleysatay gelitaanka!", 'en':'You loggedin successfully!'}
            return render(request, 'campaign/partials/message.html',{"no_twitter":True,"message":msg, "post":{"pk":0}})
        else:
            loginForm = LoginForm()
            msg = {'type':'danger','so':"Waan kaxunnahay cinwaankan wuu xiran yahay.", 'en':'Sorry, Your account is not active.'}
            return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})
    else:
        posts = Post.objects.filter(language=request.session.get('language')).exclude(category__name='About').order_by('-date_added')
        videos = Video.objects.all()
        loginForm = LoginForm()
        msg = {"type":"danger","so":"Waan kaxunnahay waxaad gelisay cinwaan ama ereysireed qaldan.","en":"Sorry! Your username or password is incorrect."}
        return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})

def register(request):
    form = UserRegistrationForm()

def logout(request):
    request.session.setdefault('language','so')

    auth_logout(request)
    loginForm = LoginForm()
    msg = {"type":"info","so":"Waad kuguuleysatay kabixitaanka.","en":"You have successfully logged out."}
    return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})


def details(request, pk):
    request.session.setdefault('language','so')

    loginForm = LoginForm()
    post = get_object_or_404(Post, pk=pk)
    post_comments = Comment.objects.filter(post=pk, approved=True)
    #posts = Post.objects.all()
    form = CommentForm()
    return render(request, 'campaign/partials/details.html',{"loginform":loginForm,"post":post, "latest_posts":"posts", "post_comments":post_comments,"form":form})

def contact(request):
    request.session.setdefault('language','so')

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
    request.session.setdefault('language','so')

    loginForm = LoginForm()
    video = get_object_or_404(Video,videoId=pk)
    post =  post = Post.objects.filter(video_id=video.pk)
    return render(request, 'campaign/partials/watch.html',{"loginform":loginForm,"no_twitter":True,"video":video, "post":{"pk":0}})

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
    request.session.setdefault('language','so')

    loginForm = LoginForm()
    posts = Post.objects.filter(language=request.session.get('language')).exclude(category__name='About').order_by('-date_added')
    return render(request, 'campaign/partials/feeds.html',{"loginform":loginForm,"posts":posts, "post":{"pk":0}})

def feedback(request):
    request.session.setdefault('language','so')

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
    request.session.setdefault('language','so')

    loginForm = LoginForm()
    posts = Post.objects.filter(category__name="Events",language=request.session.get('language')).exclude(category__name='About').order_by('-date_added')
    return render(request, 'campaign/partials/events.html',{"loginform":loginForm,"posts":posts, "post":{"pk":0}})

def about(request):
    request.session.setdefault('language','so')

    loginForm = LoginForm()
    posts = get_object_or_404(Post, category__name="About", language=request.session.get('language'))
    return render(request, 'campaign/partials/about.html',{"loginform":loginForm,"post":posts})

def issues(request):
    request.session.setdefault('language','so')

    loginForm = LoginForm()
    #posts = get_object_or_404(Post, category__name="issues")
    posts = Post.objects.filter(category__name="Issues",language=request.session.get('language')).exclude(category__name='About').order_by('-date_added')
    return render(request, 'campaign/partials/issues.html',{"loginform":loginForm,"posts":posts, "post":{"pk":0}})

def faq(request):
    request.session.setdefault('language','so')

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
        loginForm = LoginForm()
        msg = {'type':'info','so':"Waad ku guuleysatay bedelidda luqadda.", 'en':'You have successfully changed the language.'}
        return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})
    else:
        request.session.setdefault('language','so')
        loginForm = LoginForm()
        msg = {'type':'danger','so':"Waan kaxunnahay luqadda aad dooratay wili ma aanan kusoo derin boggeena.", 'en':"Sorry, we didn't add this language yet."}
        return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})

################ PURE PYTHON FUNCTIONS ##################
def getLanguage(request):
    current_language = request.session['language']
    if current_language == 'so':
        return current_language
    else:
        return 'en'
