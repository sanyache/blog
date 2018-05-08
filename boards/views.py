# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Board, Post, Topic, HashTag
from .forms import NewTopicForm, EditTopicForm, PostForm, AnonimPostForm

# Create your views here.

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})

def hash_create(form, post):
    words = form.cleaned_data.get('message').split(" ")
    for word in words:
        if word[0] == '#':
            hash_tag, created = HashTag.objects.get_or_create(name=word)
            hash_tag.post.add(post)

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(message=form.cleaned_data.get('message'),topic=topic, created_by= request.user)
            hash_create(form, post)

            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})

def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            hash_create(form, post)
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_quryset(self):
        queryset = super().get_quryset()
        return queryset.filter(create_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        hash_create(form, post)
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

def reply_delete(request, pk, topic_pk, post_pk):
    post = get_object_or_404(Post, topic__board__pk=pk, topic__pk=topic_pk, pk=post_pk)
    post.delete()
    return HttpResponseRedirect(reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk} ))

def topic_delete(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.delete()
    return HttpResponseRedirect(reverse ('board_topics', kwargs={'pk':pk}))

def topic_edit(request, pk, topic_pk):
    board = get_object_or_404(Board, pk=pk)
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == "POST":
        form = EditTopicForm(request.POST, instance=topic)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user

            topic.save()
            #post = Post.objects.create(message=form.cleaned_data.get('message'), topic=topic, created_by=request.user)
            #hash_create(form, post)
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = EditTopicForm(instance=topic)
    return render(request, 'edit_topic.html', {'form': form})


class TopicUpdate(UpdateView):
    model = Topic
    fields = ('subject',)
    pk_url_kwarg = 'pk'
    template_name = 'edit_topic.html'
    context_object_name = 'topic'

    def get_quryset(self):
        queryset = super().get_quryset()
        return queryset.filter(starter=self.request.user)


    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.last_updated = timezone.now()
        topic.save()
        return redirect('home')