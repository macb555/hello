from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.http import JsonResponse
from campaign.models import *
from campaign.forms import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db.models import Q, F
from django.core.mail import EmailMessage
from django.utils import timezone
from django.contrib import messages
from JABRIL import settings
import uuid

from django.template import Context
from django.template.loader import render_to_string, get_template



# Create your views here.
def index(request):
    language = request.session.setdefault('language','so')
    usercounter = User.objects.all().count()
    request.session['usercounter'] = usercounter
    if request.session.get('language') == 'so':
        pageheader = 'Hoyga'
    else:
        pageheader = 'Home'
    posts = Post.objects.filter(likes__gte=F('dislikes'),language=request.session.get('language')).exclude(category__name='About').order_by('-date_added')
    videos = Video.objects.all().order_by('-id')
    loginForm = LoginForm()
    #return render(request, 'campaign/partials/home.html', {'web':web, 'speeches':speeches, 'featured_items':speeches})
    return render(request, 'campaign/partials/home.html', {"loginform":loginForm,"featured_items":posts,"pageheader":pageheader, "latest_videos":videos})


def loginPage(request):
    if request.session.get('language') == 'so':
        pageheader = 'Bogga Gelitaanka'
    else:
        pageheader = 'Login Page'
    loginForm = LoginForm()
    return render(request, 'campaign/partials/login.html', {"nosidebarlogin":True,"loginform":loginForm,"pageheader":pageheader})

def loginPage2(request):
    username = request.session.get('username',None)
    password = request.session.get('password',None)
    loginForm = LoginForm(username=username, password=password)
    return render(request, 'campaign/partials/login.html', {"nosidebarlogin":True,"loginform":loginForm,"post":{"pk":0}})


def login(request):
    request.session.setdefault('language','so')
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            #return redirect('profile')
            msg = {'type':'info','so':"Waad ku guuleysatay gelitaanka!", 'en':'You loggedin successfully!'}
            showMessage(request, msg)
            return redirect('profile')
            #return render(request, 'campaign/partials/message.html',{"no_twitter":True,"message":msg, "profile":profile})
        else:
            loginForm = LoginForm()
            msg = {'type':'danger','so':"Waan kaxunnahay cinwaankan wili uma fasaxno adeegyada, hadii aad dooneyso riix mareegta kujirta emailka laguugu soo diray xiligi aad diiwaangelinta sameyneysay. Waana ka xunnahay in sidaan dhacdo..", 'en':'Sorry, Your account is not active. Please open the email we sent you during the registration and use the link inside.'}
            showMessage(request, msg)
            return redirect('index')
            #return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})
    else:
        posts = Post.objects.filter(language=request.session.get('language')).exclude(category__name='About').order_by('-date_added')
        videos = Video.objects.all()
        loginForm = LoginForm()
        msg = {"type":"danger","so":"Waan kaxunnahay waxaad gelisay cinwaan ama ereysireed qaldan.","en":"Sorry! Your username or password is incorrect."}
        showMessage(request, msg)
        return redirect('index')
        #return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})

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
            #user = authenticate(username=username, password=password)
            #auth_login(request, user)
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
    if request.session.get('language') == 'so':
        pageheader = 'Diiwaangelinta Adeegsadaha'
    else:
        pageheader = 'User Registration'
    if request.user.is_authenticated and request.user.is_active:
        return redirect('profile')
    language = request.session.get('language', 'so')
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
                        showMessage(request, msg)
                        return redirect('index')
                        #return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})
                    #If the username was already taken
                    elif newUser.username == username:
                        print("This username")
                        loginForm = LoginForm()
                        msg = {"type":"danger","so":"Waan ka xunnahay, magackugalkan(username-kan) horay ayaa loo diiwaangeliyay. Fadlan isku day markale adigoo adeegsanaya magackugal kale.","en":"Sorry, this username is already registered. Please use a different username and try again"}
                        showMessage(request, msg)
                        return redirect('join')
                        #return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})
                #if not, create new user and set active to false
                elif len(newUser)==0:
                    print("Your username and email are OK")
                    user = User.objects.create_user(username=username, password=password, first_name=f_name, last_name=l_name, email=email)
                    user.is_active = False
                    user.save()
                    new_user_profile = Profile.objects.create(user=user)
                    new_user_profile.activation_code = str(uuid.uuid4())
                    new_user_profile.registration_step = 1
                    new_user_profile.save()
                    request.session['waiting_user'] = user.email
                    user = authenticate(username=username, password=password)
                    #auth_login(request, user)
                    #sendVarificationEmail(request, user, new_user_profile.activation_code)
                    request.session['language']=language
                    sendWelcomeMessage(request, user, new_user_profile.activation_code)
                    #return redirect('getNewPerson')
                    #loginForm = LoginForm()
                    return redirect('verficationpage', email=user.email)
            #If the form is not valid
            print("The form is invalid")
            return render(request, 'campaign/partials/registration1.html', {'userform':form, 'usercounter':allUsers, 'pageheader':pageheader})
    #If the user requested a form
    userform=UserInfoForm()
    print("Rendering a fresh user registration form")
    return render(request, 'campaign/partials/registration1.html', {'userform':userform, 'usercounter':allUsers, 'pageheader':pageheader})

