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
