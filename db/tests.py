from django.test import TestCase
from datetime import date, timedelta
from .models import (
    Member, Inscription, Event, EventLink, inscription_confirmation
)
from django.utils import timezone
from django.db.models.signals import post_save


class MemberTestCase(TestCase):

    def setUp(self):
        usr1 = Member.objects.create(name='user1',
                                     family_name='family_name1',
                                     email='test1@example.com',
                                     phone='1111',)
        post_save.disconnect(receiver=inscription_confirmation,
                             sender=Inscription)

    def test_members_default_values(self):
        usr1 = Member.objects.get(name='user1')
        ins1 = Inscription.objects.create(session='2015-2016',
                                          university='FSS',
                                          education='LF',
                                          year='1',
                                          member=usr1,)
        ins2 = Inscription.objects.create(session='2016-2017',
                                          university='FSS',
                                          education='LF',
                                          year='2',
                                          member=usr1,)
        ins1 = usr1.inscription_set.get(education='LF', year='1')
        ins2 = Inscription.objects.get(education='LF', year='2')
        self.assertEqual(str(usr1), 'user1 family_name1')
        self.assertEqual(str(ins1), '2015-2016')
        self.assertEqual(str(ins2), '2016-2017')
        self.assertEqual(ins1.confirmed, False)
        self.assertEqual(ins1.member_card, False)

    def test_member_is_new(self):
        _date = date.today()
        usr1 = Member.objects.get(name='user1')
        self.assertEqual(usr1.is_new(), True)
        ins1 = Inscription.objects.create(session=_date,
                                          member=usr1,)
        self.assertEqual(usr1.is_new(), True)
        _date = date(_date.year - 1, _date.month, _date.day)
        ins2 = Inscription.objects.create(session=_date,
                                          member=usr1,)
        self.assertEqual(usr1.is_new(), False)

    def test_inscription_is_current(self):
        usr1 = Member.objects.get(name='user1')
        ins1 = Inscription.objects.create(member=usr1,)
        ins2 = Inscription.objects.create(session='2015-2016',
                                          member=usr1,)
        self.assertEqual(ins1.is_current(), True)
        self.assertEqual(ins2.is_current(), False)

    def test_event(self):
        _time = timezone.now()
        yesterday = timezone.make_aware(
            timezone.datetime(_time.year, _time.month, _time.day - 1))
        tomorrow = timezone.make_aware(
            timezone.datetime(_time.year, _time.month, _time.day + 1))
        evt1 = Event.objects.create(title='event1',
                                    description='desc',
                                    event_type='con',
                                    start=yesterday,
                                    is_ours=False,)
        evt2 = Event.objects.create(title='event2',
                                    description='desc',
                                    event_type='cha',
                                    start=yesterday,
                                    end=yesterday,
                                    is_ours=False,)
        evt3 = Event.objects.create(title='event3',
                                    description='desc',
                                    event_type='tra',
                                    start=yesterday,
                                    end=tomorrow,
                                    is_ours=False,)
        evt4 = Event.objects.create(title='event4',
                                    description='desc',
                                    event_type='tlk',
                                    start=tomorrow,
                                    is_ours=False,)
        self.assertEqual(evt1.is_passed(), True)
        self.assertEqual(evt2.is_passed(), True)
        self.assertEqual(evt3.is_passed(), False)
        self.assertEqual(evt4.is_passed(), False)
