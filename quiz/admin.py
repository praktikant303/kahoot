from django.contrib import admin
from . import models


@admin.register(models.User)
class UsersDisplay(admin.ModelAdmin):
    list_display = [
        'name',
        'last_name',
        'email',
        'list_of_groups',
        'telephone_number',
        'total_score',
    ]
    list_display_links = ['email']
    list_filter = ['groups']
    search_fields = ['name', 'last_name', 'telephone_number']
    ordering = ['ranking']
    readonly_fields = ['count_passed_tests', 'ranking', 'ranking_group']


@admin.register(models.Leader)
class LeaderDisplay(admin.ModelAdmin):
    list_display = [
        'name',
        'last_name',
        'email',
        'list_of_groups',
        'telephone_number',
        'ranking',
        'total_score',
        'count_passed_tests',
    ]
    list_filter = ['groups']
    search_fields = ['name', 'last_name', 'telephone_number']
    ordering = ['ranking']
    readonly_fields = ['count_passed_tests', 'ranking', 'ranking_group']
    list_display_links = ['email']



class UserInline(admin.TabularInline):
    model = models.User
    fields = [
        'email',
        'id'
    ]


class CatAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]
    inlines = [
        UserInline
    ]


@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'list_of_groups_quizzes'
    ]


class AnswerInlineModels(admin.TabularInline):
    """
    Allows to take two modules and use them on the same page
    We're going to put answers on the page as questions,
    because we'll be able to create answers, once we create questions
    """
    model = models.Answer
    max_num = 4
    min_num = 4
    extra = 4
    fields = [
        'answer_text',
        'is_right'
    ]


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'quiz',
        'question_image',
        'time_max',
        'score_max',
        'answer_score',
    ]
    list_display = [
        'title',
        'get_quizzes',
        'date_updated',
    ]

    inlines = [
        AnswerInlineModels
    ]


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'answer_text',
        'is_right',
        'question'
    ]
