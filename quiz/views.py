from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.edit import FormView

from .forms import QuizForm, CandidatForm
from .models import Submission, Quiz
from db.models import Member


def quiz(request, quiz_pk=None, quiz_title=None, member_pk=None,
         member_email=None):
    if quiz_pk:
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
    else:
        quiz = get_object_or_404(Quiz, title=quiz_title)
    if member_pk:
        member = get_object_or_404(Member, pk=member_pk)
    elif member_email:
        member = get_object_or_404(Member, email=member_email)
    elif request.method == 'POST':
        try:
            member = Member.object.get(email=request.POST['email'])
        except:
            return HttpResponseForbidden()
    else:
        member = Member()

    try:
        instance = Submission.objects.get(quiz=quiz, member=member)
        score = instance.score()
    except:
        instance = Submission(quiz=quiz, member=member)
        score = 0

    if request.method == 'POST':
        candidat_form = CandidatForm(request.POST, instance=member)
        form = QuizForm(request.POST, instance=instance)
        if candidat_form.is_valid() and form.is_valid():
            candidat_form.save()
            instance.save()
            form.save()
            return HttpResponseRedirect(reverse('submission', kwargs={
                "quiz_title": quiz.title,
                "member_email": member.email}))
    else:
        candidat_form = CandidatForm(instance=member)
        form = QuizForm(instance=instance)

    return render(request, 'quiz/quiz.html', {
        'candidat_form': candidat_form,
        'form': form,
        'score': score,
    })
