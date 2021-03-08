import requests
# import variables import metadata

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from entities.models import Entity
from variables.models import Variable


class Command(BaseCommand):
    help = "Fetches variables from OpenFisca API"

    def handle(self, *args, **options):

        try:
            # Get entities from API
            data = requests.get(
                f"{settings.OPENFISCA_API_URL}/variables").json()

            # Create shallow** list of variables
            # ** `shallow` means that the list only stores the variable name and URL for details
            variables_list = []
            for name, json in data.items():
                _new_item = json
                _new_item["name"] = name
                variables_list.append(_new_item)

            num_created = 0
            num_already_exists = 0
            print(num_created)
            # First create a DB object for each variable
            # Currently these DB objects will only have the "name" populated
            for variable in variables_list:
                obj, created = Variable.objects.get_or_create(
                    name=variable["name"])

                # Write to terminal to show progress
                self.stdout.ending = ""
                self.stdout.write(self.style.SUCCESS("."))
                self.stdout.ending = "\n"

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
                # if variable.get("created"):
                if True:
                    obj = Variable.objects.get(name=variable["name"])
                    data = requests.get(variable["href"]).json()

                    obj.description = data.get("description")
                    obj.value_type = data.get("valueType")
                    obj.definition_period = data.get("definitionPeriod")
                    obj.default_value = str(data.get("defaultValue"))
                    obj.possible_values = data.get("possibleValues")

                    # Link this Variable object to an Entity object according to the entity `name` attribute
                    try:
                        entity = Entity.objects.get(name=data.get("entity"))
                        obj.entity = entity
                    except Entity.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Entity '{data.get('entity')}' does not exist in database yet. Try running `python manage.py fetch_entities` first. If this doesn't fix the problem, there may be an error with the OpenFisca application"
                            )
                        )

                    formulas = data.get("formulas")
                    if formulas:
                        dates = list(formulas.keys())
                        latest_formula = formulas[dates[0]]
                        content = latest_formula.get("content", "")

                        for variable_obj in Variable.objects.all():
                            variable_name = variable_obj.name
                            if (content.find(f'"{variable_name}"') > 0) or (
                                content.find(f"'{variable_name}'") > 0
                            ):
                                # FormulaVariable.objects.get_or_create(
                                #     parent=obj, child=variable_obj
                                # )
                                obj.children.add(variable_obj)

                                # Write to terminal to show progress
                                self.stdout.ending = ""
                                self.stdout.write(self.style.SUCCESS("*"))
                                self.stdout.ending = "\n"

                    obj.save()
                    # Write to terminal to show progress
                    self.stdout.ending = ""
                    self.stdout.write(self.style.SUCCESS("."))
                    self.stdout.ending = "\n"

            self.stdout.write(
                self.style.SUCCESS(
                    f"\nSuccessfully populated database with Variables from {settings.OPENFISCA_API_URL}/variables.\n    {num_created} variables added to DB.\n    {num_already_exists} variables already existed in DB"
                )
            )

            # TODO: where should I leave these as one-time thing here?

            # UpDating MetaData here

            # metadata.updateByVariableTree()
            # for entry in Variable.objects.all():
            #     metadata.makeAlias(entry)
            # metadata.findAllParents()

        except CommandError as error:
            self.stdout.write(self.style.ERROR(
                f"Error creating Entity: {str(error)}"))
