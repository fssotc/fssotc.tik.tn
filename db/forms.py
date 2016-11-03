from django import forms
from django.core.mail import send_mass_mail
from django.template import Context, Template
import django.conf
import threading

from .models import Member


class MassMailThread(threading.Thread):

    def __init__(self, to, subject, body, fail_silently=True):
        self.to = to
        self.subject = subject
        self.body = body
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def render(self, tmpl, mail):
        try:
            m = Member.objects.get(email=mail)
            ctxt = Context({"name": m.name.capitalize(),
                            "family_name": m.family_name.capitalize(),
                            "email": mail,
                            "phone": m.phone,
                            "username": m.username,
                            })
        except Exception as e:
            print(e, mail)
            ctxt = Context()
        return tmpl.render(ctxt)

    def run(self):
        tmpl = Template(self.body)
        mails = ((self.subject, self.render(tmpl, mail),
                  django.conf.settings.DEFAULT_FROM_EMAIL, [mail])
                 for mail in self.to)
        import pprint
        pprint.pprint(list(mails))
        send_mass_mail(mails, fail_silently=self.fail_silently)


class EmailForm(forms.Form):
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)
    to = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        to = {m for m in self.cleaned_data["to"].split()
              for m in m.split(',') if m}
        subject = self.cleaned_data["subject"].strip()
        body = self.cleaned_data["body"]
        MassMailThread(to, subject, body, fail_silently=True).start()