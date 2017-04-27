# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.core.urlresolvers import reverse

from .forms import UserProfileForm, LinkForm
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

class LinkCreateView(CreateView):
	model = Link
	form_class = LinkForm
	success_url = '/'
	template_name = 'link_form.html'

	def form_valid(self, form):
		f = form.save(commit=False)
		f.rank_score = 0.0
		f.submitter = self.request.user
		f.save()

		return super(CreateView, self).form_valid(form)

class LinkDetailView(DetailView):
	model = Link
	template_name = 'link_detail.html'

	# def get_object(self):
	# 	pk = self.kwargs.get('pk')
	# 	return Link.objects.get(pk=pk)
