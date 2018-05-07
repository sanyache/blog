# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from .forms import SignUpForm

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email','username')
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user