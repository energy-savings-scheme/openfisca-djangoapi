from django.db import models

# Create your models here.


class Activity(models.Model):
    """
       Django model schema for the Safegard Activity model.
       The schema is based on the OpenFisca API metadata REGULATION REFERENCE


       OpenFisca Docs: https://openfisca.org/doc/openfisca-python-api/variables.html
       Source: https://openfisca.org/doc/_modules/openfisca_core/variables.html#Variable

       """

    version_code = models.CharField(
        max_length=255, null=False, blank=False, help_text="Abbreviation of the drafted Rules Version Name"
    )

    version_name = models.TextField(
        null=False, blank=False, help_text="Rule Draft Version of this activity"
    )

    sub_method = models.TextField(
        null=False, blank=False, help_text="Description of the SubMethod"
    )

    activity_name = models.TextField(
        null=False, blank=False, help_text="Description of the energy saving activity"
    )

    energy_savings = models.ForeignKey(
        "variables.Variable",
        related_name="energy_savings_var",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="The Final output variable that gives the energy savings of this activity.",
    )

    implementation = models.ManyToManyField(
        "variables.Variable",
        related_name="implementation",
        blank=True,
        help_text="implemention requirements for this activity."

    )
    eligibility = models.ManyToManyField(
        "variables.Variable", related_name="eligibility",
        blank=True,
        help_text="eligibility requirements for this activity."
    )
    equipment = models.ManyToManyField(
        "variables.Variable", related_name="equipment",
        blank=True,
        help_text="equipment requirements for this activity."
    )

    def __str__(self):
        return self.activity_name

    def __repr__(self):
        return f"<Activity: {str(self)}>"
