""" Developer note
    - This module defines the Django command `fetch_all` which is run in terminal by: `python manage.py fetch_all`.
      This command is defined in the `Command.handle()` method
"""

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):
    help = "Runs all fetch commands in the correct order: Entities, Variables, (Parameters - TODO)"

    def handle(self, *args, **options):
        try:
            if not settings.OPENFISCA_API_URL:
                raise CommandError(
                    "Environment variable `OPENFISCA_API_URL` not found. `OPENFISCA_API_URL` should be specified in a '.env' file in the project root directory."
                )

            self.stdout.write(
                self.style.WARNING(
                    f"\nIngesting OpenFisca data from: {settings.OPENFISCA_API_URL}"
                )
            )

            call_command("fetch_entities")
            call_command("fetch_variables")

        except CommandError as error:
            self.stdout.write(self.style.ERROR(str(error)))
