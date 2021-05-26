""" Developer note
    - This module defines the Django command `fetch_variables` which is run in terminal by: `python manage.py fetch_variables`.
      This command is defined in the `Command.handle()` method
    - In practice, this method calls the OpenFisca API to get the details of each variable. This could be hundreds or thousands
      of requests.
    - We perform these requests asynchronously to improve the speed of the operation. The improvement is about 50x
    - The three `async` functions ("fetch", "bound_fetch", and "run") define this async workflow
"""

import asyncio
from aiohttp import ClientSession
import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from entities.models import Entity
from variables.models import Variable
from activities.views import BuildActivityTable
from variables import metadata


async def fetch(url, session, django_command):
    """Asynchronous function which retrieves the response.json() object
    from each GET request.

    :params:
    - url: ... boilerplate; see `aiohttp` docs for detailed explanation...
    - session: ... boilerplate; see `aiohttp` docs for detailed explanation...
    - django_command: Django Command instance to be used to write to `stdout` to show a progress indicator...

    """
    async with session.get(url) as response:
        resp = await response.json()

        # Check that the OpenFisca API returned a 200 response. If not, raise Exception
        status = response.status
        if status != 200:
            raise CommandError(
                f"""[HTTPError]: the OpenFisca API returned a <{status}> response. Expected <200> response.\nCheck that the specified OpenFisca API ({settings.OPENFISCA_API_URL}) is online."""
            )

        django_command.stdout.ending = ""
        django_command.stdout.write(django_command.style.SUCCESS("."))
        django_command.stdout.ending = "\n"

        return resp


async def bound_fetch(sem, url, session, django_command):
    """Asynchronous function which adds each async request to the task loop.
    We use asyncio.Semaphore to rate limit the queries, because we would likely crash
    the OpenFisca API server if we made 1000 requests all at once...

    :params:
    - sem: ... boilerplate; see `aiohttp` docs for detailed explanation...
    - url: ... boilerplate; see `aiohttp` docs for detailed explanation...
    - session: ... boilerplate; see `aiohttp` docs for detailed explanation...
    - django_command: Django Command instance to be used in the `fetch` method.

    """
    # Getter function with semaphore.
    async with sem:
        return await fetch(url, session, django_command)


async def run(variables_list, django_command):
    """Asynchronous function which creates a reusable async ClientSession and instantiates
    asyncio.Semaphore.

    :params:
    - variables_list [array of dicts]: passed from the Django Command instance.
    - django_command: Django Command instance to be used in the `fetch` method.

    """
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(20)

    # Create client session that will ensure we dont open new connection per each request.
    async with ClientSession() as session:
        for variable in variables_list:
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(
                bound_fetch(sem, variable["href"], session, django_command)
            )
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        return await responses


class Command(BaseCommand):
    help = "Asynchronously fetches variables from OpenFisca API."

    def handle(self, *args, **options):
        try:
            self.stdout.ending = ""
            self.stdout.write(
                self.style.SUCCESS(
                    "\n##### Running `fetch_variables` ###############\n"
                )
            )

            # Get variables from API
            variables_data = requests.get(
                f"{settings.OPENFISCA_API_URL}/variables")
            data = variables_data.json()

            # Check that the OpenFisca API returned a 200 response. If not, raise Exception
            if variables_data.status_code != 200:
                raise CommandError(
                    f"""[HTTPError]: the OpenFisca API returned a <{variables_data.status_code}> response. Expected <200> response.\nCheck that the specified OpenFisca API ({settings.OPENFISCA_API_URL}) is online."""
                )

            # Create shallow** list of variables
            # ** `shallow` means that the list only stores the variable name and URL for details
            variables_list = []
            for name, json in data.items():
                _new_item = json
                _new_item["name"] = name
                variables_list.append(_new_item)

            num_created = 0
            num_already_exists = 0

            self.stdout.write(self.style.SUCCESS(
                "Adding Variables to database "))

            # First create a DB object for each variable
            # Currently these DB objects will only have the "name" populated
            for variable in variables_list:
                obj, created = Variable.objects.get_or_create(
                    name=variable["name"])

                # Write to terminal to show progress
                self.stdout.write(self.style.SUCCESS("."))

                # For logging purposes, we keep track of how many (new) variables were created in the DB
                # and how many already existed in the DB
                if created:
                    num_created += 1
                    variable["created"] = True
                else:
                    num_already_exists += 1

            self.stdout.write(
                self.style.SUCCESS(
                    "\nFetching Variable details from OpenFisca API ")
            )

            future = asyncio.ensure_future(run(variables_list, self))
            result = asyncio.get_event_loop().run_until_complete(future)

            for data in result:
                # Get Variable object from database
                obj = Variable.objects.get(name=data["id"])

                # Update data as per response from OpenFisca API
                obj.default_value = str(data.get("defaultValue"))
                obj.description = data.get("description")
                obj.definition_period = data.get("definitionPeriod")
                obj.metadata = data.get("metadata")
                obj.possible_values = data.get("possibleValues")
                obj.value_type = data.get("valueType")

                # experiment to get a directory tree
                directory = data.get("source").split("#")[0].split("/")
                directory_index = directory.index('variables')
                obj.directory = "/".join(directory[directory_index:])

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
                    obj.formula = content

                    for variable_obj in Variable.objects.all():
                        variable_name = variable_obj.name
                        if (content.find(f'"{variable_name}"') > 0) or (
                            content.find(f"'{variable_name}'") > 0
                        ):
                            obj.children.add(variable_obj)

                obj.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"\nSuccessfully updated database for {len(result)} variables!\n"
                )
            )

            # ----------------------------------------
            # Build Activity Table
            # ----------------------------------------
            BuildActivityTable()
            # ----------------------------------------
            # Find all parents relations
            # TODO: Skip when parents are already present
            # ----------------------------------------

            # Set 'parents' field for all objects
            for entry in Variable.objects.all():
                # TODO: only update parents when it is absent. (with value None)
                entry.parents.set(entry.parent_set.all())
                entry.save()

            for entry in Variable.objects.all():
                # `metadata.get_input_offsprings` requires every Variable to have an alias ...
                # so we'll just add a placeholder alias if none already exists.
                # TODO - make `metadata.get_input_offsprings` less reliant on a particular metadata structure
                if entry.metadata.get("alias") is None:
                    entry.metadata["alias"] = metadata.makeAlias(entry.name)
                    entry.save()
                metadata.variableType(entry)

            # needs to have variableType updated first
            for entry in Variable.objects.all():
                metadata.get_input_offsprings(entry)

        except CommandError as error:
            self.stdout.write(
                self.style.ERROR(f"\nError creating Variable: {str(error)}")
            )
