from django.test import TestCase
from datetime import date, timedelta
from .models import Member, Inscription, Event, EventLink

# Create your tests here.


class MemberTestCase(TestCase):

    def setUp(self):
        usr1 = Member.objects.create(name='user1',
                                     family_name='family_name1',
                                     email='test1@example.com',
                                     phone='1111',)

    def test_members_default_values(self):
        usr1 = Member.objects.get(name='user1')
        ins1 = Inscription.objects.create(session=date(2016, 8, 31),
                                          course='lfi1',
                                          member=usr1,)
        ins2 = Inscription.objects.create(session=date(2016, 9, 1),
                                          course='lfi2',
                                          member=usr1,)
        ins1 = usr1.inscription_set.get(course='lfi1')
        ins2 = Inscription.objects.get(course='lfi2')
        self.assertEqual(str(usr1), 'user1 family_name1')
        self.assertEqual(str(ins1), '2015-2016')
        self.assertEqual(str(ins2), '2016-2017')
        self.assertEqual(ins1.confirmed, False)
        self.assertEqual(ins1.dreamspark_key, False)
        self.assertEqual(ins1.member_card, False)

    def test_member_is_new(self):
        _date = date.today()
        usr1 = Member.objects.get(name='user1')
        self.assertEqual(usr1.is_new(), True)
        ins1 = Inscription.objects.create(session=_date,
                                          course='lfi1',
                                          member=usr1,)
        self.assertEqual(usr1.is_new(), True)
        _date = date(_date.year - 1, _date.month, _date.day)
        ins2 = Inscription.objects.create(session=_date,
                                          course='lfi2',
                                          member=usr1,)
        self.assertEqual(usr1.is_new(), False)

    def test_inscription_is_current(self):
        _date = date.today()
        usr1 = Member.objects.get(name='user1')
        ins1 = Inscription.objects.create(session=_date,
                                          course='lfi1',
                                          member=usr1,)
        _date = date(_date.year - 1, _date.month, _date.day)
        ins2 = Inscription.objects.create(session=_date,
                                          course='lfi1',
                                          member=usr1,)
        self.assertEqual(ins1.is_current(), True)
        self.assertEqual(ins2.is_current(), False)

    def test_event(self):
        _date = date.today()
        yesterday = date(_date.year, _date.month, _date.day - 1)
        tomorrow = date(_date.year, _date.month, _date.day + 1)
        evt1 = Event.objects.create(title='event1',
                                    description='desc',
                                    event_type='con',
                                    start_date=yesterday,
                                    is_ours=False,)
        evt2 = Event.objects.create(title='event2',
                                    description='desc',
                                    event_type='cha',
                                    start_date=yesterday,
                                    end_date=yesterday,
                                    is_ours=False,)
        evt3 = Event.objects.create(title='event3',
                                    description='desc',
                                    event_type='tra',
                                    start_date=yesterday,
                                    end_date=tomorrow,
                                    is_ours=False,)
        evt4 = Event.objects.create(title='event4',
                                    description='desc',
                                    event_type='tlk',
                                    start_date=tomorrow,
                                    is_ours=False,)
        self.assertEqual(evt1.place, 'FSS')
        self.assertEqual(evt1.is_passed(), True)
        self.assertEqual(evt2.is_passed(), True)
        self.assertEqual(evt3.is_passed(), False)
        self.assertEqual(evt4.is_passed(), False)
