from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse

from issues import models, forms

# Create your views here.


class CreateIssueView(CreateView):
    model = models.Issue
    form_class = forms.IssueForm
    success_url = reverse_lazy('cabinet')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.status = 'Pending'
        self.object.save()
        return super().form_valid(form)


class IssueDetail(DetailView):
    model = models.Issue

    def post(self, request, *args, **kwargs):
        comment_text = request.POST.get('comment', '')
        author = self.request.user
        data = {
            'author': author.id,
            'issue': kwargs.get('pk'),
            'text': comment_text
        }
        comment = forms.CommentForm(data)
        comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class NewIssueList(ListView):
    model = models.Issue
    queryset = models.Issue.objects.filter(status='Pending')
    ordering = '-created_at'
    template_name = 'new_issues.html'
    context_object_name = 'issue_list'

    def post(self, request, *args, **kwargs):
        issue_id = request.POST.get('issue_id', '')
        issue_reason = request.POST.get('reason', '')
        issue = models.Issue.objects.get(pk=issue_id)
        if 'decline' in request.POST:
            issue.status = 'Draft'
            issue.reason = issue_reason
        elif 'approve' in request.POST:
            issue.status = 'In progress'
            issue.save()
        issue.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class IssueUpdate(UpdateView):
    model = models.Issue
    form_class = forms.IssueForm

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.object.id})


class NewCommentView(CreateView):
    model = models.Comment
    form_class = forms.CommentForm

    def get_initial(self):
        initial = {'issue': self.kwargs.get('pk')}
        return initial

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.get_initial().get('issue')})

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

