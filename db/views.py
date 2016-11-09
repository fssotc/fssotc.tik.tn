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
        data = request.GET.dict()
        if "body" not in data:
            data["body"] = """Cher membre,

On a le plaisir de vous ....

Cordialement,

---
Open Tech Club - Faculty of Sciences of Sfax

Phone: (+216) 28 204 299
Website: mtcfss.azurewebsites.net
Facebook: fb.me/fssotc
E-mail: fssotc@gmail.com
GitHub: github.com/fssotc"""
        print(data)
        form = EmailForm(data)

    return render(request, 'db/email.html', {
        'form': form,
    })
