# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import (ListView, 
	DetailView, 
	UpdateView, 
	CreateView,
	DeleteView,)

from django.core.urlresolvers import reverse, reverse_lazy

from django_comments.models import Comment

from .forms import UserProfileForm, LinkForm
from .models import Vote, Link, UserProfile
# Create your views here.

class RandomGossipMixin(object):
	def get_context_data(self, **kwargs):
		context = super(RandomGossipMixin, self).get_context_data(**kwargs)
		context[u'randomquip'] = Comment.objects.order_by('?')[0]
		return context

class LinkListView(RandomGossipMixin, ListView):
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
	success_url = reverse_lazy('home')

class LinkCreateView(CreateView):
	model = Link
	form_class = LinkForm
	success_url = reverse_lazy('home')
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

class LinkUpdateView(UpdateView):
	model = Link
	form_class = LinkForm
	template_name = 'link_form.html'

class LinkDeleteView(DeleteView):
	model = Link
	template_name = 'delete_confirm.html'
	success_url = reverse_lazy('home')

