from django.db import models
from jsonfield import JSONField

class Variable(models.Model):
    """
    Variable model. 

    """

    variable_name = models.CharField(max_length=255, null=False, blank=False)
    metadata = JSONField()