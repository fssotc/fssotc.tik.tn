from django.contrib import admin
from .models import Member, Inscription, Event, EventLink
from .filters import InscriptionSessionFilter, MemberInscriptionSessionFilter


class InscriptionInline(admin.TabularInline):
    model = Inscription
    extra = 1


class EventLinkInline(admin.TabularInline):
    model = EventLink
    extra = 2


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone', 'email')
    inlines = [InscriptionInline]
    search_fields = ['name', 'family_name', 'inscription__education', 'inscription__university']
    list_filter = ('inscription__education', MemberInscriptionSessionFilter,)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventLinkInline]
    list_display = ('title', 'start_date', 'end_date', 'place', 'is_passed')
    search_fields = ['title', 'place', 'start_date', 'end_date']
    list_filter = ('is_ours', 'event_type', 'place')


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'member', 'confirmed',
                    'dreamspark_key', 'member_card', 'is_current')
    list_filter = ('university', 'education', 'year', 'confirmed',
                   'dreamspark_key', 'member_card', InscriptionSessionFilter,
                   'role')
    list_editable = ('confirmed', 'dreamspark_key', 'member_card')

admin.site.register(EventLink)  # TODO: use class instead


def email_members(admin_model, request, queryset):
    from django.http import HttpResponseRedirect, HttpResponseForbidden
    from django.urls import reverse
    if isinstance(admin_model, MemberAdmin):
        emails = [m.email for m in queryset]
    elif isinstance(admin_model, InscriptionAdmin):
        emails = [insc.member.email for insc in queryset]
    else:
        return HttpResponseForbidden()
    return HttpResponseRedirect(reverse('send_mail') + '?to=' +
                                ','.join(emails))
email_members.short_description = "Email Members"
admin.site.add_action(email_members)
