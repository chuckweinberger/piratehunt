from django.http import HttpResponseRedirect, HttpResponse
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

       return Profile.objects.all().order_by('-questions_answered__number')


class TeamDetailView(generic.DetailView):
    model = User
    template_name = 'piratehunt/team_details.html'

def team_auth(request, user_id):
    return HttpResponse("You're looking for team: %s" %user_id)
    
class QuestionView(generic.ListView):
    model = Question

class QuestionDetailView(generic.DetailView):
    model = Question

def signup(request):
    if request.user.is_authenticated:
        return redirect('/piratehunt')
    if request.method == 'POST':
        uform = SignUpForm(request.POST)
        # pform = UserProfileForm(data = request.POST)
        if uform.is_valid():
            user = uform.save()
            user.refresh_from_db()
            user.profile.captain = uform.cleaned_data.get('captain')
            user.profile.team_member2 = uform.cleaned_data.get('team_member2')
            user.profile.team_member3 = uform.cleaned_data.get('team_member3')
            user.profile.team_member4 = uform.cleaned_data.get('team_member4')
            user.profile.team_member5 = uform.cleaned_data.get('team_member5')
            user.save()
            username = uform.cleaned_data.get('username')
            password = uform.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/piratehunt')
        else:
            return render(request, 'registration/signup.html', {'uform': uform})
    else:
        uform = SignUpForm()
        return render(request, 'registration/signup.html', {'uform': uform})