def getNewPerson(request):
    if request.session.get('language') == 'so':
        pageheader = 'Macluumaadka Shakhsiga'
    else:
        pageheader = 'Personal Info'
    request.session.setdefault('language','so')
    #check if user is loggedin.
    if request.user.is_authenticated() and request.user.is_active:
        allUsers = User.objects.all().count()
        if request.method =="POST":
            form = PersonalInfoForm(request.POST)
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
                profile.registration_step = 2

                profile.save()
                return redirect('complete-location-info')
        form = PersonalInfoForm()
        return render(request, 'campaign/partials/registration2.html', {'personalform':form, 'usercounter':allUsers, 'pageheader':pageheader})
    else:
        return redirect('login')

def verficationpage(request, email):
    if request.session.get('language') == 'so':
        pageheader = 'Bogga Xaqiijinta'
    else:
        pageheader = 'Verification Page'
    if request.user.is_authenticated and request.user.is_active:
        return redirect('profile')
    if request.method == 'POST':
        print("User sent some data")
        form = VerficationForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=email)
            if not len(user) ==0:
                print("Redirectin to Verification page")
                user = user[0]
                #return redirect('varifyUser', pk=user.pk, activation_code=request.POST.get('verification_code'))
                print("The data is valid")
                if user.profile.activation_code == request.POST.get('verification_code'):
                    print("The activation code in the data is correct")
                    user.is_active = True
                    user.profile.registration_step = 1
                    user.save()
                    request.session['username']=user.username
                    request.session['password']=user.password
                    print("successfully activated")
                    print("Redirecting to loginpage view.")
                    return redirect('loginpage')
                print("The activation code is not correct")
        print("User didn't give a valid data")
        return render(request, 'campaign/partials/verficationpage.html', {'verificationform':form, 'pageheader':pageheader})
    print("Sending a fresh form")
    form = VerficationForm()
    return render(request, 'campaign/partials/verficationpage.html', {'verificationform':form,'pageheader':pageheader})

def directverficationpage(request, email, activation_code):
    if request.session.get('language') == 'so':
        pageheader = 'Bogga Xaqiijinta'
    else:
        pageheader = 'Verification Page'
    if request.user.is_authenticated and request.user.is_active:
        return redirect('profile')
    print("+++++++++++++++++++++++++++++++++++++ VERIFICATION ++++++++++++++++++++++++++++++")
    print("Email", email)
    print("Activation: #",activation_code)

    print("User sent some data")
    user = User.objects.filter(email=email)
    if not len(user) ==0:
        print("Redirectin to Verification page")
        user = user[0]
        #return redirect('varifyUser', pk=user.pk, activation_code=request.POST.get('verification_code'))
        print("The data is valid")
        if user.profile.activation_code == activation_code:
            print("The activation code in the data is correct")
            user.is_active = True
            user.profile.registration_step = 1
            user.save()
            #request.session['username']=user.username
            #request.session['password']=user.password
            print("successfully activated")
            print("Redirecting to loginpage view.")
            msg = {"type":"info","so":"Guul! Xaqiijinti waad ku guuleysatay. Ku gal aqoonsigaaga.","en":"Congradulations! Activation Succeeded. Login using your cridentials."}
            showMessage(request, msg)
            return redirect('loginpage')
    msg = {"type":"danger", "en":"Sorry, Make sure the varification code you used is correct.", "so":"Waan kaxunnahay, Fadlan iska hubi qoraalsireedka aad gelisay."}
    showMessage(request, msg)
    return render(request, 'campaign/partials/verficationpage.html', {'verificationform':form,'pageheader':pageheader})
    #print("Sending a fresh form")
    #form = VerficationForm()
    #return render(request, 'campaign/partials/verficationpage.html', {'verificationform':form})


