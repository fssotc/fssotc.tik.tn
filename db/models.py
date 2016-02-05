from django.db import models
from datetime import date

# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length=40)
    family_name = models.CharField(max_length=40)
    birthday = models.DateField(blank=True, null=True)
    phone = models.CommaSeparatedIntegerField(max_length=20)
    address = models.CharField(max_length=400, blank=True, null=True)
    email = models.EmailField()
    # new = models.BooleanField(default=True)  # is new if now inscription on old session

    def is_new(self):
        today = date.today()
        if today.month < 9:
            first_day_on_session = date(today.year - 1, 9, 1)
        else:
            first_day_on_session = date(today.year, 9, 1)
        ins = self.inscription_set.filter(session__lt=first_day_on_session)
        return ins.count() == 0

    def __str__(self):
        return "%s %s" % (self.name, self.family_name)

class Inscription(models.Model):
    session = models.DateField()  # auto_now_add=True
    course = models.CharField(max_length=10)
    confirmed = models.BooleanField(default=False)
    dreamspark_key = models.BooleanField(default=False)
    member_card = models.BooleanField(default=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        if self.session.month < 9:
            return "%d-%d" % (self.session.year - 1, self.session.year)
        else:
            return "%d-%d" % (self.session.year, self.session.year + 1)

class Event(models.Model):
    EVENT_TYPES = (
        ('con', 'conference'),
        ('cha', 'challenge'),
        ('tra', 'training'),
        ('tlk', 'talk'),
        ('unk', 'other'),
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    event_type = models.CharField(max_length=3, choices=EVENT_TYPES)
    place = models.CharField(max_length=80, default='FSS')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_ours = models.BooleanField()

    def is_passed(self):
        if self.end_date is not None:
            end = self.end_date
        else:
            end = self.start_date
        return end < date.today()

    def __str__(self):
        return self.title

class EventLink(models.Model):
    title = models.CharField(max_length=40)
    link = models.URLField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# TODO: add Project model
