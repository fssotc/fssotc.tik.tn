from django.contrib import admin
from .models import Register
from db.models import Member, Event


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('event', 'member', 'get_member_email',
                    'get_member_university', 'get_member_education',
                    'get_member_year')
    list_filter = ('event', 'member')
