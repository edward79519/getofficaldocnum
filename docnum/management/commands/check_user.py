from django.core.management.base import BaseCommand
from docnum.schedule.check_user import check_invalid


class Command(BaseCommand):
    def handle(self, *args, **options):
        check_invalid()
