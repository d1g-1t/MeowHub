import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from . import demo_data

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def ensure_test_user(sender, **kwargs):
    if sender.name != 'django.contrib.auth':
        return

    if kwargs.get('using') != 'default':
        return

    username = settings.TEST_USER_USERNAME
    email = settings.TEST_USER_EMAIL
    password = settings.TEST_USER_PASSWORD

    user_model = get_user_model()
    user, created = user_model.objects.get_or_create(
        username=username,
        defaults={'email': email, 'is_active': True},
    )

    update_fields = {}
    if user.email != email:
        update_fields['email'] = email
    if not user.is_active:
        update_fields['is_active'] = True

    password_changed = False
    if created or not user.check_password(password):
        user.set_password(password)
        password_changed = True

    if created or update_fields or password_changed:
        for field, value in update_fields.items():
            setattr(user, field, value)
        save_fields = list(update_fields.keys())
        if password_changed:
            save_fields.append('password')
        user.save(update_fields=save_fields or None)
        if created:
            logger.info('Создана тестовая учётная запись %s', username)
        else:
            logger.info('Обновлена тестовая учётная запись %s', username)
    else:
        logger.info('Тестовая учётная запись %s уже существует', username)


@receiver(post_migrate)
def ensure_demo_data(sender, **kwargs):
    if sender.name != 'cats':
        return

    if kwargs.get('using') != 'default':
        return

    if not getattr(settings, 'DEMO_DATA_ENABLED', True):
        logger.info('Пропущено наполнение демо-данными: DEMO_DATA_ENABLED=False')
        return

    with transaction.atomic():
        users = demo_data.ensure_demo_users(settings.TEST_USER_PASSWORD)
        achievements = demo_data.ensure_demo_achievements()
        created, updated = demo_data.ensure_demo_cats(users, achievements)
        logger.info(
            'Демо-данные готовы: владельцы=%s, достижения=%s, коты (создано=%s, обновлено=%s)',
            len(users),
            len(achievements),
            created,
            updated,
        )
