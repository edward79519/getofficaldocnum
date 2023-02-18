from django.core.management.base import BaseCommand
from docnum.schedule import report


class Command(BaseCommand):
    def handle(self, *args, **options):
        report.contract_monthly_report()
        report.mngr_monthly_report()