from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.http import JsonResponse
from campaign.models import *
from campaign.forms import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db.models import Q, F
from django.core.mail import EmailMessage
from django.utils import timezone
from JABRIL import settings
import uuid

from django.template import Context
from django.template.loader import render_to_string, get_template



# Create your views here.
def index(request):
    language = request.session.setdefault('language','so')

    posts = Post.objects.filter(likes__gte=F('dislikes'),language=request.session.get('language')).exclude(category__name='About').order_by('-date_added')
    videos = Video.objects.all()
    loginForm = LoginForm()
    #return render(request, 'campaign/partials/home.html', {'web':web, 'speeches':speeches, 'featured_items':speeches})
    return render(request, 'campaign/partials/home.html', {"loginform":loginForm,"featured_items":posts,"post":{"pk":0}, "latest_videos":videos})


def loginPage(request):
    loginForm = LoginForm()
    return render(request, 'campaign/partials/login.html', {"nosidebarlogin":True,"loginform":loginForm,"post":{"pk":0}})

def login(request):
    request.session.setdefault('language','so')
    username = request.POST.get('username')
    password = request.POST.get('password')
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
    request.session.setdefault('language','so')

    if request.method == "POST":
        print("Got data from user")

        userform = UserRegistrationForm(request.POST)
        profileForm = ProfileForm(request.POST)
        if userform.is_valid() and profileForm.is_valid():
            print("Data from the user is valid")
            username = request.POST.get('username')
            password = request.POST.get('password')
            f_name = request.POST.get('first_name')
            l_name = request.POST.get('last_name')
            email = request.POST.get('email')
            print("username:", username)
            print("password", password)
            print("first_name", f_name)
            print("last_name", l_name)

            user = User.objects.create_user(username=username, password=password, first_name=f_name, last_name=l_name, email=email)
            user.save()
            print("User subject is saved")
            print("Loggin user in")
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            print("User is logged in")
            #form = profileForm()
            #return render(request, 'campaign/partials/register_profile.html', {'form':form})
            print("Initializing user profile")
            profile = Profile.objects.create(user=request.user,
                        current_country=request.POST.get('current_country'),
                        city_of_residence=request.POST.get('city_of_residence'),
                        region_of_birth = request.POST.get('region_of_birth'),
                        city_of_birth=request.POST.get('city_of_birth'),
                        phone_no=request.POST.get('phone_no'),
                        mother_name=request.POST.get('mother_name'),
                        gender=request.POST.get('gender'),
                        marital_status=request.POST.get('marital_status'))
            profile.save()
            print("Saved user profile")
            print("Returning to home page.")
            return redirect('index')

    print("Sending a fresh user registration form")
    userform = UserRegistrationForm()
    profileForm = ProfileForm(initial={'country': 'SO'})
    print("Rendering the form")
    return render(request, 'campaign/partials/registration.html', {'userform':userform, 'profileForm':profileForm})

def register_profile(request):
    request.session.setdefault('language','so')
    profile = get_object_or_404(profile, user__pk=request.user.pk)
    if profile == None:
        if request.method == "POST":
            profileForm = profileForm(request.POST)
            if request.user.is_authenticated():
                if profileForm.is_valid():
                    username = request.POST.get('username')
                    password = request.POST.get('password')

                    profile = Profile.objects.create(user=request.user,
                                current_country=request.POST.get('current_country'),
                                city_of_residence=request.POST.get('city_of_residence'),
                                region_of_birth = request.POST.get('region_of_birth'),
                                city_of_birth=request.POST.get('city_of_birth'),
                                phone_no=request.POST.get('phone_no'),
                                mother_name=request.POST.get('mother_name'),
                                gender=request.POST.get('gender'),
                                marital_status=request.POST.get('marital_status'))
                    profile.save()
                    return redirect('index')
    else:
        profileForm = profileForm(instance=profile)
        return render(request, 'campaign/partials/register_profile.html', {'profileForm':profileForm,'profile':profile})

    profileForm = profileForm(initial={'country': 'SO'})
    return render(request, 'campaign/partials/register_profile.html', {'profileForm':profileForm})

