from django.db import models
from jsonfield import JSONField

class Entity(models.Model):
    """
    Entity model. 

    """

    name = models.CharField(max_length=255, null=False, blank=False)
    metadata = JSONField()