from rest_framework import generics

from entities.models import Entity
from entities.serializers import EntityListSerializer


class EntitiesList(generics.ListAPIView):
    """
    ## LIST all Entities stored in the database

    ### Returns
    - array of Entity objects (JSON)

    ### Query params
    - None

    """

    queryset = Entity.objects.all()
    serializer_class = EntityListSerializer