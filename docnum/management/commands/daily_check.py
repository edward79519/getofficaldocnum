from django.core.management.base import BaseCommand
from docnum.schedule import report


class Command(BaseCommand):
    def handle(self, *args, **options):
        report.user_expired_contra_check()