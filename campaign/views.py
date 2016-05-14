from django.shortcuts import render, redirect, render_to_response, get_object_or_404

# Create your views here.
def index(request):
    web = {
    'topbanner':'New down for Somalia',
    'name':'JABRIL CAMPAIGN',
    'moto':"Let's build",
    }

    speeches = [
        {
            'title':"Let's change ourselves to change our Nation!",
            'description': 'Mr. Jabril called for a change to change the situation in our Country',
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
            'description': 'Mr. Jabril ephasised that we need to forgive one another to develop our Nation',
            'image':'/static/campaign/images/2.jpg',
            'slider':'/static/campaign/images/slide-2.jpg',
        },


    ]
    return render(request, 'campaign/index.html', {'web':web, 'speeches':speeches, 'featured_items':speeches})
