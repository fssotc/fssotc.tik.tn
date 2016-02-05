#!/usr/bin/env python
import os
import sys

if len(sys.argv) != 4:
    print("Usage: %s <username> <email> <passwd>" % sys.argv[0])
    sys.exit(1)

[_, username, email, passwd] = sys.argv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()

from django.contrib.auth.models import User


try:
    user = User.objects.get(username=username)
    user.email = email
    user.password = passwd
    user.is_staff = True
    user.is_superuser = True
    print("Updating the user")
except User.DoesNotExist:
    print("Creating new user")
    user = User.objects.create_superuser(username, email, passwd)

user.save()

print("Done successfuly")