def varifyUser(request, pk, activation_code):
    if request.user.is_authenticated and request.user.is_active:
        return redirect('profile')
    if not request.user.is_authenticated():
        print("Varifying user", pk)
        user = User.objects.filter(id=pk)
        print("USER:",user)
        if not len(user)==0:
            print("Got user")
            form = VerficationForm(request.POST)
            if form.is_valid():
                if user[0].is_active:
                    print("But this user was already activated")
                    return redirect('index')
                else:
                    print("And this user is not yet activated")
                    if str(user[0].profile.activation_code) == str(activation_code):
                        print("Your serial no is correct")
                        user[0].is_active = True
                        user[0].save()
                        user[0].profile.registration_step = 1
                        user[0].profile.save()
                        print("User activated!")
                        #activated_user = authenticate(username=user[0].username, password=user[0].password)
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                        #print(activated_user)
                        #auth_login(request, activated_user)
                        #return redirect('loguserin', email=user[0].email)
                        msg = {"type":"info","so":"Waad ku guuleystay xaqiijinta email-kaaga. Fadlan adeegso magackugalkaaga(username) iyo ereysireedkaaga(password) si aad u gasho.","en":"You've successfully verified your email. Please use your username and password to login."}
                        showMessage(request, msg)
                        return redirect(reverse('loguserin',kwargs={'email':user[0].email}))
                    else:
                        print("Activation code is incorrect")
                        loginForm = LoginForm()
                        msg = {"type":"danger","so":"Waan ka xunnahay, lambarka xaqiijinta aad isticmaashay ma ahan mid sax ah. Hadii aad u aragto arintan cillad fadlan la xiriir maamulka boggan.","en":"Sorry, you have used an invalid activation number. If you think this is related to some other problem, please contact the this page's administrator."}
                        showMessage(request, msg)
                        #return redirect(reverse('verficationpage',kwargs={'email':user[0].email}))
                        return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})
            print("Didnt't provide a valid form")
        print("Didn't get any user with this id")
        loginForm = LoginForm()
        msg = {"type":"danger","so":"Waan ka xunnahay, aqoonsiga qofka aad soo dalbatay ma ahan mid jira.","en":"Sorry, The id number for this user is invalid."}
        showMessage(request, msg)
        return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})


def getNewLocation(request):
    if request.session.get('language') == 'so':
        pageheader = 'Macluumaadka Goobta'
    else:
        pageheader = 'Location Info'
    allUsers = User.objects.all().count()
    print("Gettin new location form")
    if request.user.is_authenticated() and request.user.is_active:
        print("User is logged in")
        if request.user.profile.registration_step == 2:
            print("User is in the second step")
            form = LocationInfoForm(request.POST)

            if form.is_valid():
                print("User gave a valid data")
                user = request.user
                location = Profile.objects.get(user=user)

                location.current_country = request.POST.get('current_country')
                location.city_of_residence = request.POST.get('city_of_residence')
                location.region_of_birth = request.POST.get('region_of_birth')
                location.city_of_birth = request.POST.get('city_of_birth')

                location.registration_step = 3
                location.save()
                msg = {"type":"info","so":"Hambalyo! Waad ku guuleystay diiwaangelinta.","en":"Congradulations! You have successfully completed registration."}
                showMessage(request, msg)
                return redirect('index')

            else:
                print("return to the same form because the step is not the second.")
                form = LocationInfoForm()
                return render(request, 'campaign/partials/registration3.html', {'locationform':form, 'usercounter':allUsers, 'pageheader':pageheader})
    print("user is not logged in or is not active")
    return redirect('profile')



def logout(request):
    language = request.session.get('language', 'so')
    auth_logout(request)
    loginForm = LoginForm()
    request.session['language']=language
    msg = {"type":"info","so":"Waad kuguuleysatay kabixitaanka.","en":"You have successfully logged out."}
    showMessage(request, msg)
    return redirect('index')
    #return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})
def details(request, pk):
    if request.session.get('language') == 'so':
        pageheader = 'Faafaahinta'
    else:
        pageheader = 'Details'
    loginForm = LoginForm()
    post = get_object_or_404(Post, pk=pk)
    post.view_counter += 1
    post.save()
    post_comments = Comment.objects.filter(post=pk, approved=True)
    #posts = Post.objects.all()
    form = CommentForm()
    return render(request, 'campaign/partials/details.html',{"loginform":loginForm,"post":post, "latest_posts":"posts", "post_comments":post_comments,"form":form, 'pageheader':pageheader})

