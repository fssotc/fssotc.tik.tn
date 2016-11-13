from django.contrib import admin
from django.db.models.query_utils import Q


class RegisterPaidFilter(admin.SimpleListFilter):
    title = 'event paid'
    parameter_name = 'event_paid'

    def lookups(self, request, model_admin):
        return (('True', 'True'), ('False', 'False'))

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(Q(paid=True) | Q(event__price=0))
        elif self.value() == 'False':
            return queryset.filter(paid=False, event__price__gt=0)
