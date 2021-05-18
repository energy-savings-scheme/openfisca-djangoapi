from variables.models import Variable
from activities.models import Activity
from activities.serializers import ActivityListSerializer
from rest_framework import generics

from django.http import HttpResponse


def regulation_ref(entry):
    """
    helper function to create activity entry by unpacking the regulation reference from openfisca variables
    """
    metadata = entry.metadata
    if (metadata != None):
        if "regulation_reference" in metadata.keys():

            ref = entry.metadata["regulation_reference"]
            reg_ref = {"version_name": ref['version'],
                       "version_code": ref['identifier']}
            while "part" in ref.keys():
                ref = ref["part"]
                if (ref["part_type"] == "SubMethod"):
                    reg_ref["subMethod"] = ref["title"]

                if (ref["part_type"] == "Activity Definition"):
                    reg_ref["activity"] = ref["title"]

                if (ref["part_type"] == "Requirement"):
                    if ref["identifier"] == "energy_savings":
                        reg_ref["energy_savings"] = True
                    elif ref["identifier"] == "implementation":
                        reg_ref["implementation"] = True
                    elif ref["identifier"] == "eligibility":
                        reg_ref["eligibility"] = True
                    elif ref["identifier"] == "equipment":
                        reg_ref["equipment"] = True

            return reg_ref


def BuildActivityTable():

    all_variables = Variable.objects.all()
    for entry in all_variables:
        reg_ref = regulation_ref(entry)

        # create unique entry with version_name, version_code, subMethod, activity

        if reg_ref is not None and 'activity' in reg_ref.keys() and 'subMethod' in reg_ref.keys():
            activity, created = Activity.objects.get_or_create(
                version_name=reg_ref["version_name"],
                version_code=reg_ref["version_code"],
                sub_method=reg_ref['subMethod'],
                activity_name=reg_ref["activity"],
            )
            activity.save()
            # print(created)  # False if object already exist

        # Add many to many variable relations to the optional fields

            for (k, v) in reg_ref.items():
                if(v is True):
                    if(k == "energy_savings"):
                        setattr(activity, k, entry)
                    else:
                        for child in entry.children.all():
                            getattr(activity, k).add(child)
            activity.save()

    # print(Activity.objects.all())


class ActivityList(generics.ListAPIView):
    """
      LIST all Activities stored in the database

    # Returns
    - array of Activity objects (JSON)

    """
    queryset = Activity.objects.all()
    serializer_class = ActivityListSerializer
