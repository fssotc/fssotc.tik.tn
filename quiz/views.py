from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import FormView

from .forms import QuizForm
from .models import Submission, Quiz
from db.models import Member

# Create your views here.


def quiz(request, quiz_pk=None, quiz_title=None, member_pk=None):
    score = 0
    if quiz_pk:
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
    else:
        quiz = get_object_or_404(Quiz, title=quiz_title)
    if member_pk:
        member = get_object_or_404(Member, pk=member_pk)
    else:
        member = Member()
    try:
        instance = Submission.objects.get(quiz=quiz, member=member)
    except:
        instance = Submission(quiz=quiz, member=member)

    if request.method == 'POST':
        form = QuizForm(request.POST, instance=instance)
        if form.is_valid():
            score = form.score()
    else:
        form = QuizForm(instance=instance)

    return render(request, 'quiz/quiz.html', {
        'form': form,
        'score': score,
    })