def contact(request):
    if request.session.get('language') == 'so':
        pageheader = 'Nala Soo Xiriir'
    else:
        pageheader = 'Contact us'
    loginForm = LoginForm()
    contact_info = {
        "emails":["welcome@halqaran.org","info@halqaran.org"],
        "phones":["+252-61-9011268","+252-69-9007551"],
        "websites":["halqaran.org",],
        "facebookPages":["https://www.facebook.com/profile.php?id=100012631158342&ref=br_rs",],
        "youtubeChannels":["https://www.youtube.com/channel/UCcAKBo1Ll35bIuyHZIc6EQA",],
        "twitter":["https://twitter.com/halqaran_info",],
    }
    return render(request, 'campaign/partials/contacts.html',{"loginform":loginForm,"contacts":contact_info, "pageheader":pageheader})

def videos(request):
    if request.session.get('language') == 'so':
        pageheader = 'Muuqaalada'
    else:
        pageheader = 'Videos'
    request.session.setdefault('language','so')
    videos = Video.objects.all().order_by("-id")
    loginForm = LoginForm()
    return render(request, 'campaign/partials/videos.html', {'videos':videos,'loginform':loginForm,'pageheader':pageheader})

def photos(request):
    if request.session.get('language') == 'so':
        pageheader = 'Sawirrada'
    else:
        pageheader = 'Photos'
    request.session.setdefault('language','so')
    photos = Image.objects.all().order_by("-id")
    loginForm = LoginForm()
    return render(request, 'campaign/partials/photos.html', {'photos':photos,'loginform':loginForm, 'pageheader':pageheader})


def watch(request, pk):
    if request.session.get('language') == 'so':
        pageheader = 'Daawo'
    else:
        pageheader = 'Watch'
    request.session.setdefault('language','so')

    loginForm = LoginForm()
    video = get_object_or_404(Video,videoId=pk)
    post =  post = Post.objects.filter(video_id=video.pk)
    return render(request, 'campaign/partials/watch.html',{"loginform":loginForm,"no_twitter":True,"video":video, "pageheader":pageheader})

def comments(request, status=None):
    if request.session.get('language') == 'so':
        pageheader = 'Artiyada Bulshada'
    else:
        pageheader = 'User Comments'
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
        showMessage(request, msg)
        return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "status":status, 'pageheader':pageheader})

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
    if request.session.get('language') == 'so':
        pageheader = 'Warbixinada'
    else:
        pageheader = 'Feed'
    loginForm = LoginForm()
    posts = Post.objects.filter(language=request.session.get('language')).exclude(category__name='About').order_by('-date_added')
    return render(request, 'campaign/partials/feeds.html',{"loginform":loginForm,"posts":posts, "pageheader":pageheader})

def feedback(request):
    request.session.setdefault('language','so')
    if request.session.get('language') == 'so':
        pageheader = 'Warcelin'
    else:
        pageheader = 'Feedback'
    loginForm = LoginForm()
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            loginForm = LoginForm()
            msg = {"type":"info","so":"Waad kuguuleysatay diritaanka fariintan. Waxaan jecelnahay inaan jawaab ama wax kaqabad degdega naga aragto","en":"You have successfully sent your feedback. We promise for response soon."}
            showMessage(request, msg)
            return redirect('index')
            #return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})
            #return JsonResponse({"feedback":feedback})
    else:
        form = FeedbackForm()
        return render(request, 'campaign/partials/feedback.html',{"loginform":loginForm,'form':form, "pageheader":pageheader})


def events(request):
    if request.session.get('language') == 'so':
        pageheader = 'Dhacdooyinka iyo Munaasabadaha'
    else:
        pageheader = 'Events'
    loginForm = LoginForm()
    posts = Post.objects.filter(category__name="Events",language=request.session.get('language')).exclude(category__name='About').order_by('-date_added')
    return render(request, 'campaign/partials/events.html',{"loginform":loginForm,"posts":posts, "pageheader":pageheader})

def about(request):
    if request.session.get('language') == 'so':
        pageheader = 'Ku Saabsan '+str(settings.SITE_NAME.get('so'))
    else:
        pageheader = 'Feed'
    loginForm = LoginForm()
    posts = Post.objects.filter(category__name="About", language=request.session.get('language'))
    if posts:
        posts = posts[0]
    return render(request, 'campaign/partials/about.html',{"loginform":loginForm,"post":posts, 'pageheader':pageheader})

def issues(request):
    if request.session.get('language') == 'so':
        pageheader = 'Arimaha'
    else:
        pageheader = 'Issues'
    loginForm = LoginForm()
    #posts = get_object_or_404(Post, category__name="issues")
    posts = Post.objects.filter(category__name="Issues",language=request.session.get('language')).exclude(category__name='About').order_by('-date_added')
    return render(request, 'campaign/partials/issues.html',{"loginform":loginForm,"posts":posts, "pageheader":pageheader})

