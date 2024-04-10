from rest_framework import viewsets, status
from rest_framework.response import Response

from pereval.models import Passes, PassUser, Coords, Level, Images
from pereval.serializers import UserSerializer, CoordsSerializer, LevelSerializer, ImagesSerializer, PassSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = PassUser.objects.all()
    serializer_class = UserSerializer


class CoordsViewSet(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class PassesViewSet(viewsets.ModelViewSet):
    queryset = Passes.objects.all()
    serializer_class = PassSerializer

    def create(self, request, *args, **kwargs):
        serializer = PassSerializer(data=request.data)

        status_ = ''
        message_ = None
        id_ = None

        if serializer.is_valid():
            serializer.save()
            status_ = status.HTTP_200_OK
            id_ = serializer.instance.id
        elif status.HTTP_400_BAD_REQUEST:
            status_ = status.HTTP_400_BAD_REQUEST
            message_ = 'Bad Request',
        elif status.HTTP_500_INTERNAL_SERVER_ERROR:
            status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
            message_ = 'Ошибка подключения к базе данных',

        return Response({
            'status': status_,
            'message': message_,
            'id': id_,
        })
