from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pereval.models import Passes, PassUser, Coords, Level, Images
from pereval.serializers import PassSerializer


class PassTest(APITestCase):
    def setUp(self):
        """ Установки запускаются перед каждым тестом"""

        # Объект перевал 1
        self.pass_1 = Passes.objects.create(
            beauty_title='beauty_title',
            title='title',
            other_titles='other_title',
            connect='connect',
            user=PassUser.objects.create(
                email='Ivanov@mail.ru',
                fam='Иванов',
                name='Петр',
                otc='Васильевич',
                phone='89999999999'
            ),
            coords=Coords.objects.create(
                latitude=22.222,
                longitude=11.111,
                height=1000
            ),
            level=Level.objects.create(
                winter='',
                summer='1A',
                autumn='1A',
                spring=''
            )
        )

        # Изображение для объекта перевал 1
        self.image_1 = Images.objects.create(
            title='Title_1',
            data='https://images.app.goo.gl/eT3kx7tigk33vNQG8',
            pereval=self.pass_1
        )

    def test_get_pereval_list(self):
        """ Тест - список всех объектов модели Passes """
        response = self.client.get(reverse('submitData-list'))
        serializer_data = PassSerializer([self.pass_1, ], many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_get_pereval_list_email(self):
        """ Тест - список всех перевалов отобранных по email создавшего пользователя"""

        email = self.pass_1.user.email
        url = f'/submitData/?user__email={email}'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pass_pereval_create(self):
        json_text = ('{'
                     '"beauty_title": "пер.",'
                     '"title": "Пхия 123456",'
                     '"other_titles": "Триев",'
                     '"connect": "",'
                     '"user": {'
                     '    "email": "qwerty@mail.ru",'
                     '    "name": "Вася",'
                     '    "fam": "Пупкин",'
                     '    "otc": "Васильевич",'
                     '    "phone": "+7 902 000 00 00"'
                     '},'
                     '"coords": {'
                     '    "latitude": "45.3842",'
                     '    "longitude": "7.1525",'
                     '    "height": "1200"'
                     '},'
                     '"level": {'
                     '    "winter": "",'
                     '    "summer": "1A",'
                     '    "autumn": "1A",'
                     '    "spring": ""'
                     '},'
                     '"images": ['
                     '    {'
                     '        "data": "https://habrastorage.org/getpro/habr/company/361/259/86f/36125986f4f45846a087d0a71d88d32b.jpg",'
                     '        "title": "Седловина"'
                     '    },'
                     '    {'
                     '        "data": "https://assets.habr.com/habr-web/img/avatars/024.png",'
                     '        "title": "Подъём"'
                     '    }'
                     ']'
                     '}')
        url = f'/submitData/'
        response = self.client.post(url, json_text, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Passes.objects.count(), 2)
        self.assertEqual(Passes.objects.get(id=response.data['id']).title, 'Пхия 123456')

    def test_patch_pereval(self):
        json_text = ('{'
                     '    "beauty_title": "пер.",)'
                     '    "title": "Пхия",'
                     '    "other_titles": "Триев",'
                     '    "connect": "",'
                     '    "add_time": "18-04-2024 01:02:20",'
                     '    "user": {'
                     '        "email": "Ivanov@mail.ru",'
                     '        "name": "Петр",'
                     '        "fam": "Иванов",'
                     '        "otc": "Васильевич",'
                     '        "phone": "89999999999"'
                     '    },'
                     '    "coords": {'
                     '        "latitude": "50.00000000",'
                     '        "longitude": "50.00000000",'
                     '        "height": 1200'
                     '    },'
                     '    "level": {'
                     '        "winter": "",'
                     '        "summer": "1A",'
                     '        "autumn": "1A",'
                     '        "spring": ""'
                     '    },'
                     '    "images": ['
                     '        {'
                     '            "data": "https://assets.habr.com/habr-web/img/avatars/024.png",'
                     '            "title": "Подъём"'
                     '        },'
                     '    ],'
                     '}')

        pereval = Passes.objects.all().first()
        url = f'/submitData/{pereval.id}/'

        response = self.client.patch(url, json_text, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(Passes.objects.get(id=pereval.id).title, 'Пхия')
