# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Link, Vote
# Register your models here.

# class LinkAdmin()

admin.site.register(Vote)
admin.site.register(Link)