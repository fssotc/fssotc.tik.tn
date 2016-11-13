from django.views.generic import DetailView, ListView
from django.shortcuts import render
from db.models import Member, Inscription
from event.models import Event

# Create your views here.


def index(request):
    # FIXME: only no passed events
    events = Event.objects.comming().order_by('start')
    print(events.count())
    return render(request, 'website/index.html', {
        'events': events
    })


class MemberList(ListView):
    model = Inscription
    template_name = 'website/members.html'
    ordering = ['member__name', 'member__family_name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        members_insc = self.model.objects.filter(
            role__exact='', confirmed=True,
            session=Inscription.current_session()
        ).order_by('member__name', 'member__family_name')
        context['member_list'] = members_insc
        admin_insc = self.model.objects.exclude(role__exact='').filter(
            session=Inscription.current_session()
        ).order_by('role', 'member__name', 'member__family_name')
        context['admin_list'] = admin_insc
        return context


def wpad(request):
    # wpad.dat file for auto-proxy detect on local network used on mtcfss club
    return render(request, 'website/wpad.dat',
                  content_type='application/x-ns-proxy-autoconfig')
