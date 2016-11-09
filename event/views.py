import datetime

from .forms import InscriptionForm, MemberForm
from db.models import Member, Inscription, Event
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from django.shortcuts import render, get_object_or_404
from .models import Register


def register(request, event_id):
    msg = ''
    event = get_object_or_404(Event, pk=event_id)
    if event.end_date and event.end_date < datetime.date.today():
        return render(request, 'event/ended.html', {'event': event})
    if request.method == 'POST':
        try:
            member = Member.objects.get(email=request.POST['email'])
        except:
            member = Member()
        member_form = MemberForm(request.POST, instance=member)
        inscription_form = InscriptionForm(request.POST)
        insc = [insc for insc in Inscription.objects.filter(member=member)
                if insc.is_current()]
        insc = insc[0] if len(insc) == 1 else None
        if not insc and member_form.is_valid() and inscription_form.is_valid():
            member = member_form.save()
            insc = inscription_form.save(commit=False)
            insc.member = member
            insc.session = Inscription.current_session()
            insc.save()
            created = True
        if insc:
            try:
                Register.objects.create(member=member, event=event)
                msg = 'You have successfully registered'
            except:
                msg = 'You has already registred!'
        else:
            msg = 'Error when registering!'
    else:
        member_form = MemberForm()
        inscription_form = InscriptionForm()

    return render(request, 'event/register.html', {
        'member_form': member_form,
        'inscription_form': inscription_form,
        'forms': [member_form, inscription_form],
        'event': event,
        'msg': msg
    })


class EventList(ListView):
    model = Event
    template_name = 'event/event_list.html'
    queryset = Event.objects.order_by('-start')


class EventDetail(DetailView):
    model = Event
    template_name = 'event/event_detail.html'
