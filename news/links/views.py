# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from django.core.urlresolvers import reverse

from .forms import UserProfileForm
from .models import Vote, Link, UserProfile
# Create your views here.

class LinkListView(ListView):
	model = Link
	template_name = 'link_list.html'

	queryset = Link.with_votes.all()
	paginate_by = 3

class UserProfileDetailView(DetailView):
	model = UserProfile
	template_name = 'user_detail.html'

class UserProfileUpdateView(UpdateView):
	model = UserProfile
	form_class = UserProfileForm
	template_name = "edit_profile.html"
	success_url = '/'
