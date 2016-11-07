from django import forms
import django.conf

from .models import Member, Inscription
from .email import send_mails


class EmailForm(forms.Form):
    subject = forms.CharField()
    body = forms.CharField(
        widget=forms.Textarea,
        help_text="Template body. Available context: name, family_name, "
        "email, phone, username, inscription.{year,session,education,"
        "university,role,confirmed}")
    to = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        to = {m for m in self.cleaned_data["to"].split()
              for m in m.split(',') if m}
        subject = self.cleaned_data["subject"].strip()
        body = self.cleaned_data["body"]
        send_mails(to, subject, body)
