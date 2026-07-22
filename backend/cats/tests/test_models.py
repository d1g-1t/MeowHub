from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Achievement, AchievementCat, Cat

User = get_user_model()


class AchievementModelTests(TestCase):
    def setUp(self):
        self.achievement = Achievement.objects.create(name='Мастер мурчания')

    def test_achievement_str(self):
        self.assertEqual(str(self.achievement), 'Мастер мурчания')

    def test_achievement_unique_name(self):
        with self.assertRaises(Exception):
            Achievement.objects.create(name='Мастер мурчания')

    def test_achievement_ordering(self):
        Achievement.objects.create(name='Акробат скакалок')
        Achievement.objects.create(name='Чемпион по сну')
        names = list(Achievement.objects.values_list('name', flat=True))
        self.assertEqual(names, ['Акробат скакалок', 'Мастер мурчания', 'Чемпион по сну'])


class CatModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@meowhub.local',
            password='testpass123',
        )
        self.achievement = Achievement.objects.create(name='Королева невесомости')

    def test_cat_creation(self):
        cat = Cat.objects.create(
            name='Луна',
            color='white',
            birth_year=2020,
            owner=self.user,
        )
        self.assertEqual(cat.name, 'Луна')
        self.assertEqual(cat.color, 'white')
        self.assertEqual(cat.birth_year, 2020)
        self.assertEqual(cat.owner, self.user)

    def test_cat_str(self):
        cat = Cat.objects.create(
            name='Марсик',
            color='darkorange',
            birth_year=2018,
            owner=self.user,
        )
        self.assertEqual(str(cat), 'Марсик')

    def test_cat_future_birth_year_raises_error(self):
        future_year = datetime.now().year + 1
        cat = Cat(
            name='Будущий',
            color='black',
            birth_year=future_year,
            owner=self.user,
        )
        with self.assertRaises(ValidationError):
            cat.full_clean()

    def test_cat_birth_year_below_min_raises_error(self):
        cat = Cat(
            name='Древний',
            color='gray',
            birth_year=1899,
            owner=self.user,
        )
        with self.assertRaises(ValidationError):
            cat.full_clean()

    def test_cat_with_achievements(self):
        cat = Cat.objects.create(
            name='Йода',
            color='darkgrey',
            birth_year=2013,
            owner=self.user,
        )
        cat.achievements.add(self.achievement)
        self.assertEqual(cat.achievements.count(), 1)
        self.assertEqual(cat.achievements.first().name, 'Королева невесомости')

    def test_cat_image_upload_path(self):
        cat = Cat.objects.create(
            name='Светляк',
            color='whitesmoke',
            birth_year=2021,
            owner=self.user,
        )
        expected_path = f'cats/images/{self.user.pk}/test.jpg'
        path = cat.image.field.upload_to(cat, 'test.jpg')
        self.assertEqual(path, expected_path)

    def test_cat_ordering(self):
        Cat.objects.create(name='Астра', color='white', birth_year=2022, owner=self.user)
        Cat.objects.create(name='Зефир', color='bisque', birth_year=2018, owner=self.user)
        names = list(Cat.objects.values_list('name', flat=True))
        self.assertEqual(names[0], 'Зефир')
        self.assertEqual(names[1], 'Астра')

    def test_cat_with_relations_queryset(self):
        Cat.objects.create(
            name='Радар',
            color='black',
            birth_year=2016,
            owner=self.user,
        )
        cats = Cat.objects.with_relations()
        with self.assertNumQueries(2):
            for cat in cats:
                _ = cat.owner.username
                _ = list(cat.achievements.all())


class AchievementCatThroughTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser2',
            email='test2@meowhub.local',
            password='testpass123',
        )
        self.achievement = Achievement.objects.create(name='Инженер по коробкам')
        self.cat = Cat.objects.create(
            name='Дымок',
            color='gray',
            birth_year=2014,
            owner=self.user,
        )

    def test_achievement_cat_str(self):
        through = AchievementCat.objects.create(
            achievement=self.achievement,
            cat=self.cat,
        )
        self.assertIn('Инженер по коробкам', str(through))
        self.assertIn('Дымок', str(through))

    def test_achievement_cat_unique_constraint(self):
        AchievementCat.objects.create(achievement=self.achievement, cat=self.cat)
        with self.assertRaises(Exception):
            AchievementCat.objects.create(achievement=self.achievement, cat=self.cat)