def faq(request):
    if request.session.get('language') == 'so':
        pageheader = "Su'aalaha Badanaa La is Weydiiyo"
    else:
        pageheader = 'Frequently Asked Questions'
    loginForm = LoginForm()
    posts = get_object_or_404(Post, category__name="faq")
    return render(request, 'campaign/partials/details.html',{"loginform":loginForm,"post":posts, 'pageheader':pageheader})


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
        try:
            comment = Comment.objects.filter(pk=pk).delete()
        except:pass
        return JsonResponse({"status":True})

def AmIIn(request):
    return JsonResponse({"status":user.is_authenticated()})

def changeLanguage(request, language):
    redirect_to = request.POST.get('next', request.GET.get('next', '/'))
    if language == 'so' or language == 'en':
        request.session["language"] = language
        loginForm = LoginForm()
        msg = {'type':'info','so':"Waad ku guuleysatay bedelidda luqadda.", 'en':'You have successfully changed the language.'}
        showMessage(request, msg)
        return redirect(redirect_to)
        #return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})
    else:
        request.session.setdefault('language','so')
        loginForm = LoginForm()
        msg = {'type':'danger','so':"Waan kaxunnahay luqadda aad dooratay wili ma aanan kusoo derin boggeena.", 'en':"Sorry, we didn't add this language yet."}
        showMessage(request, msg)
        return redirect(redirect_to)
        #return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})

################ PURE PYTHON FUNCTIONS ##################
def getLanguage(request):
    current_language = request.session.get('language','so')
    if current_language == 'so':
        return current_language
    else:
        return 'en'

################ SIGNALS ################
'''@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    user.is_active = False
    user.save()'''

def sendWelcomeMessage(request, user, activation_code):
    sender = settings.EMAIL_HOST_USER
    receiver = user.email
    link = settings.SITE_DOMAIN + '/verfication/' +str(receiver)+'/'+ str(activation_code)
    content = """
    <html>
    <head>
    </head>
    <body>
    [Somali]
    <h1>Haye {name}</h1>
    Kusoo dhawoow Hal Qaran, waad ku mahadsan tahay kusoo biiritaankaaga.</br>
    <p>Fadlan <a  name='confirmation' href="{url}">riix halkan</a> si aad diiwaangelinta u dhameystirto.<br/>
    ama adeegso qoraalsireedkan: <b>{code}</b>
    </p>
    <p><b>FG:</b> Waxaan fariintan kuugu soo dirnay in aan hubinno in cinwaankan aad adiga leedahay. Hadii uu qof kale isku dayayo inuu adeegsado cinwaankaaga,
    Haka walwalin, uma fasixi doono inuu u adeegsado, hadii aadan mareegta [link] kore aadan riixin.</p>
    <p>Waad ku mahadsan tahay daneynta dib u dhiska dalkaaga.</p>
    <hr/>
    [English]
    <h1>Hello {name}</h1>
    Welcome to Hal Qaran, thanks for joining us.</br>
    <p>Please <span><a  name=\'confirmation\' href=\'{url}\'>click here</a></span> to complete your registration.<br/>
    or use this code: <b>{code}</b>
    </p>
    <p><b>NB:</b> We have sent you this email to confirm that it is you who
    used your email addres to register with Hal Qaran. If someone else
    is trying to use your email, just ignore this message because they will not be able to
    complete their registration.</p>
    <p>Thanks for your interest in our effort to rebuild Somalia.</p>
    </body>
    </html>
    """.format(name=user.first_name, url=link, code=activation_code)
    from welcome import Welcome
    w = Welcome()
    try:
        w.login()
        return w.send(subject="Kusoo Dhawoow Hal Qaran | Welcome to Hal Qaran", to=user.email, content=content, isHtml=True)
    except:
        return False


def sendVarificationEmail(request, user, activation_code):
    print("Sending email to", user.email)
    subject = "Welcome to Hal Qaran"
    sender = settings.EMAIL_HOST_USER
    receiver = user.email
    link = settings.SITE_DOMAIN + '/verfication/' +str(receiver)+'/'+ str(activation_code)
    #http://localhost:8000/verfication/boolow5@gmail.com/12d6de94-86b9-494a-8626-cde95bdd25c4
    ctx = {
        "user":user.first_name,
        "date":timezone.now(),
        "link":link
        }
    if request.session.get('language', 'so') == 'so':
        message = get_template('registration/so-email.html').render(Context(ctx))
    else:
        message = get_template('registration/en-email.html').render(Context(ctx))

    #send_mail(subject,message,sender,[receiver],fail_silently=False)
    try:
        print("Please wait...")
        msg = EmailMessage(subject, message, to=[receiver], from_email=sender)
        msg.content_subtype = 'html'
        print("Setting the email type to HTML")
        msg.send()
        print("SENT!")
    except Exception as e:
        print(e)
    return 1



