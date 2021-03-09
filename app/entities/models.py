from django.db import models
from jsonfield import JSONField


class Entity(models.Model):
    """
    Django model schema for the Entity model.
    The schema is based on the OpenFisca API response.

    N.B. The OpenFisca API response differs slightly in naming convention from the
    OpenFisca source code...

    Source: https://openfisca.org/doc/_modules/openfisca_core/entities.html#Entity

    """

    name = models.CharField(
        max_length=255, null=False, blank=False, help_text="Entity name", unique=True
    )
    description = models.CharField(
        max_length=255, null=True, blank=True, help_text="Human-readable description"
    )
    plural = models.CharField(
        max_length=255, null=True, blank=True, help_text="Human-readable plural name"
    )
    documentation = models.TextField(null=True, blank=True, help_text="Documentation")
    is_person = models.BooleanField(
        default=False,
        help_text="Specifies whether the entity is a single entity (`Person`) or a group entity",
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Entity: {str(self)}>"