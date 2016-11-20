from django.utils import timezone
from datetime import date

from django.db import models
from django.db.models.query_utils import Q
from db.models import Member
from django.shortcuts import reverse


class EventManager(models.Manager):

    def comming(self):
        return self.get_queryset().filter(Q(start__gte=date.today()) |
                                          Q(end__gte=date.today()))


class Event(models.Model):
    EVENT_TYPES = (
        ('con', 'conference'),
        ('cha', 'challenge'),
        ('tra', 'training'),
        ('tlk', 'talk'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    event_type = models.CharField(max_length=3, choices=EVENT_TYPES,
                                  blank=True)
    place = models.CharField(max_length=80,
                             default='Faculty of Sciences of Sfax, Amphi A9')
    start = models.DateTimeField(verbose_name="Event Start Time (UTC)")
    end = models.DateTimeField(blank=True, null=True,
                               verbose_name="Event End Time (UTC)")
    is_ours = models.BooleanField()
    price = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Price (-5 for members)")

    objects = EventManager()

    def get_absolute_url(self):
        return reverse('event', kwargs={'pk': self.pk})

    def is_passed(self):
        if self.end is not None:
            end = self.end
        else:
            end = self.start
        return end < timezone.now()

    is_passed.boolean = True

    def __str__(self):
        return self.title


class EventLink(models.Model):
    title = models.CharField(max_length=40)
    link = models.URLField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Register(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ("member", "event")

    def __str__(self):
        return "{} - {}".format(self.event, self.member)

    def get_member_email(self):
        return self.member.email
    get_member_email.short_description = 'email'

    def get_member_cin(self):
        return self.member.cin
    get_member_cin.short_description = 'CIN'

    @property
    def inscription(self):
        try:
            return self.member.inscription_set.get(session=Session.current_session())
        except:
            return self.member.inscription_set.all().order_by('-session')[0]

    def get_member_university(self):
        return self.inscription.university
    get_member_university.short_description = 'University'
    get_member_university.admin_order_field = 'member__inscription__university'

    def get_member_education(self):
        return self.inscription.education
    get_member_education.short_description = 'education'
    get_member_education.admin_order_field = 'member__inscription__education'

    def get_member_year(self):
        return self.inscription.year
    get_member_year.short_description = 'year'

    def inscription_paid(self):
        return self.inscription.confirmed
    inscription_paid.short_description = 'Inscription Paid'
    inscription_paid.boolean = True

    def has_paid(self):
        return self.event.price == 0 or self.paid
    has_paid.short_description = "Event Paid"
    has_paid.boolean = True

    def get_absolute_url(self):
        return reverse('registers', kwargs={'event_id': self.event_id})
