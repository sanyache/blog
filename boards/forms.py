from django import forms
from .models import Topic, Post

class NewTopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ['subject', 'message']

    message= forms.CharField(widget=forms.Textarea(attrs={'rows': 5,}), max_length=4000)

class EditTopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ['subject',]

class AnonimPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['anonim_name','anonim_mail','message',]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message',]