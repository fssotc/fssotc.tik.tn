from django.contrib import admin
from django import forms
from django.db import models
from .models import Quiz, Question, Choice, Submission, Answer
import nested_admin
from grappelli.forms import GrappelliSortableHiddenMixin
# Register your models here.


class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 1})},
    }
    classes = ('grp-collapse grp-open',)


class QuestionInline(GrappelliSortableHiddenMixin,
                     nested_admin.NestedStackedInline):
    model = Question
    extra = 0
    inlines = [ChoiceInline]
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 3})},
    }
    inline_classes = ('grp-collapse grp-open',)
    sortable_field_name = "position"


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    list_display = ('__str__', 'questions_count', 'max_score')
    inlines = [QuestionInline]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'member', 'score')
    list_filter = ('quiz', 'member')
    inlines = [AnswerInline]
