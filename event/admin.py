from django.contrib import admin
from .models import Register, Event, EventLink
from db.models import Member
from .filters import RegisterPaidFilter


class EventLinkInline(admin.TabularInline):
    model = EventLink
    extra = 2


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventLinkInline]
    list_display = ('title', 'start', 'end', 'place', 'is_passed')
    search_fields = ['title', 'place', 'start', 'end']
    list_filter = ('is_ours', 'event_type', 'place')


admin.site.register(EventLink)


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('event', 'member', 'get_member_email',
                    'get_member_university', 'get_member_education',
                    'get_member_year', 'inscription_paid', 'has_paid')
    list_filter = ('event', 'member', RegisterPaidFilter)
