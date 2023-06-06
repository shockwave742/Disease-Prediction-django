from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import UserProfileModel, Results
from .forms import NewUserForm, InputForm

from MyApp.machineLearningModel import findDesesFromSymptom
from django.core.cache import cache


from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
import pandas as pd
import operator as op

# Create your views here.


def index(request):
    return render(request, 'home.html')


def redirect_index(request):
    __doc__ = '''When this function is called, it redirects user to index page.'''
    return HttpResponseRedirect('home')


class SignUpView(CreateView):
    form_class = NewUserForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def profile_view(request):
    user = get_object_or_404(UserProfileModel, username=request.user.username)
    # full_name = user.full_name
    # tokens = user.tokens
    return render(request, template_name='profile.html',
                  context={'user': user})


@login_required
def reports_view(request):
    user = get_object_or_404(UserProfileModel, username=request.user.username)
    last_report = Results.objects.filter(created_by=user).last()
    input_view = last_report.input
    str_input = str(input_view)
    disease = findDesesFromSymptom(str_input)

    last_report.result = disease
    last_report.save()

    cache.clear()

    reports_list = Results.objects.filter(created_by=user)
    return render(request, template_name="reports.html",
                  context={"reports_list": reports_list})




### Dynamic search is bidirectional
# TODO Modify this function for searching
@login_required
def input_symptoms_view(request):
    user1 = get_object_or_404(UserProfileModel, username=request.user.username)

    tk = user1.tokens

    # create a form instance and populate it with data from the request:
    form = InputForm(request.POST, initial={'user': request.user.id})
    # create the django object in memory, but don't save to the database

    if tk >= 1:
        # temporary saves dirty input
        if request.method == 'POST':

            # check whether it's valid:
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()

                # process the data in form.cleaned_data as required
                # ...

                UserProfileModel.objects.filter(username=request.user.username).update(tokens=(tk - 1))
                # redirect to a new URL:
                return HttpResponseRedirect('/reports')


        # if a GET (or any other method) we'll create a blank form
        else:
            form = InputForm()
    else:
        # Better be a error page
        print("user has no tokens")
        return HttpResponseRedirect('/error')

    template_name = 'input_symptoms.html'
    context = {'form': form}
    return render(request, template_name, context)

'''
@login_required
def input_symptoms_view(request):
    user1 = get_object_or_404(UserProfileModel, username=request.user.username)

    tk = user1.tokens

    # create a form instance and populate it with data from the request:
    form = InputForm(request.POST, initial={'user': request.user.id})
    # create the django object in memory, but don't save to the database

    if tk >= 1:
        # temporary saves dirty input
        if request.method == 'POST':

            # check whether it's valid:
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()

                # process the data in form.cleaned_data as required
                # ...

                UserProfileModel.objects.filter(username=request.user.username).update(tokens=(tk - 1))
                # redirect to a new URL:
                return HttpResponseRedirect('/reports')


        # if a GET (or any other method) we'll create a blank form
        else:
            form = InputForm()
    else:
        # Better be a error page
        print("user has no tokens")
        return HttpResponseRedirect('/error')

    template_name = 'input_symptoms.html'
    context = {'form': form, 'user1': user1}
    return render(request, template_name, context)
'''


def error_token_view(request):
    return render(request, 'error_tocken.html')

