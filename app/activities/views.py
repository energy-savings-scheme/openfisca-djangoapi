from variables.models import Variable
from activities.models import Activity
# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def regulation_ref(entry):

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
                elif (ref["part_type"] == "Activity Definition"):
                    reg_ref["activity"] = ref["title"]
                elif (ref["part_type"] == "Requirement"):
                    if ref["identifier"] == "energy_savings":
                        reg_ref["energy_savings"] = entry
                    elif ref["identifier"] == "implementation":
                        reg_ref["implementation"] = entry.children
                    elif ref["identifier"] == "eligibility":
                        reg_ref["eligibility"] = entry.children
                    elif ref["identifier"] == "equipment":
                        reg_ref["equipment"] = entry.children

            return reg_ref


def ActivityList():

    all_variables = Variable.objects.all()
    for entry in all_variables:

        reg_ref = regulation_ref(entry)
        if reg_ref is not None:
            print(entry.name)
            # print(reg_ref['activity'])

    test = Variable.objects.get(
        name="Appliance__installation_purpose")

    print(regulation_ref(test))  # only have version name and version code
#  activity, created = Activity.objects.get_or_create(
#             version_name=ref["version"])
