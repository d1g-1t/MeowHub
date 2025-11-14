from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

User = get_user_model()


def cat_image_upload_path(instance, filename):
    return f'cats/images/{instance.owner_id}/{filename}'


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Achievement(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class CatQuerySet(models.QuerySet):
    def with_relations(self):
        return self.select_related('owner').prefetch_related('achievements')


class CatManager(models.Manager):
    def get_queryset(self):
        return CatQuerySet(self.model, using=self._db)

    def with_relations(self):
        return self.get_queryset().with_relations()


class Cat(TimeStampedModel):
    name = models.CharField(max_length=32)
    color = models.CharField(max_length=16)
    birth_year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(timezone.now().year),
        ]
    )
    owner = models.ForeignKey(User, related_name='cats', on_delete=models.CASCADE)
    achievements = models.ManyToManyField(
        Achievement,
        through='AchievementCat',
        related_name='cats',
    )
    image = models.ImageField(upload_to=cat_image_upload_path, null=True, blank=True, default=None)

    objects = CatManager()

    class Meta:
        ordering = ('-created_at', 'name')

    def __str__(self):
        return self.name


class AchievementCat(TimeStampedModel):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('achievement', 'cat')
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.achievement} {self.cat}'
