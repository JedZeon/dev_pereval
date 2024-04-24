from rest_framework import viewsets, status, mixins
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
    http_method_names = ['get', 'post', 'patch', ]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]
    filterset_fields = ['user__email', ]

    def list(self, request, *args, **kwargs):
        """
        Получить список перевалов, доступен отбор по email

        GET /submitData/ — получить список всех перевалов
        GET /submitData/?user__email='email' — список данных обо всех объектах, которые пользователь с почтой 'email' отправил на сервер
        """
        return super().list(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Добавление нового перевала

        автоматически присвоится статус - new
        """
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
        Получить данные перевала по ID

        GET /submitData/<id> — получить одну запись (перевал) по её id.
        Выводит всю информацию об объекте, в том числе статус модерации
        """
        if request.method != 'GET':
            return Response({
                'status': status.HTTP_405_METHOD_NOT_ALLOWED,
                'message': 'Метод запроса не поддерживается',
            })

        pk_ = self.kwargs.get('pk')
        pereval_ = Passes.objects.filter(pk=pk_).first()
        if pereval_:
            serializer = PassSerializer(pereval_)
            return Response(serializer.data)
        else:
            return Response({
                'error': 'Перевал не найден',
            })

    def partial_update(self, request, *args, **kwargs):
        """
        Внести изменения в существующий перевал, со статусом: new

        PATCH /submitData/<id> — изменение перевала по её id.
        Выводит всю информацию об объекте
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
