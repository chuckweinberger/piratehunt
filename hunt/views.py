from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import Question, Profile
from .forms import SignUpForm

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'piratehunt/index.html'
    context_object_name = 'team_list'

    def get_queryset(self):
        """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]

        return Profile.objects.order_by('last_question_answered')


class TeamView(generic.ListView):
    model = User
    #
    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.order_by('-pub_date')[:5]

class TeamDetailView(generic.DetailView):
    model = User

class QuestionView(generic.ListView):
    model = Question
    #
    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.order_by('-pub_date')[:5]

class QuestionDetailView(generic.DetailView):
    model = Question


def signup(request):
    if request.user.is_authenticated:
        return redirect('/piratehunt')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/piratehunt')
        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})