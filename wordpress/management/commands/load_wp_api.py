from __future__ import unicode_literals

import logging
from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from dateutil import parser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "loads data from the Wordpress.com API, for the given site_id"

    def add_arguments(self, parser):
        parser.add_argument('site_id', nargs=1)
        parser.add_argument(
            '--purge',
            action='store_true',
            dest='purge',
            default=False,
            help='Purge data locally first.')
        parser.add_argument(
            '--full',
            action='store_true',
            dest='full',
            default=False,
            help='Full sweep of posts (update and insert as needed).')

    def handle(self, *args, **options):
        from wordpress import loading

        site_id = options['site_id'][0]

        purge_first = options.get("purge")
        full = options.get("full")

        modified_after = None
        if modified_after:
            # string to datetime
            modified_after = parse_datetime(modified_after) or parser.parse(modified_after)
            # assign current app's timezone if needed
            if timezone.is_naive(modified_after):
                modified_after = timezone.make_aware(modified_after, timezone.get_current_timezone())

        type = 'all'
        status = 'publish'
        batch_size = None

        loader = loading.WPAPILoader(site_id=site_id)
        loader.load_site(purge_first=purge_first,
                         full=full,
                         modified_after=modified_after,
                         type=type,
                         status=status,
                         batch_size=batch_size)
