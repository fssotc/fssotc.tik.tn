from django.db import models

# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length=40)
    family_name = models.CharField(max_length=40)
    birthday = models.DateField(blank=True, null=True)
    course = models.CharField(max_length=10)
    phone = models.CommaSeparatedIntegerField(max_length=20)
    address = models.CharField(max_length=400, blank=True, null=True)
    email = models.EmailField()
    new = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    dreamspark_key = models.BooleanField(default=False)
    member_card = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s" % (self.name, self.family_name)
