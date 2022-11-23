"""
Django command to delete expired binary images links.
"""
from django.utils import timezone
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand, CommandError

from datetime import timedelta, time, datetime

from images.models import BinaryImageLink

from pytz import timezone as tz
from django.conf import settings

class Command(BaseCommand):
    """Searching for expired links and removing them."""

    def handle(self, *args, **options):
        """Entrypoint for command"""

        settings_time_zone = tz(settings.TIME_ZONE)

        today = timezone.now()
        today_aware = today.astimezone(settings_time_zone)

        links = BinaryImageLink.objects.all()
        link_count = 0


        for link in links:
            link_date = link.expiration_date.astimezone(settings_time_zone)
            if link_date < today_aware:
                self.stdout.write(f"Log at {today_aware}. {link.binary_image.name} will be deleted. It's time expired at {link_date}.")
                link.delete()
                link_count += 1

        if link_count > 0:
                self.stdout.write(f"Periodic taks ended. The number of deleted links: {link_count}")
        else:
                self.stdout.write(f"Log at {today_aware}. Periodic taks ended. There was nothing to delete.")
