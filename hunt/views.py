from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max

from .models import Question, Profile, Answer
from .forms import SignUpForm, AnswerForm

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'piratehunt/index.html'
    context_object_name = 'team_list'

    def get_queryset(self):

        # return Profile.objects.order_by('-questions_answered__number').distinct()
       return Profile.objects.annotate(max_number=Max('questions_answered__number')).order_by('-max_number')

@login_required
def QuestionView(request):
    profile = request.user.profile
    last_question = profile.questions_answered.last()
    
    #Capture fringe cases
    if hasattr(last_question, 'number'): #the team has already answered a question
        
        #capture when the user's next question does not exist
        try:
            current_question = Question.objects.get(number=(last_question.number + 1))
        except:
            messages.info(request, 'It looks like you have answered all of the questions.  Good job!')
            return HttpResponseRedirect(reverse('piratehunt:index'))
    
    else: #this team has yet to answer the first question
        current_question = Question.objects.first()
        
    url = reverse('piratehunt:question', kwargs={'question_number': current_question.number})
    return HttpResponseRedirect(url)
    
class TeamDetailView(generic.DetailView):
    model = User
    template_name = 'piratehunt/team_details.html'

def team_auth(request, user_id):
    return HttpResponse("You're looking for team: %s" %user_id)
    
@login_required
def QuestionDetail(request, question_number):
    
    #create the user instance
    user = User.objects.get(pk=request.user.id)
    last_question = user.profile.questions_answered.last()
    
    #Capture the case of the team that hasn't yet answered a question
    if hasattr(last_question, 'number'): #the team has already answered a question
        
        #capture when the user's next question does not exist
        try:
            current_question = Question.objects.get(number=(last_question.number + 1))
        except:
            messages.info(request, 'It looks like you have answered all of the questions.  Good job!')
            return HttpResponseRedirect(reverse('piratehunt:index'))
        
    else:
        
        current_question = Question.objects.get(number = 1)
        user.profile.last_wrong_answer_made_on = now() - timedelta(hours=3)
        
    #Make sure this team is accessing the correct question
    if current_question.number == question_number:

        #Make sure that this team isn't trying to answer the question too fast
        if user.profile.last_wrong_answer_made_on < now() - timedelta(minutes=1):
            form = AnswerForm(request.POST)
            if form.is_valid():
                
                #create new Answer instance
                attempt = form.cleaned_data.get('answer')

                answer = current_question.answer_set.create(
                    text = attempt,
                    user = user,
                    made_on = now()
                )
                
                #test the answer to see if it is correct
                if  answer.text == current_question.answer1 or (attempt == current_question.answer2) or (attempt == current_question.answer3):
                    user.profile.questions_answered.add(current_question)
                    user.save()
                    
                    #update the question instance
                    current_question.times_solved = current_question.times_solved + 1
                    current_question.save()
                    
                    #update the answer instance to show that the answer is correct
                    answer.right = True
                    answer.save()

                    messages.info(request, 'Great News!  You are correct! You can now go on to the next problem')
                    return HttpResponseRedirect(reverse('piratehunt:index'))
                
                else:
                    user.profile.last_wrong_answer_made_on = now()
                    user.save()
                    
                    messages.info(request, 'All guesses are wrong!  Try again in one minute.')
                    return HttpResponseRedirect(reverse('piratehunt:index'))
                    
                    
            else: #this is the GET for this view
            
                return render(request, 'piratehunt/question_answer.html', {'form': form, 'question': current_question.question_text})
                
        else:  #Not enough time has passed since the last wrong answer
            
            messages.info(request, 'You must wait one minute before you can try to answer this question again')
            return HttpResponseRedirect(reverse('piratehunt:index'))
            
    else: #user is trying to access the wrong question number
        
        url = reverse('piratehunt:question', kwargs={'question_number': current_question.number})
        messages.info(request, 'You are not at that question')
        return HttpResponseRedirect(url)
    

class QuestionDetailView(generic.DetailView):
    model = Question

def signup(request):
    if request.user.is_authenticated:
        return redirect('/piratehunt')
    if request.method == 'POST':
        uform = SignUpForm(request.POST)
        if uform.is_valid():
            user = uform.save()
            user.refresh_from_db()
            user.email = uform.cleaned_data.get('email')
            user.profile.captain = uform.cleaned_data.get('captain')
            user.profile.team_member2 = uform.cleaned_data.get('team_member2')
            user.profile.team_member3 = uform.cleaned_data.get('team_member3')
            user.profile.team_member4 = uform.cleaned_data.get('team_member4')
            user.profile.team_member5 = uform.cleaned_data.get('team_member5')
            #make sure that the user can start answering questions right away
            user.profile.last_wrong_answer_made_on = now() - timedelta(hours = 2)
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