import logging
from typing import Any, Dict, List, Tuple

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Achievement, Cat

logger = logging.getLogger(__name__)

DEMO_USERS: List[Dict[str, Any]] = [
    {
        'username': 'astro_anna',
        'first_name': 'Анна',
        'last_name': 'Орбитова',
        'email': 'anna@meowhub.local',
    },
    {
        'username': 'nebula_ivan',
        'first_name': 'Иван',
        'last_name': 'Туманский',
        'email': 'ivan@meowhub.local',
    },
    {
        'username': 'comet_polina',
        'first_name': 'Полина',
        'last_name': 'Кометина',
        'email': 'polina@meowhub.local',
    },
    {
        'username': 'gravity_olga',
        'first_name': 'Ольга',
        'last_name': 'Тяготеева',
        'email': 'olga@meowhub.local',
    },
    {
        'username': 'saturn_maksim',
        'first_name': 'Максим',
        'last_name': 'Кольцев',
        'email': 'maksim@meowhub.local',
    },
    {
        'username': 'aurora_ksenia',
        'first_name': 'Ксения',
        'last_name': 'Полярная',
        'email': 'ksenia@meowhub.local',
    },
    {
        'username': 'meteor_kirill',
        'first_name': 'Кирилл',
        'last_name': 'Потоков',
        'email': 'kirill@meowhub.local',
    },
    {
        'username': 'zenith_maria',
        'first_name': 'Мария',
        'last_name': 'Зенитова',
        'email': 'maria@meowhub.local',
    },
    {
        'username': 'nova_stepan',
        'first_name': 'Степан',
        'last_name': 'Вспышкин',
        'email': 'stepan@meowhub.local',
    },
    {
        'username': 'signal_daria',
        'first_name': 'Дарья',
        'last_name': 'Частотина',
        'email': 'daria@meowhub.local',
    },
    {
        'username': 'orbit_roman',
        'first_name': 'Роман',
        'last_name': 'Эллипсов',
        'email': 'roman@meowhub.local',
    },
    {
        'username': 'eclipse_viktor',
        'first_name': 'Виктор',
        'last_name': 'Затмениев',
        'email': 'viktor@meowhub.local',
    },
]

DEMO_ACHIEVEMENTS: Tuple[str, ...] = (
    'Королева невесомости',
    'Чемпион по сну',
    'Капитан лазерных охотников',
    'Инженер по коробкам',
    'Мастер мурчания',
    'Архитектор когтеточек',
    'Посол доброго взгляда',
    'Страж подоконника',
    'Акробат скакалок',
    'Искатель солнечных пятен',
    'Гид по орбитам',
    'Дегустатор космического корма',
    'Навигатор робопылесоса',
    'Специалист по посадке на колени',
)

