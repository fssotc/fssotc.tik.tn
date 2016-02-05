from django.test import TestCase
from .models import Member

# Create your tests here.
class MemberTestCase(TestCase):

    def setUp(self):
        Member.objects.create(name='user1',
                              family_name='family_name1',
                              email='test1@example.com',
                              course='lfi1',
                              phone='1111',
                              )

    def test_members_default_values(self):
        user1 = Member.objects.get(name='user1')
        self.assertEqual(str(user1), 'user1 family_name1')
        self.assertEqual(user1.new, True)
        self.assertEqual(user1.confirmed, False)
        self.assertEqual(user1.dreamspark_key, False)
        self.assertEqual(user1.member_card, False)
