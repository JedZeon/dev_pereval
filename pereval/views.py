from rest_framework import viewsets, status
from rest_framework.response import Response

from pereval.models import Passes, PassUser, Coords, Level, Images
from pereval.serializers import UserSerializer, CoordsSerializer, LevelSerializer, ImagesSerializer, PassSerializer
import django_filters


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
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]
    filterset_fields = ['beauty_title', 'title', 'add_time', 'user__email']

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

    def retrieve(self, request, *args, **kwargs):
        """
        Обработка запроса конкретного перевала

        GET /submitData/<id> — получить одну запись (перевал) по её id.
        Выведи всю информацию об объекте, в том числе статус модерации
        """
        pk_ = self.kwargs.get('pk')
        pereval_ = Passes.objects.filter(pk=pk_).first()
        if pereval_:
            serializer = PassSerializer(pereval_)
            return Response(serializer.data)
        else:
            return Response({
                'error': 'Перевал не найден',
            })

    def update(self, request, *args, **kwargs):
        """
        Обработка запроса изменения перевала

        PATCH /submitData/<id> — изменение перевала по её id.
        Выведи всю информацию об объекте
        """
        instance = self.get_object()

        if instance.status != 'new':
            return Response({'state': '0', 'message': 'Можно редактировать только записи со статусом "new"'})

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'state': '1', 'message': 'Успешно удалось отредактировать запись в базе данных'})
        else:
            return Response({'state': '0', 'message': serializer.errors})
