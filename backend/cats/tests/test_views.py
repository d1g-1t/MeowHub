from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Achievement, Cat

User = get_user_model()


class HealthCheckTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_health_check_returns_ok(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'status': 'ok'})


class CatListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='catowner',
            email='owner@meowhub.local',
            password='testpass123',
        )
        self.achievement = Achievement.objects.create(name='Чемпион по сну')
        Cat.objects.create(name='Луна', color='white', birth_year=2020, owner=self.user)
        Cat.objects.create(name='Марсик', color='darkorange', birth_year=2018, owner=self.user)

    def test_list_returns_paginated_response(self):
        response = self.client.get('/api/cats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(data['count'], 2)
        self.assertEqual(len(data['results']), 2)

    def test_list_ordered_by_created_at_desc(self):
        response = self.client.get('/api/cats/')
        results = response.json()['results']
        self.assertEqual(results[0]['name'], 'Марсик')
        self.assertEqual(results[1]['name'], 'Луна')

    def test_list_includes_age_field(self):
        response = self.client.get('/api/cats/')
        cat = response.json()['results'][0]
        self.assertIn('age', cat)
        self.assertIsInstance(cat['age'], int)


class CatDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='detailuser',
            email='detail@meowhub.local',
            password='testpass123',
        )
        self.cat = Cat.objects.create(
            name='Орион',
            color='darkgrey',
            birth_year=2019,
            owner=self.user,
        )

    def test_detail_returns_cat(self):
        response = self.client.get(f'/api/cats/{self.cat.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'Орион')

    def test_detail_non_existent_returns_404(self):
        response = self.client.get('/api/cats/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CatCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='creator',
            email='creator@meowhub.local',
            password='testpass123',
        )

    def test_create_requires_authentication(self):
        response = self.client.post('/api/cats/', {
            'name': 'Астра',
            'color': '#DCDCDC',
            'birth_year': 2022,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_with_authentication(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/cats/', {
            'name': 'Астра',
            'color': '#DCDCDC',
            'birth_year': 2022,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['name'], 'Астра')
        self.assertEqual(response.json()['owner'], self.user.pk)

    def test_create_with_achievements(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/cats/', {
            'name': 'Йода',
            'color': '#A9A9A9',
            'birth_year': 2013,
            'achievements': [{'name': 'Мастер мурчания'}],
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Achievement.objects.filter(name='Мастер мурчания').exists())
        cat = Cat.objects.get(pk=response.json()['id'])
        self.assertEqual(cat.achievements.count(), 1)

    def test_create_with_duplicate_achievements_returns_error(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/cats/', {
            'name': 'Дубль',
            'color': '#000000',
            'birth_year': 2020,
            'achievements': [
                {'name': 'Тестовое'},
                {'name': 'Тестовое'},
            ],
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CatUpdateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@meowhub.local',
            password='testpass123',
        )
        self.other = User.objects.create_user(
            username='other',
            email='other@meowhub.local',
            password='testpass123',
        )
        self.cat = Cat.objects.create(
            name='Зефир',
            color='bisque',
            birth_year=2018,
            owner=self.owner,
        )

    def test_update_requires_authentication(self):
        response = self.client.patch(f'/api/cats/{self.cat.pk}/', {
            'name': 'Обновлённый',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_as_owner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(f'/api/cats/{self.cat.pk}/', {
            'name': 'Обновлённый Зефир',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cat.refresh_from_db()
        self.assertEqual(self.cat.name, 'Обновлённый Зефир')


class CatDeleteTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(
            username='deleter',
            email='deleter@meowhub.local',
            password='testpass123',
        )
        self.cat = Cat.objects.create(
            name='Туман',
            color='gray',
            birth_year=2011,
            owner=self.owner,
        )

    def test_delete_requires_authentication(self):
        response = self.client.delete(f'/api/cats/{self.cat.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_as_owner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(f'/api/cats/{self.cat.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cat.objects.filter(pk=self.cat.pk).exists())


class AchievementReadOnlyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.achievement = Achievement.objects.create(name='Страж подоконника')

    def test_list_achievements(self):
        response = self.client.get('/api/achievements/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)

    def test_create_achievement_not_allowed(self):
        response = self.client.post('/api/achievements/', {
            'name': 'Новое достижение',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
