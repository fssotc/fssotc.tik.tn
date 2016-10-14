from django.views.generic import DetailView, ListView
from django.shortcuts import render
from db.models import Event, Member, Inscription

# Create your views here.


def index(request):
    # FIXME: only no passed events
    events = Event.objects.comming()
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
        members_insc = self.model.objects.filter(role__exact='').order_by('member__name', 'member__family_name')
        context['member_list'] = [insc for insc in members_insc if insc.is_current()]
        admin_insc = self.model.objects.exclude(role__exact='').order_by('role', 'member__name', 'member__family_name')
        context['admin_list'] = [insc for insc in admin_insc if insc.is_current()]
        return context
