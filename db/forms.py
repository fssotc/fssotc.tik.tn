from django import forms
from django.core.mail import send_mass_mail
import django.conf
import threading


class MassMailThread(threading.Thread):

    def __init__(self, mails, fail_silently=True):
        self.mails = mails
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mass_mail(self.mails, fail_silently=self.fail_silently)


class EmailForm(forms.Form):
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)
    to = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        to = {m for m in self.cleaned_data["to"].split()
              for m in m.split(',') if m}
        subject = self.cleaned_data["subject"].strip()
        body = self.cleaned_data["body"]
        mails = ((subject, body, django.conf.settings.DEFAULT_FROM_EMAIL, [m])
                 for m in to)
        MassMailThread(mails, fail_silently=True).start()