def resendVarificationCode(request, email):
    if request.session.get('language') == 'so':
        pageheader = 'Xaqiijinta Markale Iso Dir'
    else:
        pageheader = 'Resend Verification'
    try:
        user = User.objects.filter(email=email)
        if not len(user) == 0:
            #got user
            profile = Profile.objects.get(user=user[0])
            sendVarificationEmail(request, user[0], profile.activation_code)
            loginForm = LoginForm()
            msg = {
                'type':'info',
                'so':"Lambarka xaqiijinta markale ayaa laguu soo diray. Hadii aad weyso wax fariin ah waxa ay macnaheedu noqoneysaa in email-kaaga aadan si sax ah u gelin. Hadii aad arintan cillad u aragto fadlan nala soo socodsii, anagaa kaa caawin doonno furitaanka adeegaaga.",
                'en':'You activation code is resent to your email. If you don\'t get this email it means your email was not correct. If you think this another error, please contact us to help you activate your account.'
                }
            showMessage(request, msg)
            return render(request, 'campaign/partials/message.html',{"no_twitter":True,"message":msg, "loginform":loginForm, 'pageheader':pageheader})
        else:
            loginForm = LoginForm()
            msg = {
                'type':'info',
                'so':"Waan ka xunnahay email-ka aad gelisay majirto qof ku diiwaansan. Fadlan iska hubi oo markale ku celi.",
                'en':'Sorry, this email does\'t belong to any of our users. Please make sure you have written the correct email and try again.'
                }
            showMessage(request, msg)
            return render(request, 'campaign/partials/message.html',{"no_twitter":True,"message":msg, "loginform":loginForm, 'pageheader':pageheader})
    except:
        loginForm = LoginForm()
        msg = {
            'type':'info',
            'so':"Waan ka xunnahay kuma guuleysan in aad dib u dirto xaqiijinta. Fadlan markale isku day.",
            'en':'Sorry, there was a problem sending your verification message. Please try again.'
            }
        showMessage(request, msg)
        return redirect('index')
        #return render(request, 'campaign/partials/message.html',{"no_twitter":True,"message":msg, "loginform":loginForm})

def generate_unique_code():
    return uuid.uuid4()
def loguserin(request, email=None):
    if email is not None:
        user = User.objects.filter(email=email)
        if len(user)!=0:
            user = user[0]
    else:
        return redirect('loginpage')
    username = user.username
    password = user.password
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            redirect('getNewPerson')
        else:
            loginForm = LoginForm(username=username, password=password)
            msg = {'type':'danger','so':"Waan kaxunnahay cinwaankan wili uma fasaxno adeegyada, hadii aad dooneyso riix mareegta kujirta emailka laguugu soo diray xiligi aad diiwaangelinta sameyneysay. Waana ka xunnahay in sidaan dhacdo..", 'en':'Sorry, Your account is not active. Please open the email we sent you during the registration and use the link inside.'}
            showMessage(request, msg)
            return redirect('index')
            #return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})
    else:
        posts = Post.objects.filter(language=request.session.get('language')).exclude(category__name='About').order_by('-date_added')
        videos = Video.objects.all()
        loginForm = LoginForm()
        msg = {"type":"danger","so":"Waan kaxunnahay waxaad gelisay cinwaan ama ereysireed qaldan.","en":"Sorry! Your username or password is incorrect."}
        showMessage(request, msg)
        return redirect('index')
        #return render(request, 'campaign/partials/message.html',{"loginform":loginForm, "no_twitter":True,"message":msg, "post":{"pk":0}})

def profile(request):
    if request.session.get('language') == 'so':
        pageheader = 'Macluumaadkaaga'
    else:
        pageheader = 'Your Profile'
    if request.user.is_authenticated() and request.user.is_active:
        print("user is logged in")
        #user is active and logged in
        profile = Profile.objects.filter(user = request.user)
        if len(profile)!=0:
            print("got the profile")
            profile = profile[0]
            print("profile step", profile.registration_step)
            if profile.registration_step == 1:
                print("user is in the first step of registration")
                #take user to registration step 2
                return redirect('getNewPerson')
            elif profile.registration_step == 2:
                print("user is in the second step of registration")
                #take user to last step registration
                return redirect('complete-location-info')
        return render(request, 'campaign/partials/profile.html', {'profile':profile, 'pageheader':pageheader})
            #    #show profile
            #return redirect('getNewPerson')
            #    return render(request, 'campaign/partials/profile.html', {'profile':profile})
    else:
        return redirect('loginpage')

