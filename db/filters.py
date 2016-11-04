from datetime import date
from django.contrib import admin
from .models import Inscription


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
