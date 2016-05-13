from django.shortcuts import render, redirect, render_to_response, get_object_or_404

# Create your views here.
def index(request):
    web = {
    'name':'JABRIL CAMPAIGN',
    'moto':"Let's build",
    }
    speeches = [
        {
            'title':"Let's build Somalia together!",
            'description': 'Mr. Jabril ephasised that we need to work together to build our Nation'
        },
        {
            'title':"Let's forget our past and build a better future!",
            'description': 'Mr. Jabril ephasised that we need to forgive one another to develop our Nation'
        },
        {
            'title':"Let's change ourselves to change our Nation!",
            'description': 'Mr. Jabril called for a change to change the situation in our Country'
        },

    ]
    return render(request, 'campaign/layout/layout.html', {'web':web, 'speeches':speeches})
