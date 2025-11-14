from django.db import migrations, models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import cats.models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='achievement',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='achievementcat',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='achievementcat',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cat',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cat',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='achievement',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='achievementcat',
            name='achievement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cats.achievement'),
        ),
        migrations.AlterField(
            model_name='achievementcat',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cats.cat'),
        ),
        migrations.AlterField(
            model_name='cat',
            name='achievements',
            field=models.ManyToManyField(related_name='cats', through='cats.AchievementCat', to='cats.Achievement'),
        ),
        migrations.AlterField(
            model_name='cat',
            name='birth_year',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(django.utils.timezone.now().year)]),
        ),
        migrations.AlterField(
            model_name='cat',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=cats.models.cat_image_upload_path),
        ),
        migrations.AlterField(
            model_name='cat',
            name='name',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterUniqueTogether(
            name='achievementcat',
            unique_together={('achievement', 'cat')},
        ),
    ]
