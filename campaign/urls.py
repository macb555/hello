from django.conf.urls import include, url
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^loginpage$', views.loginPage, name='loginpage'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^join$', views.register, name='join'),
    #url('^register/', CreateView.as_view(
    #        template_name='campaign/partials/registration.html',
    #        form_class=UserCreationForm,
    #        success_url='/'
    #)),
    #url('^accounts/', include('django.contrib.auth.urls')),

    url(r'^post/(?P<pk>[0-9]+)/$', views.details, name='details'),
    url(r'^issues$', views.issues, name='issues'),
    url(r'^about$', views.about, name='about'),
    url(r'^feed$', views.feed, name='feed'),
    url(r'^feedback$', views.feedback, name='feedback'),
    url(r'^faq$', views.faq, name='faq'),
    url(r'^events$', views.events, name='events'),
    url(r'^contact$', views.contact, name='contact'),

    url(r'^post/(?P<pk>[0-9]+)/like$', views.likePost, name='likePost'),
    url(r'^comment/(?P<pk>[0-9]+)/like$', views.likeComment, name='likeComment'),

    url(r'^post/(?P<pk>[0-9]+)/dislike$', views.dislikePost, name='dislikePost'),
    url(r'^comment/(?P<pk>[0-9]+)/dislike$', views.dislikeComment, name='dislikeComment'),

    url(r'^comment/(?P<post>[0-9]+)$', views.addComment, name='addComment'),
    url(r'^reply/(?P<post>[0-9]+)/(?P<parent>[0-9]+)$', views.addReply, name='addReply'),
    url(r'^watch/(?P<pk>[\w\-]+)/$', views.watch, name='watch'),

    url(r'^language/(?P<language>[a-z]{2})', views.changeLanguage, name='language'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
#    urlpatterns += ['django.views.static', (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),]
