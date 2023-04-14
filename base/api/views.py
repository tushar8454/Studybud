from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
# . is used for previous directory
from base.models import Room
from .serializers import Roomserializer

# @api_view(['GET','PUT','POST'])
@api_view(['GET'])
def getroutes(request):
    routes=[
        'GET/api',
        'GET/api/rooms',
        'GET/api/rooms/:id',
    ]
    # SAFE CHANGE INTO JSON FILE
    # return JsonResponse(routes,safe=False)
    return Response(routes)


@api_view(['GET'])
def getrooms(requset):
    rooms=Room.objects.all()
    serializer=Roomserializer(rooms,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getroom(requset,pk):
    room=Room.objects.get(id=pk)
    serializer=Roomserializer(room,many=False)
    return Response(serializer.data)