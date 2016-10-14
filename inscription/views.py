import datetime

from .forms import InscriptionForm, MemberForm
from db.models import Member, Inscription
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
        member = member_form.save()
        inscription_form = InscriptionForm(request.POST)
        inscription = inscription_form.save(commit=False)
        inscription.member = member
        inscription.session = datetime.date.today()
        inscription.save()
        return render(request, 'inscription/success.html')
    else:
        member_form = MemberForm()
        inscription_form = InscriptionForm()

    return render(request, 'inscription/index.html', {
        'member_form': member_form,
        'inscription_form': inscription_form})


def success(request):
    return render(request, 'inscription/success.html')
