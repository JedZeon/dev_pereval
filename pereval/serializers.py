from .models import Images, Level, Coords, PassUser, Passes
from rest_framework import serializers
from django.db import transaction


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class ImagesSerializer(serializers.ModelSerializer):
    data = serializers.URLField()

    class Meta:
        model = Images
        fields = ['data', 'title']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassUser
        fields = ['email', 'name', 'fam', 'otc', 'phone']


class PassSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer(allow_null=True)
    images = ImagesSerializer(many=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Passes
        fields = [
            'beauty_title',
            'title',
            'other_titles',
            'connect',
            'add_time',
            'user',
            'coords',
            'level',
            'images',
            'status'
        ]

    # Если новый перевал не создастся не создаются и остальные записи
    # Через транзакции
    @transaction.atomic
    def create(self, validated_data):
        user_ = validated_data.pop('user')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        exist_user = PassUser.objects.filter(email=user_['email']).first()

        if not exist_user:
            exist_user = PassUser.objects.create(**user_)

        coords = Coords.objects.create(**coords)
        levels = Level.objects.create(**level)

        new_pass = Passes.objects.create(
            **validated_data,
            user=exist_user,
            level=levels,
            coords=coords,
            status='new'
        )

        if images:
            for image in images:
                title = image.pop('title')
                data = image.pop('data')
                Images.objects.create(pereval=new_pass, title=title, data=data)

        return new_pass

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            validating_user_fields = [
                instance_user.name != data_user['name'],
                instance_user.fam != data_user['fam'],
                instance_user.otc != data_user['otc'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],
            ]
            if data_user is not None and any(validating_user_fields):
                raise serializers.ValidationError({'отклонено': 'у пользователя нельзя изменить данные'})
        return data

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        # PassUser.objects.update(**user)
        Coords.objects.update(**coords)
        Level.objects.update(**level)

        for image in images:
            title = image.pop('title')
            data = image.pop('data')
            Images.objects.update(data=data, title=title)

        return super().update(instance, validated_data)
