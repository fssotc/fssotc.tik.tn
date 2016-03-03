os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()

from db.models import Member

for m in Member.objects.all():
    if not m.username:
        m.username = None
        m.save()
