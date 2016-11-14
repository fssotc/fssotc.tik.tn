from datetime import date
from django.contrib import admin
from .models import Inscription, Member
from django.db.models import Count


class InscriptionSessionFilter(admin.SimpleListFilter):
    title = 'session'
    parameter_name = 'session'

    def lookups(self, request, model_admin):
        return reversed(Inscription.SESSIONS)

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(session=self.value())


class MemberInscriptionSessionFilter(InscriptionSessionFilter):
    parameter_name = 'inscription'

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(inscription__session=self.value())


class MemberFieldsDuplicationFilter(admin.SimpleListFilter):
    title = 'possible duplications'
    parameter_name = 'duplicated_field'

    def lookups(self, request, queryset):
        return (
            ('phone', 'By Phone'),
            ('birthday', 'By Birthday'),
            ('family_name', 'By Family Name'),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            n = Member.objects.values(self.value()).\
                annotate(Count('id')).order_by().\
                filter(id__count__gt=1).values(self.value())
            n = [e[self.value()] for e in n]
        if self.value() == 'phone':
            return queryset.filter(phone__in=n)
        if self.value() == 'birthday':
            return queryset.filter(birthday__in=n)
        if self.value() == 'family_name':
            return queryset.filter(family_name__in=n)


class InscriptionTypeFilter(admin.SimpleListFilter):
    title = 'inscription type'
    parameter_name = 'inscription_type'

    def lookups(self, request, queryset):
        return (
            ('new', 'New Inscription'),
            ('renew', 'Renew Inscription (Inscripted Last Year)'),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            if ('session' not in request.GET):
                from django.contrib.messages import warning
                warning(request, '"Inscription Type" filter needs "Session" '
                        'filter to be specified!')
                return
            session = request.GET['session']
            inscps = Inscription.objects.filter(session__lt=session).\
                values('member_id').\
                annotate(Count('session')).order_by().\
                filter(session__count__gt=0)
            members = [inscp['member_id'] for inscp in inscps]
        if self.value() == 'new':
            return queryset.exclude(member_id__in=members)
        if self.value() == 'renew':
            return queryset.filter(member_id__in=members)
