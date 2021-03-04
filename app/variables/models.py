from django.db import models
from jsonfield import JSONField


class Variable(models.Model):
    """
    Django model schema for the Variable model.
    The schema is based on the OpenFisca API response.

    N.B. The OpenFisca API response differs slightly in naming convention from the
    OpenFisca source code...

    OpenFisca Docs: https://openfisca.org/doc/openfisca-python-api/variables.html
    Source: https://openfisca.org/doc/_modules/openfisca_core/variables.html#Variable

    """

    VALUE_TYPES = [
        ("Int", "Int"),
        ("Float", "Float"),
        ("Boolean", "Boolean"),
        ("String", "String"),
        ("Date", "Date"),
        ("Enum", "Enum"),
    ]

    DEFINTION_PERIOD = [("MONTH", "MONTH"), ("YEAR", "YEAR"), ("ETERNITY", "ETERNITY")]

    name = models.CharField(
        max_length=255, null=False, blank=False, help_text="Variable name"
    )
    description = models.TextField(
        null=True, blank=True, help_text="Human-readable description"
    )
    value_type = models.CharField(
        max_length=16,
        choices=VALUE_TYPES,
        null=True,
        blank=True,
        help_text="The value type of the variable",
    )
    entity = models.ForeignKey(
        "entities.Entity",
        related_name="variables",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="Entity the variable is defined for",
    )
    definition_period = models.CharField(
        max_length=16,
        choices=DEFINTION_PERIOD,
        null=True,
        blank=True,
        help_text="Period the variable is defined for",
    )
    reference = models.TextField(
        null=True,
        blank=True,
        help_text="Legislative reference describing the variable",
    )
    default_value = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Default value of the variable.",
    )
    possible_values = JSONField(null=True, blank=True)
    metadata = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Variable: {str(self)}>"

    @property
    def get_children(self):
        children_links = FormulaVariable.objects.filter(parent=self)
        children = Variable.objects.filter(children__in=children_links)

        return children

    @property
    def get_parents(self):
        parents_links = FormulaVariable.objects.filter(child=self)
        parents = Variable.objects.filter(is_parent__in=parents_links)

        return parents


class FormulaVariable(models.Model):
    parent = models.ForeignKey(
        "variables.Variable",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="is_parent",
    )
    child = models.ForeignKey(
        "variables.Variable",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )