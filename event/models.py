from django.db import models
from db.models import Event, Member


class Register(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("member", "event")

    def __str__(self):
        return "{} - {}".format(self.event, self.member)

    def get_member_email(self):
        return self.member.email
    get_member_email.short_description = 'email'

    def get_member_university(self):
        return self.member.inscription_set.all().\
            order_by('-session')[0].university
    get_member_university.short_description = 'University'
    get_member_university.admin_order_field = 'member__inscription__university'

    def get_member_education(self):
        return self.member.inscription_set.all().\
            order_by('-session')[0].education
    get_member_education.short_description = 'education'
    get_member_education.admin_order_field = 'member__inscription__education'

    def get_member_year(self):
        return self.member.inscription_set.all().order_by('-session')[0].year
    get_member_year.short_description = 'year'
