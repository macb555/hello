from django.conf.urls import include, url
from . import views
from JABRIL import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.details, name='details'),
    url(r'^issues$', views.issues, name='issues'),
    url(r'^bio$', views.bio, name='bio'),
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
]

#if settings.DEBUG:
#    urlpatterns += ['django.views.static', (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),]
