# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Board, Topic, Post,HashTag

# Register your models here.

admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(HashTag)
