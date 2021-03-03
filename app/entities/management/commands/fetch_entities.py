""" Developer note
    - This module defines the Django command `fetch_entities` which is run in terminal by: `python manage.py fetch_entities`.
      This command is defined in the `Command.handle()` method
"""

import requests

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from entities.models import Entity


class Command(BaseCommand):
    help = "Fetches entities from OpenFisca API"

    def handle(self, *args, **options):
        try:
            self.stdout.ending = ""
            self.stdout.write(
                self.style.SUCCESS("\n##### Running `fetch_entities` ###############\n")
            )

            # Get variables from API
            entities_data = requests.get(f"{settings.OPENFISCA_API_URL}/entities")
            data = entities_data.json()

            # Check that the OpenFisca API returned a 200 response. If not, raise Exception
            if entities_data.status_code != 200:
                raise CommandError(
                    f"""[HTTPError]: the OpenFisca API returned a <{entities_data.status_code}> response. Expected <200> response.\nCheck that the specified OpenFisca API ({settings.OPENFISCA_API_URL}) is online."""
                )

            self.stdout.write(self.style.SUCCESS("Adding Entities to database "))

            # Iterate through entities
            for name in data.keys():
                json = data[name]
                description = json.get("description")
                plural = json.get("plural")
                documentation = json.get("documentation")
                is_person = json.get("roles", None) is None

                entity, created = Entity.objects.get_or_create(
                    name=name,
                    defaults={
                        "description": description,
                        "plural": plural,
                        "documentation": documentation,
                        "is_person": is_person,
                    },
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"\n{entity.__repr__()} added to database.")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"\n{entity.__repr__()} already exists in database. No action taken..."
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"\nSuccessfully updated database for {len(data.keys())} entities!\n"
                )
            )

        except CommandError as error:
            self.stdout.write(self.style.ERROR(f"Error creating Entity: {str(error)}"))
