import datetime
from django.utils import timezone

from .forms import InscriptionForm, MemberForm
from db.models import Member, Inscription
from django.contrib.messages import error, info, success
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import permission_required
from .models import Register, Event


def register(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.end and event.end < timezone.now():
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
        if insc:
            try:
                Register.objects.create(member=member, event=event)
                success(request, 'You have successfully registered')
            except:
                info(request, 'You has already registred!')
        else:
            error(request, 'Error when registering!')
    else:
        member_form = MemberForm()
        inscription_form = InscriptionForm()

    return render(request, 'event/register.html', {
        'member_form': member_form,
        'inscription_form': inscription_form,
        'forms': [member_form, inscription_form],
        'event': event,
    })


class EventList(ListView):
    model = Event
    template_name = 'event/event_list.html'
    queryset = Event.objects.order_by('-start')


class EventDetail(DetailView):
    model = Event
    template_name = 'event/event_detail.html'


@permission_required('event.change_register')
def register_list(request, event_id=None):
    registers = list(Register.objects.filter(event__id=event_id).order_by(
        'member__name'))
    event = registers[0].event if len(registers) else \
        get_object_or_404(Event, pk=event_id)
    others = list(Inscription.objects.filter(
        session=Inscription.current_session()).order_by('member__name'))
    registers_insc = [r.inscription for r in registers]
    others = [other for other in others if other not in registers_insc]
    return render(request, 'event/register_list.html', {
        'register_list': registers,
        'other_list': others,
        'event': event,
    })
