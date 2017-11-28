from django.contrib import admin
from .models import Member, Inscription
from .filters import (
    InscriptionSessionFilter, MemberInscriptionSessionFilter,
    MemberFieldsDuplicationFilter, InscriptionTypeFilter
)
from event.admin import RegisterAdmin
from quiz.admin import SubmissionAdmin


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


def export_as_vcard(modeladmin, request, queryset):
    from datetime import datetime
    from django.http import HttpResponse
    d = datetime.now()
    vcard = ""
    vcard_template = """BEGIN:VCARD
VERSION:3.0
N:{p.family_name};{p.name}
FN:{p.name} {p.family_name}
TEL;TYPE=HOME,VOICE:{p.phone}
EMAIL:{p.email}
REV:{rev}
END:VCARD
"""
    for person in queryset.all():
        person_vcard = vcard_template.format(
            p=person,
            rev=d.strftime('%Y%M%d%H%f'),
        )
        vcard += person_vcard
    # Prepare response
    response = HttpResponse(vcard, content_type='text/vcard')
    filename = 'fssotc_members_' + d.strftime('%Y%M%d%H%f') + '.vcf'
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


export_as_vcard.short_description = "Export as vCard"


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
    actions = [export_as_vcard, email_members]


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'member', 'confirmed',
                    'member_card', 'is_current')
    list_filter = ('university', 'education', 'year', 'confirmed',
                   'member_card', InscriptionSessionFilter, 'role',
                   InscriptionTypeFilter)
    list_editable = ('confirmed', 'member_card')
    actions = [email_members]
