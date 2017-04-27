from django.conf.urls import url
from django.contrib.auth.decorators import login_required as auth

from links.views import (LinkListView, 
	UserProfileDetailView, 
	UserProfileUpdateView, 
	LinkCreateView,
	LinkDetailView,)

# app_name = 'links'
urlpatterns = [
    url(r'^$', LinkListView.as_view(), name='home'),
    url(r'^users/(?P<pk>\d+)/$', UserProfileDetailView.as_view(), name='profile'),
    url(r'^update/(?P<pk>\d+)/$', auth(UserProfileUpdateView.as_view()), name='update'),
    url(r'^create/$', auth(LinkCreateView.as_view()), name='create'),
    url(r'^detail/(?P<pk>\d+)/$', LinkDetailView.as_view(), name='detail'),
]
