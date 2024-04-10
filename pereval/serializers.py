from .models import Images, Level, Coords, PassUser, Passes
from rest_framework import serializers


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

