from .forms import InscriptionForm
from django.views.generic.edit import FormView
from django.shortcuts import render


class InscriptionView(FormView):
    template_name = 'inscription/index.html'
    form_class = InscriptionForm
    success_url = 'success/'

    def form_valid(self, form):
        return super(InscriptionView, self).form_valid(form)


def success(request):
    return render(request, 'inscription/success.html')
