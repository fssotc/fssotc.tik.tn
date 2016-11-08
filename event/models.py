from django.db import models
from db.models import Event, Member


class Register(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("member", "event")

    def __str__(self):
        return "{} - {}".format(self.event, self.member)
