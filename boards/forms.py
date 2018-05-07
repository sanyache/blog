from django import forms
from .models import Topic, Post

class NewTopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ['subject', 'message']

    message= forms.CharField(widget=forms.Textarea(attrs={'rows': 5,}), max_length=4000)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message',]