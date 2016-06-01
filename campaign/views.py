from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.http import JsonResponse
from campaign.models import *
# Create your views here.
def index(request):
    posts = Post.objects.all()

    web = {
    'topbanner':'New down for Somalia',
    'name':'JABRIL CAMPAIGN',
    'moto':"Let's build",
    }

    speeches = [
        {
            'title':"Let's change ourselves to change our Nation!",
            'description': 'Mr. Jabril called for a change to make the situation in our Country better.',
            'image':'/static/campaign/images/3.jpg',
            'slider':'/static/campaign/images/slide-3.jpg',
        },
        {
            'title':"Let's build Somalia together!",
            'description': 'Mr. Jabril ephasised that we need to work together to build our Nation',
            'image':'/static/campaign/images/1.jpg',
            'slider':'/static/campaign/images/slide-1.jpg',
        },
        {
            'title':"Let's forget our past and build a better future!",
            'description': 'Mr. Jabril emphasised that we need to forgive one another to develop our Nation',
            'image':'/static/campaign/images/2.jpg',
            'slider':'/static/campaign/images/slide-2.jpg',
        },


    ]
    #return render(request, 'campaign/partials/home.html', {'web':web, 'speeches':speeches, 'featured_items':speeches})
    return render(request, 'campaign/partials/home.html', {'web':web, "featured_items":posts})

def details(request, pk):
    post = {
        "pk":1,
        "title":"Mowduuc Tijaabo ah oo Booscelis ahaan halkan loo dhigay!",
        "date":"30/05/2016",
        "author":"Mahdi Bolow",
        "likes":"15",
        "video":{"videoId":"yNYJG3WFPak"},
        "description":"Waa warbixin tijaabo ah oo loogu talagalay in lagu saxo muuqaalka warbixinada soo socda",
        "content":"Waa warbixin tijaabo ah oo loogu talagalay in lagu saxo muuqaalka warbixinada soo socda. Waa warbixin tijaabo ah oo loogu talagalay in lagu saxo muuqaalka warbixinada soo socda. Waa warbixin tijaabo ah oo loogu talagalay in lagu saxo muuqaalka warbixinada soo socda. Waa warbixin tijaabo ah oo loogu talagalay in lagu saxo muuqaalka warbixinada soo socda. Waa warbixin tijaabo ah oo loogu talagalay in lagu saxo muuqaalka warbixinada soo socda. ",
        "comments":[{
            "pk":1,
            "text":"Waa comment tijaabo ahaan aan usoo geliyay si loo arko sida comments-ka ay usoo bixi doonaan marka aqristayaasha ay soo geliyaan",
            "date":"31/05/2016",
            "likes":"9",
            "user":"Mahdi Bolow"
        },{
            "pk":2,
            "text":"Waa comment tijaabo ahaan aan usoo geliyay si loo arko sida comments-ka ay usoo bixi doonaan marka aqristayaasha ay soo geliyaan",
            "date":"31/05/2016",
            "likes":"9",
            "user":"Mahdi Bolow"
        },{
            "pk":3,
            "text":"Waa comment tijaabo ahaan aan usoo geliyay si loo arko sida comments-ka ay usoo bixi doonaan marka aqristayaasha ay soo geliyaan",
            "date":"31/05/2016",
            "likes":"9",
            "user":"Mahdi Bolow"
        },{
            "pk":4,
            "text":"Waa comment tijaabo ahaan aan usoo geliyay si loo arko sida comments-ka ay usoo bixi doonaan marka aqristayaasha ay soo geliyaan",
            "date":"31/05/2016",
            "likes":"9",
            "user":"Mahdi Bolow"
        },]
    }
    return render(request, 'campaign/partials/details.html',{"post":post, "id":pk})

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
    data = {"status":True, "likes":20, "id":pk}
    return JsonResponse(data)

def likeComment(request, pk):
    data = {"status":True, "likes":20, "id":pk}
    return JsonResponse(data)