DEMO_CATS: List[Dict[str, Any]] = [
    {
        'name': 'Луна',
        'color': 'white',
        'birth_year': 2020,
        'owner': 'astro_anna',
        'achievements': ('Королева невесомости', 'Искатель солнечных пятен'),
    },
    {
        'name': 'Марсик',
        'color': 'darkorange',
        'birth_year': 2018,
        'owner': 'nebula_ivan',
        'achievements': ('Капитан лазерных охотников', 'Страж подоконника'),
    },
    {
        'name': 'Карамель',
        'color': 'bisque',
        'birth_year': 2016,
        'owner': 'gravity_olga',
        'achievements': ('Мастер мурчания', 'Специалист по посадке на колени'),
    },
    {
        'name': 'Орион',
        'color': 'darkgrey',
        'birth_year': 2019,
        'owner': 'saturn_maksim',
        'achievements': ('Гид по орбитам', 'Навигатор робопылесоса'),
    },
    {
        'name': 'Тайга',
        'color': 'saddlebrown',
        'birth_year': 2015,
        'owner': 'aurora_ksenia',
        'achievements': ('Архитектор когтеточек', 'Акробат скакалок'),
    },
    {
        'name': 'Светляк',
        'color': 'whitesmoke',
        'birth_year': 2021,
        'owner': 'zenith_maria',
        'achievements': ('Искатель солнечных пятен', 'Посол доброго взгляда'),
    },
    {
        'name': 'Комета',
        'color': 'orange',
        'birth_year': 2017,
        'owner': 'comet_polina',
        'achievements': ('Чемпион по сну', 'Посол доброго взгляда'),
    },
    {
        'name': 'Графит',
        'color': 'gray',
        'birth_year': 2014,
        'owner': 'meteor_kirill',
        'achievements': ('Страж подоконника', 'Архитектор когтеточек'),
    },
    {
        'name': 'Астра',
        'color': 'gainsboro',
        'birth_year': 2022,
        'owner': 'nova_stepan',
        'achievements': ('Королева невесомости', 'Мастер мурчания'),
    },
    {
        'name': 'Ирис',
        'color': 'bisque',
        'birth_year': 2020,
        'owner': 'signal_daria',
        'achievements': ('Дегустатор космического корма', 'Чемпион по сну'),
    },
    {
        'name': 'Йода',
        'color': 'darkgrey',
        'birth_year': 2013,
        'owner': 'astro_anna',
        'achievements': ('Инженер по коробкам', 'Гид по орбитам'),
    },
    {
        'name': 'Шёлк',
        'color': 'white',
        'birth_year': 2018,
        'owner': 'gravity_olga',
        'achievements': ('Посол доброго взгляда', 'Мастер мурчания'),
    },
    {
        'name': 'Радар',
        'color': 'black',
        'birth_year': 2016,
        'owner': 'nebula_ivan',
        'achievements': ('Навигатор робопылесоса', 'Капитан лазерных охотников'),
    },
    {
        'name': 'Иней',
        'color': 'whitesmoke',
        'birth_year': 2019,
        'owner': 'zenith_maria',
        'achievements': ('Чемпион по сну', 'Искатель солнечных пятен'),
    },
    {
        'name': 'Фобос',
        'color': 'chocolate',
        'birth_year': 2015,
        'owner': 'saturn_maksim',
        'achievements': ('Архитектор когтеточек', 'Страж подоконника'),
    },
    {
        'name': 'Мята',
        'color': 'gainsboro',
        'birth_year': 2021,
        'owner': 'aurora_ksenia',
        'achievements': ('Посол доброго взгляда', 'Акробат скакалок'),
    },
    {
        'name': 'Сапфир',
        'color': 'darkorange',
        'birth_year': 2012,
        'owner': 'nova_stepan',
        'achievements': ('Навигатор робопылесоса', 'Гид по орбитам'),
    },
    {
        'name': 'Дымок',
        'color': 'gray',
        'birth_year': 2014,
        'owner': 'meteor_kirill',
        'achievements': ('Дегустатор космического корма', 'Инженер по коробкам'),
    },
    {
        'name': 'Лилия',
        'color': 'white',
        'birth_year': 2023,
        'owner': 'signal_daria',
        'achievements': ('Посол доброго взгляда', 'Королева невесомости'),
    },
    {
        'name': 'Квант',
        'color': 'black',
        'birth_year': 2017,
        'owner': 'comet_polina',
        'achievements': ('Капитан лазерных охотников', 'Навигатор робопылесоса'),
    },
    {
        'name': 'Облако',
        'color': 'whitesmoke',
        'birth_year': 2016,
        'owner': 'orbit_roman',
        'achievements': ('Чемпион по сну', 'Искатель солнечных пятен'),
    },
    {
        'name': 'Зефир',
        'color': 'bisque',
        'birth_year': 2018,
        'owner': 'orbit_roman',
        'achievements': ('Мастер мурчания', 'Специалист по посадке на колени'),
    },
    {
        'name': 'Север',
        'color': 'gainsboro',
        'birth_year': 2015,
        'owner': 'eclipse_viktor',
        'achievements': ('Страж подоконника', 'Архитектор когтеточек'),
    },
    {
        'name': 'Пульсар',
        'color': 'darkorange',
        'birth_year': 2022,
        'owner': 'eclipse_viktor',
        'achievements': ('Гид по орбитам', 'Дегустатор космического корма'),
    },
    {
        'name': 'Туман',
        'color': 'gray',
        'birth_year': 2011,
        'owner': 'meteor_kirill',
        'achievements': ('Чемпион по сну', 'Навигатор робопылесоса'),
    },
]


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

    updates = {}
    if user.email != email:
        updates['email'] = email
    if not user.is_active:
        updates['is_active'] = True

    password_changed = False
    if created or not user.check_password(password):
        user.set_password(password)
        password_changed = True

    if created or updates or password_changed:
        for field, value in updates.items():
            setattr(user, field, value)
        update_fields = list(updates.keys())
        if password_changed:
            update_fields.append('password')
        user.save(update_fields=update_fields or None)
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
        users = _ensure_demo_users(settings.TEST_USER_PASSWORD)
        achievements = _ensure_demo_achievements()
        created, updated = _ensure_demo_cats(users, achievements)
        logger.info(
            'Демо-данные готовы: владельцы=%s, достижения=%s, коты (создано=%s, обновлено=%s)',
            len(users),
            len(achievements),
            created,
            updated,
        )


def _ensure_demo_users(password: str):
    user_model = get_user_model()
    lookup = {}
    for spec in DEMO_USERS:
        defaults = {
            'first_name': spec['first_name'],
            'last_name': spec['last_name'],
            'email': spec['email'],
            'is_active': True,
        }
        user, created = user_model.objects.get_or_create(
            username=spec['username'],
            defaults=defaults,
        )

        update_fields: List[str] = []
        for field, value in defaults.items():
            if getattr(user, field) != value:
                setattr(user, field, value)
                update_fields.append(field)

        is_staff = spec.get('is_staff', False)
        if user.is_staff != is_staff:
            user.is_staff = is_staff
            update_fields.append('is_staff')

        if created or not user.check_password(password):
            user.set_password(password)
            update_fields.append('password')

        if update_fields:
            user.save(update_fields=list(dict.fromkeys(update_fields)))

        lookup[spec['username']] = user
    return lookup


def _ensure_demo_achievements():
    lookup = {}
    for name in DEMO_ACHIEVEMENTS:
        achievement, _ = Achievement.objects.get_or_create(name=name)
        lookup[name] = achievement
    return lookup


def _ensure_demo_cats(users, achievements):
    created_count = 0
    updated_count = 0
    for spec in DEMO_CATS:
        owner = users.get(spec['owner'])
        if owner is None:
            continue
        defaults = {
            'color': spec['color'],
            'birth_year': spec['birth_year'],
        }
        cat, created = Cat.objects.get_or_create(
            owner=owner,
            name=spec['name'],
            defaults=defaults,
        )
        if created:
            created_count += 1
        else:
            update_fields = []
            for field, value in defaults.items():
                if getattr(cat, field) != value:
                    setattr(cat, field, value)
                    update_fields.append(field)
            if update_fields:
                cat.save(update_fields=update_fields)
                updated_count += 1
        desired = [achievements[name] for name in spec['achievements'] if name in achievements]
        if desired:
            cat.achievements.set(desired)
    return created_count, updated_count
