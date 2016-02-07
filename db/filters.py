from datetime import date
from django.contrib import admin
from .models import Inscription

class InscriptionSessionFilter(admin.SimpleListFilter):
    title = 'session'
    parameter_name = 'session'

    def lookups(self, request, model_admin):
        choises = reversed(sorted(set(str(o) for o in Inscription.objects.all())))
        return [(name, name) for name in choises]

    def queryset(self, request, queryset):
        if self.value() is not None:
            years = self.value().split('-')
            return queryset.filter(
                session__gte=date(int(years[0]), 9, 1),
                session__lt=date(int(years[1]), 9, 1))

class MemberInscriptionSessionFilter(InscriptionSessionFilter):
    parameter_name = 'inscription'

    def queryset(self, request, queryset):
        if self.value() is not None:
            years = self.value().split('-')
            return queryset.filter(
                inscription__session__gte=date(int(years[0]), 9, 1),
                inscription__session__lt=date(int(years[1]), 9, 1))