def getNewUser(request):
    request.session.setdefault('language','so')
    #check if user is logged in
    print("User registration view:")
    allUsers = User.objects.all().count()
    #If user posts a form
    if request.method=='POST':
        if not request.user.is_authenticated():
            print("No logged in user")
            form = UserInfoForm(request.POST)

            if form.is_valid():
                print("User provided a valid form")
                #if not, check if username or email exists in the database
                username = request.POST.get('username')
                email = request.POST.get('email')
                password = request.POST.get('password')
                f_name = request.POST.get('first_name')
                l_name = request.POST.get('last_name')

                newUser = User.objects.filter(Q(username=username)|Q(email=email))
                #if there is some other user with this username or email
                if len(newUser)>0:
                    print("There is already another user with:")
                    #If the email is already registered
                    if newUser[0].email == email:
                        print("This email")
                        loginForm = LoginForm()
                        msg = {"type":"danger","so":"Waan ka xunnahay, email-kan horay ayaa loo diiwaangeliyay. Fadlan midkale isticmaal.","en":"Sorry, this email is already registered. Please use a different email"}
                        return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})
                    #If the username was already taken
                    elif newUser.username == username:
                        print("This username")
                        loginForm = LoginForm()
                        msg = {"type":"danger","so":"Waan ka xunnahay, magackugalkan(username-kan) horay ayaa loo diiwaangeliyay. Fadlan isku day markale adigoo adeegsanaya magackugal kale.","en":"Sorry, this username is already registered. Please use a different username and try again"}
                        return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})
                #if not, create new user and set active to false
                elif len(newUser)==0:
                    print("Your username and email are OK")
                    user = User.objects.create_user(username=username, password=password, first_name=f_name, last_name=l_name, email=email)
                    user.is_active = False
                    user.save()
                    new_user_profile = Profile.objects.create(user=user)
                    new_user_profile.activation_code = generate_unique_code()
                    try:
                        sendVarificationEmail(request, user, new_user_profile.activation_code)
                    except:pass
                    loginForm = LoginForm()
                    msg = {"type":"info","so":"Waad ku guuleysatay iska diiwaangelinta Hal Qaran. Si aad noogu xaqiijiso in aad email-kan leedahay, fariinta aan kusoo dirnay fur kadib riix mareegta kujirta si laguugu fasaxo adeegyada ay helaan xubnaha Hal Qaran","en":"You have successfully registered to Hal Qaran. To varify this email belongs to you, open the email we sent you and click the link in the message."}
                    return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})
            #If the form is not valid
            print("The form is invalid")
            return render(request, 'campaign/partials/registration1.html', {'userform':form, 'usercounter':allUsers})
    #If the user requested a form
    userform=UserInfoForm()
    print("Rendering a fresh user registration form")
    return render(request, 'campaign/partials/registration1.html', {'userform':userform, 'usercounter':allUsers})

def getNewPerson(request, serialNo):
    request.session.setdefault('language','so')
    #check if user is loggedin.
    if request.user.is_authenticated() and request.user.is_active():
        form = PersonalInfoForm(request.POST)
        allUsers = User.objects.all().count()
        if form.is_valid():
            user = request.user
            try:
                profile = Profile.objects.get(user=user)
            except:
                profile = Profile.objects.create(user=user)
            mother_name = request.POST.get('mother_name')
            gender = request.POST.get('gender')
            marital_status = request.POST.get('marital_status')
            phone_no = request.POST.get('phone_no')

            profile.mother_name = mother_name
            profile.gender = gender
            profile.marital_status = marital_status
            profile.phone_no = phone_no
            profile.registration_step = 1

            profile.save()
            return redirect('getNewLocation')
        return render(request, 'campaign/partials/registration2.html', {'personalform':form, 'usercounter':allUsers})
    else:
        return redirect('login')


def varifyUser(request, user, varification_code):
    if request.user.is_authenticated():
        print("")
        if request.user.is_active():
            return redirect('index')
        else:
            profile = Profile.objects.get(user=request.user)
            if profile.activation_code == varification_code:
                print("Your serial no is correct")
                profile.user.is_active = True
                profile.save()
                return redirect('getNewPerson')
            else:
                loginForm = LoginForm()
                msg = {"type":"danger","so":"Waan ka xunnahay, lambarka xaqiijinta aad isticmaashay ma ahan mid sax ah. Hadii aad u aragto arintan cillad fadlan la xiriir maamulka boggan.","en":"Sorry, you have used an invalid activation number. If you think this is related to some other problem, please contact the this page's administrator."}
                return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})
    else:
        print("Sorry, no loggedin user to varify")
        print("Redirecting to login page")


def getNewLocation(request):
    if request.user.is_authenticated() and request.user.is_active():
        if registration_step > 1:
            form = LocationInfoForm(request.POST)
            allUsers = User.objects.all().count()
            if form.is_valid():
                user = request.user
                location = Profile.objects.get(user=user)

                location.current_country = request.POST.get('current_country')
                location.city_of_residence = request.POST.get('city_of_residence')
                location.region_of_birth = request.POST.get('region_of_birth')
                location.city_of_birth = request.POST.get('city_of_birth')

                location.save()
        else:
            form = LocationInfoForm()
            return render(request, 'campaign/partials/registration3.html', {'locationform':form, 'usercounter':allUsers})
    return redirect('login')



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
        "emails":["halqaran@gmail.com",],
        "phones":["+252-618-270616","+252-698-270616",],
        "websites":["halqaran.org",],
        "facebookPages":["http://facebook.com/halqaran",],
        "youtubeChannels":["http://youtube.com/halqaran",],
        "twitter":["http:twitter.com/halqaran",],
    }
    return render(request, 'campaign/partials/contacts.html',{"loginform":loginForm,"contacts":contact_info, "post":{"pk":0}})

