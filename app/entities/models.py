from django.db import models
from jsonfield import JSONField

class Entity(models.Model):
    """
    Entity model.
    
    This class specified the db schema for Entity objects.
    The schema is based on the OpenFisca object attributes, and the OpenFisca API response

    Source: https://openfisca.org/doc/_modules/openfisca_core/entities.html#Entity

    """

    key = models.CharField(max_length=255, null=False, blank=False)
    label = models.CharField(max_length=255, null=False, blank=False)
    plural = models.CharField(max_length=255, null=False, blank=False)
    docs = models.CharField(max_length=255, null=False, blank=False)
    is_person = models.BooleanField(default=False)