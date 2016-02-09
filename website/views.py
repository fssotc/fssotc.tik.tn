from django.views.generic import DetailView, ListView
from django.shortcuts import render
from db.models import Event, Member

# Create your views here.
def index(request):
    # FIXME: only no passed events
    events = Event.objects.all()
    print(events.count())
    return render(request, 'website/index.html', {
        'events': events
    })

class MemberList(ListView):
    model = Member
    template_name = 'website/members.html'
    ordering = ['name', 'family_name']
