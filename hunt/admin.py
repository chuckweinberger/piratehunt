from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group

from .models import Question, Profile, Answer

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Team Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = ('get_teamname', 'get_captain', 'get_last_question_answered')

    def get_teamname(self, instance):
        return instance.username
    get_teamname.short_description = "Team Name"

    def get_captain(self, instance):
        return instance.profile.captain
    get_captain.short_description = "Team Captain"

    def get_last_question_answered(self, instance):
        try:
            return instance.profile.questions_answered.last().number
        except AttributeError:
            return 0
    get_last_question_answered.short_description = "Last Question Answered"
    
class QuestionAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('number', 'question_text', 'first_to_solve', 'latest_to_miss', 'times_solved', 'times_missed')

class AnswerAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('question_number', 'question', 'text', 'right', 'user', 'made_on' )
    ordering = ('question__number',)

admin.site.unregister(User)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(User, UserAdmin)