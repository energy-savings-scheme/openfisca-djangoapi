from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Fetches variables from OpenFisca API'

    def handle(self, *args, **options):

        try:
            print("""Fetching variables from OpenFisca API\n####################################\n#################################### """)
        except CommandError as e:
            print(e)
