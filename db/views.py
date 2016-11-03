from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.admin.views.decorators import staff_member_required

from .forms import EmailForm


@staff_member_required
def email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.send_email()
    else:
        form = EmailForm(request.GET)

    return render(request, 'db/email.html', {
        'form': form,
    })
