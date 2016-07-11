from django.conf.urls import include, url
from . import views
from django.conf import settings
from django.conf.urls.static import static


#from .views import RegistrationView
from django.contrib.auth import views as auth_views


from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm


urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^loginpage$', views.loginPage, name='loginpage'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^manage/comments$', views.comments, name='comments'),
    url(r'^manage/comments/(?P<status>[0-9]+)$', views.comments, name='comments'),

    url(r'^join$', views.register, name='join'),
    url(r'^profile-registration$', views.register_profile, name='register_profile'),
    url(r'^profile-registration/update$', views.register_profile, name='register_profile_update'),

    url(r'^post/(?P<pk>[0-9]+)/$', views.details, name='details'),
    url(r'^issues$', views.issues, name='issues'),
    url(r'^about$', views.about, name='about'),
    url(r'^feed$', views.feed, name='feed'),
    url(r'^feedback$', views.feedback, name='feedback'),
    url(r'^faq$', views.faq, name='faq'),
    url(r'^events$', views.events, name='events'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^videos$', views.videos, name='videos'),
    url(r'^photos$', views.photos, name='photos'),

    url(r'^post/(?P<pk>[0-9]+)/like$', views.likePost, name='likePost'),
    url(r'^comment/(?P<pk>[0-9]+)/like$', views.likeComment, name='likeComment'),

    url(r'^comment/(?P<pk>[0-9]+)/approve$', views.approveComment, name='approveComment'),
    url(r'^comment/(?P<pk>[0-9]+)/unapprove$', views.unapproveComment, name='unapproveComment'),
    url(r'^comment/(?P<pk>[0-9]+)/delete$', views.deleteComment, name='deleteComment'),

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
