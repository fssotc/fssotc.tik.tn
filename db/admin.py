from django.contrib import admin
from .models import Member, Inscription
from .filters import (
    InscriptionSessionFilter, MemberInscriptionSessionFilter,
    MemberFieldsDuplicationFilter, InscriptionTypeFilter
)
from event.admin import RegisterAdmin
from quiz.admin import SubmissionAdmin


class InscriptionInline(admin.TabularInline):
    model = Inscription
    extra = 1


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone', 'email', 'cin')
    inlines = [InscriptionInline]
    search_fields = ['name', 'family_name', 'inscription__education',
                     'inscription__university', 'cin']
    list_filter = ('inscription__education', MemberInscriptionSessionFilter,
                   MemberFieldsDuplicationFilter)


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'member', 'confirmed',
                    'member_card', 'is_current')
    list_filter = ('university', 'education', 'year', 'confirmed',
                   'member_card', InscriptionSessionFilter, 'role',
                   InscriptionTypeFilter)
    list_editable = ('confirmed', 'member_card')


def email_members(admin_model, request, queryset):
    from django.http import HttpResponseRedirect, HttpResponseForbidden
    from django.urls import reverse
    if isinstance(admin_model, MemberAdmin):
        emails = {m.email for m in queryset}
    elif isinstance(admin_model,
                    (InscriptionAdmin, SubmissionAdmin, RegisterAdmin)):
        emails = {insc.member.email for insc in queryset}
    else:
        return HttpResponseForbidden()
    return HttpResponseRedirect(reverse('send_mail') + '?to=' +
                                ','.join(emails))


email_members.short_description = "Email Members"
admin.site.add_action(email_members)
