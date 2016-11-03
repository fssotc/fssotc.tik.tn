from django import forms
from django.core.mail import send_mass_mail
import django.conf


class EmailForm(forms.Form):
    subject = forms.CharField(default="""Cher membre,

On a le plaisir de vous ....

Cordialement,

---
Microsoft Tech Club Fss

Phone: (+216) 28 204 299
Website: mtcfss.azurewebsites.net
Facebook: fb.me/MTCFss
E-mail: mtcfss@outlook.com
GitHub: github.com/mtcfss""")
    content = forms.CharField(widget=forms.Textarea)
    to = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        to = {m for m in self.cleaned_data["to"].split()
              for m in m.split(',') if m}
        subject = self.cleaned_data["subject"].strip()
        content = self.cleaned_data["content"]
        mails = ((subject, content, django.conf.settings.DEFAULT_FROM_EMAIL,
                  [m]) for m in to)
        send_mass_mail(mails, fail_silently=True)
