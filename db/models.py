from django.db import models

# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length=40)
    family_name = models.CharField(max_length=40)
    birthday = models.DateField(blank=True)
    course = models.CharField(max_length=10)
    phone = models.CommaSeparatedIntegerField(max_length=20)
    address = models.CharField(max_length=400, blank=True)
    email = models.EmailField()
    new = models.BooleanField()
    confirmed = models.BooleanField()
    dreamspark_key = models.BooleanField()
    member_card = models.BooleanField()

    def __str__(self):
        return "%s %s" % (self.name, self.family_name)
