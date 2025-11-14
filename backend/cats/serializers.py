import base64
from datetime import datetime

from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers
import webcolors

from .models import Achievement, Cat


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            header, imgstr = data.split(';base64,')
            ext = header.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'upload.{ext}')
        return super().to_internal_value(data)


class HexColorField(serializers.CharField):
    def to_internal_value(self, value):
        value = super().to_internal_value(value)
        try:
            return webcolors.hex_to_name(value)
        except ValueError as exc:
            raise serializers.ValidationError('Неизвестный цвет') from exc


class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name')


class CatSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(required=False, many=True)
    color = HexColorField()
    age = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Cat
        fields = (
            'id',
            'name',
            'color',
            'birth_year',
            'achievements',
            'owner',
            'age',
            'image',
            'image_url',
            'created_at',
        )
        read_only_fields = ('owner', 'age', 'image_url', 'created_at')

    def get_age(self, obj):
        return datetime.now().year - obj.birth_year

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

    def validate_birth_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError('Год рождения не может быть в будущем')
        return value

    def validate_achievements(self, value):
        names = [item['name'] for item in value]
        if len(names) != len(set(names)):
            raise serializers.ValidationError('Достижения не должны повторяться')
        return value

    def _sync_achievements(self, cat, achievements):
        if achievements is None:
            return
        achievement_objects = []
        for payload in achievements:
            achievement, _ = Achievement.objects.get_or_create(name=payload['name'])
            achievement_objects.append(achievement)
        cat.achievements.set(achievement_objects)

    @transaction.atomic
    def create(self, validated_data):
        achievements = validated_data.pop('achievements', None)
        cat = Cat.objects.create(**validated_data)
        self._sync_achievements(cat, achievements)
        return cat

    @transaction.atomic
    def update(self, instance, validated_data):
        achievements = validated_data.pop('achievements', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if achievements is not None:
            self._sync_achievements(instance, achievements)
        return instance
