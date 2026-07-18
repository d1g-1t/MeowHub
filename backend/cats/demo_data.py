import logging
from typing import Any, Dict, List, Tuple

from django.contrib.auth import get_user_model

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


def ensure_demo_users(password: str):
    user_model = get_user_model()
    usernames = [spec['username'] for spec in DEMO_USERS]
    existing_users = user_model.objects.in_bulk(usernames, field_name='username')

    to_create = []
    for spec in DEMO_USERS:
        username = spec['username']
        if username in existing_users:
            user = existing_users[username]
            update_fields = {}
            for field in ('first_name', 'last_name', 'email', 'is_active'):
                value = spec.get(field, True if field == 'is_active' else None)
                if value is not None and getattr(user, field) != value:
                    setattr(user, field, value)
                    update_fields[field] = value

            if not user.check_password(password):
                user.set_password(password)
                update_fields['password'] = True

            if update_fields:
                user.save(update_fields=list(update_fields.keys()))
        else:
            to_create.append(
                get_user_model()(
                    username=username,
                    first_name=spec['first_name'],
                    last_name=spec['last_name'],
                    email=spec['email'],
                    is_active=True,
                )
            )

    if to_create:
        created_users = get_user_model().objects.bulk_create(to_create)
        for user in created_users:
            user.set_password(password)
        get_user_model().objects.bulk_update(created_users, ['password'])
        existing_users = user_model.objects.in_bulk(usernames, field_name='username')

    return existing_users


def ensure_demo_achievements():
    Achievement.objects.bulk_create(
        [Achievement(name=name) for name in DEMO_ACHIEVEMENTS],
        ignore_conflicts=True,
    )
    return Achievement.objects.in_bulk(DEMO_ACHIEVEMENTS, field_name='name')


def ensure_demo_cats(users, achievements):
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
