from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.details, name='details'),
    url(r'^issues$', views.issues, name='issues'),
    url(r'^bio$', views.bio, name='bio'),
    url(r'^feed$', views.feed, name='feed'),
    url(r'^feedback$', views.feed, name='feedback'),
    url(r'^faq$', views.faq, name='faq'),
    url(r'^events$', views.events, name='events'),
    url(r'^contacts$', views.contacts, name='contacts'),
    url(r'^post/(?P<pk>[0-9]+)/like$', views.likePost, name='likePost'),
    url(r'^comment/(?P<pk>[0-9]+)/like$', views.likeComment, name='likeComment'),
]
