from django.urls import path
from . import views

app_name = 'piratehunt'

urlpatterns = [

#   ex: /piratehunt
    path('', views.IndexView.as_view(), name='index'),
#   ex: /piratehunt/teams
    path('teams/', views.TeamView.as_view(), name='teams'),
#   ex: /piratehunt/teams/3
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
#   ex: /piratehunt/question/3
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    #   ex: '/piratehunt/signup
    path('signup/', views.signup, name='signup'),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='questions')
]