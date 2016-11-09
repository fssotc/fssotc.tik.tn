import threading
import django.conf
from django.core.mail import send_mass_mail
from django.template import Context, Template


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
            try:
                insc = m.inscription_set.get(
                    session=Inscription.current_session())
                ctxt.update({"inscription": insc})
            except:
                pass
        except:
            ctxt = Context()
        return tmpl.render(ctxt)

    def run(self):
        tmpl = Template(self.body)
        mails = ((self.subject, self.render(tmpl, mail),
                  django.conf.settings.DEFAULT_FROM_EMAIL, [mail])
                 for mail in self.to)
        send_mass_mail(mails, fail_silently=self.fail_silently)


def send_mails(to, subject, body):
    MassMailThread(to, subject, body).start()
