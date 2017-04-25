# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView

from .models import Vote, Link
# Create your views here.

class LinkListView(ListView):
	model = Link
	template_name = 'link_list.html'
