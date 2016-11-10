import datetime

from .forms import InscriptionForm, MemberForm
from db.models import Member, Inscription
from django.contrib.messages import error, info, success
from django.forms import inlineformset_factory
from django.views.generic.edit import FormView
from django.shortcuts import render


class InscriptionView(FormView):
    template_name = 'inscription/index.html'
    form_class = InscriptionForm
    success_url = 'success/'

    def form_valid(self, form):
        return super(InscriptionView, self).form_valid(form)


def inscription(request):
    if request.method == 'POST':
        try:
            member = Member.objects.get(email=request.POST['email'])
        except:
            member = Member()
        member_form = MemberForm(request.POST, instance=member)
        inscription_form = InscriptionForm(request.POST)
        if any(insc.is_current() for insc in Inscription.objects.filter(member=member)):
            info(request, 'Already inscripted on the current session!')
        elif member_form.is_valid() and inscription_form.is_valid():
            member = member_form.save()
            inscription = inscription_form.save(commit=False)
            inscription.member = member
            inscription.session = Inscription.current_session()
            inscription.save()
            success(request, 'Inscription created!')
        else:
            error(request, 'Error when creating inscription!')
    else:
        member_form = MemberForm()
        inscription_form = InscriptionForm()

    return render(request, 'inscription/index.html', {
        'member_form': member_form,
        'inscription_form': inscription_form,
    })


def success(request):
    return render(request, 'inscription/success.html')
