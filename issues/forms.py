from django import forms

from issues import models


class IssueForm(forms.ModelForm):
    class Meta:
        model = models.Issue
        fields = ('topic', 'text', 'priority')


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('author', 'issue', 'text')
