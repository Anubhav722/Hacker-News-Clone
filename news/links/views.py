# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import (ListView, 
	DetailView, 
	UpdateView, 
	CreateView,
	DeleteView,
	FormView,)

from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django_comments.models import Comment
from django.http import HttpResponse
	
import json

from .forms import UserProfileForm, LinkForm, VoteForm
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

	def get_context_data(self, **kwargs):
		context = super(LinkListView, self).get_context_data(**kwargs)
		if self.request.user.is_authenticated():
			voted = Vote.objects.filter(voter=self.request.user)
			links_in_page = [link.id for link in context["object_list"]]
			voted = voted.filter(link_id__in=links_in_page)
			voted = voted.values_list('link_id', flat=True)
			context["voted"] = voted
		return context

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

# class VoteFormView(FormView):
# 	model = Vote
# 	form_class = VoteForm

# 	def form_valid(self, form):
# 		link = get_object_or_404(Link, pk=form.data['link'])
# 		user = self.request.user
# 		prev_votes = Vote.objects.filter(voter=user, link=link)
# 		has_voted = (prev_votes.count() > 0)

# 		if not has_voted:
# 			Vote.objects.create(voter=user, link=link)
# 			print ('voted')

# 		else:
# 			prev_votes[0].delete()
# 			print ('unvoted')

# 		return redirect('home')

# 	def form_invalid(self, form):
# 		print ('invalid')
# 		return redirect('home')

class JSONFormMixin(object):
	def create_response(self, vdict=dict(), valid_form=True):
		# import ipdb; ipdb.set_trace()
		response = HttpResponse(json.dumps(vdict), content_type='application/json')
		response.status = 200 if valid_form else 500
		return response

class VoteFormBaseView(FormView):
	model = Vote
	form_class = VoteForm
	# import ipdb; ipdb.set_trace()
	def create_response(self, vdict=dict(), valid_form=True):
		# import ipdb; ipdb.set_trace()
		response = HttpResponse(json.dumps(vdict))
		response.status = 200 if valid_form else 500
		return response

	def form_valid(self, form):
		# import ipdb; ipdb.set_trace()
		link = get_object_or_404(Link, pk=form.data['link'])
		user = self.request.user
		prev_votes = Vote.objects.filter(voter = user, link=link)
		has_voted = (len(prev_votes) > 0)

		ret = {"success": 1}

		if not has_voted:
			v = Vote.objects.create(voter=user, link=link)
			ret['voteobj'] = v.id

		else:
			prev_votes[0].delete()
			ret['unvoted'] = 1

		return self.create_response(ret, True)

	def form_invalid(self, form):
		ret = {"success": 0, "form_errors": form.errors }
		return self.create_response(ret, False)

class VoteFormView(JSONFormMixin, VoteFormBaseView):
	pass