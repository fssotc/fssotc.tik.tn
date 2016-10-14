from django.views.generic import DetailView, ListView
from django.shortcuts import render
from db.models import Event, Member

# Create your views here.


def index(request):
    # FIXME: only no passed events
    events = Event.objects.comming()
    print(events.count())
    return render(request, 'website/index.html', {
        'events': events
    })


class MemberList(ListView):
    model = Member
    template_name = 'website/members.html'
    ordering = ['name', 'family_name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member_list'] = self.model.objects.filter(inscription__role__exact='')
        context['admin_list'] = self.model.objects.exclude(inscription__role__exact='').order_by('inscription__role', 'name', 'family_name')
        return context
