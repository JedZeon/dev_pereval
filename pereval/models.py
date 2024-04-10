from django.db import models
from .util import get_path_upload_photo


class PassUser(models.Model):
    email = models.CharField(max_length=200, verbose_name='Email адрес')
    fam = models.CharField(max_length=150, verbose_name='Фамилия')
    name = models.CharField(max_length=150, verbose_name='Имя')
    otc = models.CharField(max_length=150, blank=True, verbose_name='Отчество')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')


class Coords(models.Model):
    latitude = models.DecimalField(decimal_places=8, max_digits=10)
    longitude = models.DecimalField(decimal_places=8, max_digits=10)
    height = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Координаты'
        verbose_name_plural = 'Координаты'


class Level(models.Model):
    """
    Категория трудности. В разное время года перевал может иметь разную категорию трудности
    """
    CHOICE_LEVEL = (
        ('', ''),
        ('1A', '1A'),
        ('2A', '2A'),
        ('3A', '3A'),
        ('4A', '4A'),
    )
    winter = models.CharField(max_length=2, choices=CHOICE_LEVEL, default='')
    summer = models.CharField(max_length=2, choices=CHOICE_LEVEL, default='')
    autumn = models.CharField(max_length=2, choices=CHOICE_LEVEL, default='')
    spring = models.CharField(max_length=2, choices=CHOICE_LEVEL, default='')

    class Meta:
        verbose_name = 'Категория трудности'
        verbose_name_plural = 'Категории трудности'


class Passes(models.Model):
    STATUS = [
        ('new', 'new'),
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
    ]

    add_time = models.DateTimeField(auto_now_add=True)
    beauty_title = models.CharField(max_length=250, verbose_name='Красивое название')
    title = models.CharField(max_length=150, verbose_name='Название')
    other_titles = models.CharField(max_length=250, verbose_name='Дополнительное название')
    connect = models.CharField(blank=True, null=True, verbose_name='Какие объекты на местности соединяет данный перевал')
    user = models.ForeignKey(PassUser, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, verbose_name='Статус')

    class Meta:
        verbose_name = "Перевал"
        verbose_name_plural = "Перевалы"

    def __str__(self):
        return f'{self.title}'


class Images(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    data = models.ImageField(upload_to=get_path_upload_photo, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    pereval = models.ForeignKey(Passes, on_delete=models.CASCADE, blank=True, null=True, related_name='images')

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return f'{self.title}'
