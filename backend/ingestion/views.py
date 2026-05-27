from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def upload_csv(request):

    return Response({
        "message": "endpoint working",
        "data": request.data
    })