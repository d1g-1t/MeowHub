import logging
from typing import Any

from django.conf import settings
from django.core.cache import cache
from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from .cache import build_cat_list_cache_key, reset_cat_cache
from .models import Achievement, Cat
from .serializers import AchievementSerializer, CatSerializer

logger = logging.getLogger(__name__)


class CatViewSet(viewsets.ModelViewSet):
    serializer_class = CatSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> QuerySet[Cat]:
        return Cat.objects.with_relations()

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        page_number = request.query_params.get('page', '1')
        cache_key = build_cat_list_cache_key(page_number)
        cached_payload = cache.get(cache_key)
        if cached_payload:
            return Response(cached_payload)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, settings.CACHE_TTL)
        return response

    def perform_create(self, serializer: CatSerializer) -> None:
        cat = serializer.save(owner=self.request.user)
        reset_cat_cache()
        logger.info('Создан кот %s пользователем %s', cat.pk, self.request.user.pk)

    def perform_update(self, serializer: CatSerializer) -> None:
        cat = serializer.save()
        reset_cat_cache()
        logger.info('Обновлён кот %s пользователем %s', cat.pk, self.request.user.pk)

    def perform_destroy(self, instance: Cat) -> None:
        cat_id = instance.pk
        owner_id = instance.owner_id
        super().perform_destroy(instance)
        reset_cat_cache()
        logger.info('Удалён кот %s пользователем %s', cat_id, owner_id)


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Achievement.objects.order_by('name')
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
