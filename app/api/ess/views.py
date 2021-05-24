from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET", "POST"])
def activity_x1(request, *args, **kwargs):
    return Response({"foo": "bar"}, status=200)