def showMessage(request, msg={}):
    try:
        if msg is not None:
            language = request.session.get("language", None)
            if language =="so":
                if msg['type']=='info':
                    messages.add_message(request, messages.SUCCESS, msg['so'])
                elif msg['type']=='danger':
                    messages.add_message(request, messages.ERROR, msg['so'])
                else:
                    messages.add_message(request, messages.INFO, msg['so'])
            else:
                if msg['type']=='info':
                    messages.add_message(request, messages.SUCCESS, msg['en'])
                elif msg['type']=='danger':
                    messages.add_message(request, messages.ERROR, msg['en'])
                else:
                    messages.add_message(request, messages.INFO, msg['en'])
    except:
        pass
    finally:
        return 1

def forgotpassword(request):
    if request.session.get('language') == 'so':
        pageheader = 'Ereysireedki Ayaan Ilaaway'
    else:
        pageheader = 'I Forgot My Password'
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("Sorry you forgot your password")
    if not request.user.is_authenticated():
        if request.method == "POST":
            print("You sent some data")
            form = ForgotPasswordForm(request.POST)
            if form.is_valid():
                print("The data is valid")
                user = User.objects.filter(email=request.POST.get('email'))
                if not len(user) ==0:
                    print("Got user with this email")
                    profile = user[0].profile
                    profile.activation_code = str(uuid.uuid4())
                    profile.save()
                    print("Generated a new code for this user")
                    print("Redirecting to SEND PASSWORD RESET VIEW")
                    return redirect('sendPasswordReset', email=request.POST.get('email'))
                msg = {'type':'danger','so':"Waan ka xunnahay majirto cid email-kan ku diiwaansan.", 'en':'Sorry there is no one registered with this email.'}
                showMessage(request, msg)
                print("There is no user with this email")
                return redirect('index')
            print("The data is invalid")
        form = ForgotPasswordForm()
        print("Sending a fresh Fortgot Password Form")
        return render(request, 'campaign/partials/forgotpassword.html', {'forgotpasswordform':form, 'pageheader':pageheader})
    msg = {'type':'danger','so':"Waxaaba kuu furan cinwaankaaga.", 'en':'You are already loged in.'}
    showMessage(request, msg)
    print("You are already logged in")
    return redirect('index')

def resetPassword(request, email, activation_code):
    if request.session.get('language') == 'so':
        pageheader = 'Ereysireedka Iga Bedel'
    else:
        pageheader = 'Reset My Password'
    user = User.objects.filter(email=email)
    if not len(user) ==0:
        profile = user[0].profile
        if profile.activation_code == activation_code:
            new_password = request.POST.get('password1')
            user[0].set_password(new_password)
            user[0].save()
            msg = {'type':'info','so':"Ereysireedkaaga (password) waa la bedelay. Fadlan midka cusub ku gal hada.", 'en':'Your password has been changed. Please login using your new password.'}
            showMessage(request, msg)
        msg = {'type':'danger','so':"Waan kaxunnahay, ereysireedkaaga (password) lama bedelin. iska hubi in mareegta (link) aad soo raacday ay tahay sida email-kaaga aan kugu soo dirnay.", 'en':'Sorry, your password didn\'t change. Please make sure the link is the same as the one we sent you through your email.'}
        showMessage(request, msg)
        return redirect('index')
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=email)
            if not len(user) ==0:
                profile = user[0].profile
                if profile.activation_code == activation_code:
                    new_password = request.POST.get('password1')
                    user[0].set_password(new_password)
                    user[0].save()
                    msg = {'type':'info','so':"Ereysireedkaaga (password) waa la bedelay. Fadlan midka cusub ku gal hada.", 'en':'Your password has been changed. Please login using your new password.'}
                    showMessage(request, msg)
                msg = {'type':'danger','so':"Waan kaxunnahay, ereysireedkaaga (password) lama bedelin. iska hubi in mareegta (link) aad soo raacday ay tahay sida email-kaaga aan kugu soo dirnay.", 'en':'Sorry, your password didn\'t change. Please make sure the link is the same as the one we sent you through your email.'}
                showMessage(request, msg)
                #return redirect('resetPassword', email=request.POST.get('email'))
    form = ResetPasswordForm()
    return render(request, 'campaign/partials/resetpassword.html', {'resetpasswordform':form, 'pageheader':pageheader})

