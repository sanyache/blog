# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator


# Create your models here.

class Board(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

    def __unicode__(self):
        return u"%s"%(self.name)

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics')
    starter = models.ForeignKey(User, related_name='topics')
    views = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u"%s"%(self.subject)

class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts')
    updated_by = models.ForeignKey(User, null=True, related_name='+')

    def __unicode__(self):
        post = Truncator(self.message).chars(30)
        return u"%s"%(post)

class HashTag(models.Model):

    name = models.CharField(max_length = 50, unique = True)
    post = models.ManyToManyField(Post)

    def __unicode__(self):
        return u"%s"%(self.name)