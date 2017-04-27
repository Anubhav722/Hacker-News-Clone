from django.conf.urls import url

from links.views import LinkListView, UserProfileDetailView
urlpatterns = [
    url(r'^$', LinkListView.as_view(), name='home'),
    url(r'^users/(?P<pk>\d+)/$', UserProfileDetailView.as_view(), name='profile')
]