def sendPasswordReset(request, email):
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("in SEND PASSWORD RESET VIEW")
    #try:
    user = User.objects.filter(email=email)
    if not len(user) ==0:
        #generate key
        print("There is user with this email")
        profile = user[0].profile
        profile.activation_code = str(uuid.uuid4())
        profile.save()
        sendPasswordResetEmail(request, user[0], profile.activation_code)
        msg = {'type':'info','so':"Mareegti aad u adeegsan laheyd bedelidda ereysireedkaaga waxaa loo diray email-kaaga. Fadlan raac mareegtaas si aad u bedesho ereysireedka", 'en':'A link for resetting your password is sent to your email. Please follow that link to reset your password.'}
        showMessage(request, msg)
    #except:pass
    print("Redirecting to home page")
    return redirect('index')
    '''
    if request.method == "POST":
        print("Got some data")
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            print("Data is valid")
            user = User.objects.filter(email=email)
            if not len(user) ==0:
                #generate key
                print("There is user with this email")
                profile = user[0].profile
                profile.activation_code = str(uuid.uuid4())
                profile.save()
                #send email
                print("Generated a new code")
                print("Sending an email")
                sendPasswordEmail(request, user[0], profile.activation_code)
                print("Sent an email")
                #return to home and tell user to wait for email
                msg = {'type':'info','so':"Mareegti aad u adeegsan laheyd bedelidda ereysireedkaaga waxaa loo diray email-kaaga. Fadlan raac mareegtaas si aad u bedesho ereysireedka", 'en':'A link for resetting your password is sent to your email. Please follow that link to reset your password.'}
                showMessage(request, msg)
                print("Redirecting to home page")
                #return redirect('sendPasswordEmail', email=email, activation_code=profile.activation_code)
                return redirect('index')
        return render(request, 'campaign/partials/forgotpassword.html', {'forgotpasswordform':form})'''
    #form = ForgotPasswordForm()
    #return render(request, 'campaign/partials/forgotpassword.html', {'forgotpasswordform':form})


def sendPasswordEmail(request, user, activation_code):
    print("PASSWORD RESET EMAIL VIEW")
    subject = "Welcome to Hal Qaran"
    sender = settings.EMAIL_HOST_USER
    receiver = user.email
    link = settings.SITE_DOMAIN + '/reset/' +str(receiver)+'/'+ str(activation_code)
    #http://localhost:8000/verfication/boolow5@gmail.com/12d6de94-86b9-494a-8626-cde95bdd25c4
    ctx = {
        "user":user.first_name,
        "date":timezone.now(),
        "link":link
        }
    if request.session.get('language', 'so') == 'so':
        message = get_template('registration/so-reset-email.html').render(ctx)
    else:
        message = get_template('registration/en-reset-email.html').render(ctx)

    #send_mail(subject,message,sender,[receiver],fail_silently=False)
    #try:
    msg = EmailMessage(subject, message, to=[receiver], from_email=sender)
    msg.content_subtype = 'html'
    msg.send()
    print("SENT EMAIL")
    #except:pass

    return 1

def sendPasswordResetEmail(request, user, activation_code):
    print("PASSWORD RESET EMAIL VIEW")
    subject = "Welcome to Hal Qaran"
    sender = settings.EMAIL_HOST_USER
    receiver = user.email
    link = settings.SITE_DOMAIN + '/reset/' +str(receiver)+'/'+ str(activation_code)
    content = """
    <html>
    <head>
    </head>

    <h1>Hello {name}</h1>
    <p>Welcome to <strong>Hal Qaran</strong>, we are sorry that you forgot your password.</p>
    <p>but don't worry we have your back. below is the link to reset your password.</p>
    <p>Link: <strong><a href='{url}'  name='confirmation' id='confirm-code'>{url}</a></strong></p>
    <p>Activation Code: <b>{code}</b></p>
    <hr/>
    <p>Thanks for supporting</p>

    <h1>Haye {name}</h1>
    <p>Kusoo dhawoow <strong>Hal Qaran</strong>, waan ka xunnahay inaad ilowdo ereysireedkaaga.</p>
    <p>Balse ha walwalin anagaa halkan kuu joogna, waxaan hoos kuugu soo dirnay mareegta (link) aad ku cusbooneysiisan laheyd ereysireedkaaga.</p>
    <p>Mareegta: <strong><a href='{url}'  name='confirmation' id='confirm-code'>{url}</a></strong></p>
    <p>Qoraal Sireedka: <b>{code}</b></p>
    <hr/>
    <p>Waad Ku Mahadsantahay in aad nala jirto</p>

    </body>
    </html>
    """.format(name=user.first_name, url=link, code=activation_code)
    from welcome import Welcome
    w = Welcome()
    try:
        w.login()
        return w.send(subject="Cusbooneysiinta Ereysireedka | Password Reset", to=user.email, content=content, isHtml=True)
    except:
        return False
