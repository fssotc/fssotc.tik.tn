from django.contrib import admin
from .models import Register
from db.models import Member, Event


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('event', 'member')
    list_filter = ('event', 'member')
