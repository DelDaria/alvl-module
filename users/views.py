from django.contrib.auth import login
from django.contrib.auth import logout as logout_
from django.http import HttpResponseRedirect

from django.views.generic import ListView

from django.shortcuts import render, redirect

from .forms import RegisterForm
from .models import User
from issues import models as iss_models


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index_page.html')
    else:
        return redirect('cabinet')


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
            )
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            return redirect('/')
    return render(request, 'register.html', {'form': form})


def logout(request):
    logout_(request)
    return redirect('/')


class UserCabinet(ListView):
    model = iss_models.Issue
    queryset = iss_models.Issue.objects.all()
    ordering = '-created_at'
    template_name = 'cabinet.html'
    context_object_name = 'issue_list'

    def post(self, request, *args, **kwargs):
        issue_id = request.POST.get('issue_id', '')
        issue = iss_models.Issue.objects.get(pk=issue_id)
        if 'restore' in request.POST:
            issue.status = 'Pending'
            issue.i += 1
        issue.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