def videos(request):
    request.session.setdefault('language','so')
    videos = Video.objects.all()
    loginForm = LoginForm()
    return render(request, 'campaign/partials/videos.html', {'videos':videos,'loginform':loginForm})

def photos(request):
    request.session.setdefault('language','so')
    photos = Image.objects.all()
    loginForm = LoginForm()
    return render(request, 'campaign/partials/photos.html', {'photos':photos,'loginform':loginForm})


def watch(request, pk):
    request.session.setdefault('language','so')

    loginForm = LoginForm()
    video = get_object_or_404(Video,videoId=pk)
    post =  post = Post.objects.filter(video_id=video.pk)
    return render(request, 'campaign/partials/watch.html',{"loginform":loginForm,"no_twitter":True,"video":video, "post":{"pk":0}})

def comments(request, status=None):
    request.session.setdefault('language','so')
    print(status)
    print("##############################")
    if request.user.is_authenticated() and request.user.is_staff:
        message = 'Comments Manager'
        if status==1:
            status = True
            message = "Approved Comments"
        elif status == None or status == 0:
            status = False
            message = "Comments Waiting Approval"
        comments = Comment.objects.filter(approved=status)
        return render(request, 'campaign/partials/comments_validation.html',{"comments":comments,"no_twitter":True, 'title':message})
    else:
        loginForm = LoginForm()
        msg = {"type":"danger","so":"Waan kaxunnahay! Uma fasaxnid inaad gasho boggan.","en":"Sorry! you don't have permission to access this page."}
        return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "status":status})

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
            loginForm = LoginForm()
            msg = {"type":"info","so":"Waad kuguuleysatay diritaanka fariintan. Waxaan jecelnahay inaan jawaab ama wax kaqabad degdega naga aragto","en":"You have successfully sent your feedback. We promise for response soon."}
            return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})
            #return JsonResponse({"feedback":feedback})
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
    post = get_object_or_404(Post, pk=pk)
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
    likes = Like.objects.filter(liked_comment_id=pk, user=request.user)
    comment = get_object_or_404(Comment, pk=pk)
    if not len(likes) > 0:
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
    if request.user.is_authenticated():
        dislikes = Dislike.objects.filter(disliked_post_id=pk, user=request.user)
    else:
        dislikes = []
    post = get_object_or_404(Post,pk=pk)
    if not len(dislikes) > 0:
        new_dislike = Dislike()
        new_dislike.disliked_post_id = pk
        if request.user.is_authenticated():
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
    comment = get_object_or_404(Comment, pk=pk)
    if not len(dislikes) > 0:
        new_dislike = Dislike()
        new_dislike.disliked_comment_id = pk
        new_dislike.user = request.user
        new_dislike.save()
        dislike_count = Dislike.objects.filter(disliked_comment_id=pk).count()
        comment.dislikes = dislike_count
        comment.save()
    return JsonResponse({"dislikes":comment.dislikes})

def approveComment(request, pk):
    if request.user.is_authenticated() and request.user.is_staff:
        comment = get_object_or_404(Comment, pk=pk)

        if not comment.approved:
            comment.approved = True
            comment.save()
            return JsonResponse({"status":True})
        return JsonResponse({"status":False})
    return JsonResponse({"status":"Sorry you don't have permission to do this."})

def unapproveComment(request, pk):
    if request.user.is_authenticated() and request.user.is_staff:
        comment = get_object_or_404(Comment, pk=pk)

        if comment.approved:
            comment.approved = False
            comment.save()
            return JsonResponse({"status":True})
        return JsonResponse({"status":False})
    return JsonResponse({"status":"Sorry you don't have permission to do this."})


def deleteComment(request, pk):
    if request.user.is_authenticated() and request.user.is_staff:
        comment = Comment.objects.filter(pk=pk).delete()
        return JsonResponse({"status":True})

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

################ SIGNALS ################
'''@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    user.is_active = False
    user.save()'''

def sendVarificationEmail(request, user, activation_code):
    subject = "Welcome to Hal Qaran"
    sender = settings.EMAIL_HOST_USER
    receiver = user.email
    site_domain = settings.SITE_DOMAIN
    url=site_domain+"/activate/"+activation_code
    ctx = {
        "user":user.first_name,
        "date":timezone.now(),
        "url":url
        }
    if request.session.get('language', 'so') == 'so':
        message = get_template('registration/so-email.html').render(Context(ctx))
    else:
        message = get_template('registration/en-email.html').render(Context(ctx))

    #send_mail(subject,message,sender,[receiver],fail_silently=False)
    msg = EmailMessage(subject, message, to=[receiver], from_email=sender)
    msg.content_subtype = 'html'
    msg.send()
    return 1

def generate_unique_code():
    return uuid.uuid4()
