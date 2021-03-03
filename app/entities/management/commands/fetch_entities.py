import requests

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from entities.models import Entity


class Command(BaseCommand):
    help = "Fetches entities from OpenFisca API"

    def handle(self, *args, **options):

        try:
            # Get entities from API
            entities_data = requests.get(
                f"{settings.OPENFISCA_API_URL}/entities"
            ).json()

            # Iterate through entities
            for name in entities_data.keys():
                json = entities_data[name]
                description = json.get("description")
                plural = json.get("plural")
                documentation = json.get("documentation")
                is_person = json.get("roles", None) is None

                entity, created = Entity.objects.get_or_create(
                    name=name,
                    description=description,
                    plural=plural,
                    documentation=documentation,
                    is_person=is_person,
                )
                if not created:
                    self.stdout.write(
                        self.style.WARNING(
                            f"{entity.__repr__()} already exists in database. No action taken..."
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully populated database with Entities from {settings.OPENFISCA_API_URL}/entities"
                )
            )

        except CommandError as error:
            self.stdout.write(self.style.ERROR(f"Error creating Entity: {str(error)}"))
