from django.urls import path
from . import views

app_name = 'piratehunt'

urlpatterns = [
#   ex: /piratehunt
    path('', views.IndexView.as_view(), name='index'),
#   ex: /piratehunt/teams/3
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
#   ex: /piratehunt/3/auth
    path('teams/<int:user_id>/auth', views.team_auth, name='team_auth'),
#   ex: /piratehunt/question/3
    path('question/<int:question_number>/', views.QuestionDetail, name='question'),
#   ex/piratehunt/signup
    path('signup/', views.signup, name='signup'),
    
]