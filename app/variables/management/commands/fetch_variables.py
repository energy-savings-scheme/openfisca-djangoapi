import requests

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from entities.models import Entity
from variables.models import Variable


class Command(BaseCommand):
    help = "Fetches variables from OpenFisca API"

    def handle(self, *args, **options):

        try:
            # Get entities from API
            data = requests.get(f"{settings.OPENFISCA_API_URL}/variables").json()

            # Create shallow** list of variables
            ## ** `shallow` means that the list only stores the variable name and URL for details
            variables_list = []
            for name, json in data.items():
                _new_item = json
                _new_item["name"] = name
                variables_list.append(_new_item)

            variables_list = variables_list[10:40]  # for testing only

            num_created = 0
            num_already_exists = 0

            # First create a DB object for each variable
            # Currently these DB objects will only have the "name" populated
            for variable in variables_list:
                variable, created = Variable.objects.get_or_create(
                    name=variable["name"]
                )

                # For logging purposes, we keep track of how many (new) variables were created in the DB
                # and how many already existed in the DB
                if created:
                    num_created += 1
                    variable["created"] = True
                else:
                    num_already_exists += 1

            # Second - iterate through all variables in variables_list
            for variable in variables_list:
                # Only fetch details if the Variable is newly added to the DB
                if variable.get("created"):
                    obj = Variable.objects.get(name=variable["name"])
                    data = requests.get(variable["href"]).json()

                    obj.description = data.get("description")
                    obj.value_type = data.get("valueType")
                    obj.definition_period = data.get("definitionPeriod")
                    obj.default_value = str(data.get("defaultValue"))
                    obj.possible_values = data.get("possibleValues")

                    try:
                        entity = Entity.objects.get(name=data.get("entity"))
                        obj.entity = entity
                    except Entity.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Entity '{data.get('entity')}' does not exist in database yet. Try running `python manage.py fetch_entities` first. If this doesn't fix the problem, there may be an error with the OpenFisca application"
                            )
                        )

                    obj.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully populated database with Variables from {settings.OPENFISCA_API_URL}/variables.\n    {num_created} variables added to DB.\n    {num_already_exists} variables already existed in DB"
                )
            )

        except CommandError as error:
            self.stdout.write(self.style.ERROR(f"Error creating Entity: {str(error)}"))
