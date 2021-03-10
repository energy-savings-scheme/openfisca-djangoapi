import re
from variables.models import Variable
from django.db.models import Count, Q


variableTree = {
    "resa": ["resa"],  # RESA: Recognised Energy Savings Activity
    "nabers": ["nabers"],
    "D": [
        "D1",
        "D2",
        "D3",
        "D4",
        "D5",
        "D6",
        "D7",
        "D8",
        "D9",
        "D10",
        "D11",
        "D12",
        "D13",
        "D14",
        "D15",
    ],
    "E": [
        "E1",
        "E2",
        "E3",
        "E4",
        "E5",
        "E6",
        "E7",
        "E8",
        "E9",
        "E10",
        "E11",
        "E12",
        "E13",
    ],
    "F": [
        "F1",
        "F2",
        "F3",
        "F4",
        "F5",
        "F6",
        "F7",
        "F8",
        "F9",
        "F10",
        "F11",
        "F12",
        "F13",
        "F14",
        "F15",
    ],
}


# TODO: allow different wordings of keywords to find category
def update_categories(majorCat, minorCat):
    entries = Variable.objects.select_for_update().filter(
        Q(name__icontains=minorCat) | Q(description__icontains=minorCat)
    )
    entries.update(metadata={"majorCat": majorCat, "minorCat": minorCat})


def updateByVariableTree():
    for key in variableTree:
        majorCat = key
        for subCat in variableTree[key]:
            update_categories(majorCat, subCat)


def makeAlias(entry):
    toReplace = {'_and': '&',
                 'maximum': 'max',
                 'minimum': 'min',
                 '_percent': '%',
                 'reference': 'ref'}

    name0 = entry.name
    for word, newWord in toReplace.items():
        name0 = name0.replace(word, newWord)

    alias = re.sub(r'\b[A-Z]\d+_[a-zA-Z0-9]{1}_', "", name0)
    alias = re.sub(r'\b[A-Z]\d+_', "", alias)

    aliasList = []
    for word in alias.split("_"):
        if word.isupper():
            aliasList.append(word)
        else:
            aliasList.append(word.title())

    alias = " ".join(aliasList)

    if entry.metadata is None:
        entry.metadata = {"alias": alias}
    else:
        entry.metadata['alias'] = alias
    entry.save()


def findAllParents():
    for entry in Variable.objects.all():
        entry.parents.set(entry.parent_set.all())
        entry.save()
