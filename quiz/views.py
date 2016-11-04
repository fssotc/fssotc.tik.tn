from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import PythonQuizForm

# Create your views here.


def python_quiz(request):
    score = 0
    if request.method == 'POST':
        form = PythonQuizForm(request.POST)
        if form.is_valid():
            score = form.score()
    else:
        form = PythonQuizForm()

    return render(request, 'quiz/python_quiz.html', {
        'form': form,
        'score': score,
        'max_score': len(form.fields) * 2,
    })
