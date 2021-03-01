from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView


class ExampleView(APIView):

    def get(self, request, *args, **kwargs):
        time = timezone.now()

        return Response({"time": time}, status=200)
    
    def post(self, request, *args, **kwargs):
        time = timezone.now()
        data = request.data

        return Response({"time": time, "data": data }, status=200)
        
