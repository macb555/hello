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

    #url(r'^register$', views.RegistrationView, name='register'),

    url(r'^join$', views.register, name='join'),
    url(r'^location-registration$', views.register_location, name='register_location'),
    url(r'^location-registration/update$', views.register_location, name='register_location_update'),
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

'''
urlpatterns += [
    url(r'^register/$', RegistrationView.as_view(), name='register'),
    url(r'^register/done/$', auth_views.password_reset_done, {
        'template_name': 'registration/initial_done.html',
    }, name='register-done'),

    url(r'^register/password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {
        'template_name': 'registration/initial_confirm.html',
        'post_reset_redirect': 'accounts:register-complete',
    }, name='register-confirm'),
    url(r'^register/complete/$', auth_views.password_reset_complete, {
        'template_name': 'registration/initial_complete.html',
    }, name='register-complete'),
]
'''

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
#    urlpatterns += ['django.views.static', (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),]
