from django.contrib import admin

from .models import Achievement, AchievementCat, Cat


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'owner', 'birth_year', 'color')
	search_fields = ('name', 'owner__username')
	list_filter = ('color',)
	ordering = ('-created_at',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')
	search_fields = ('name',)
	ordering = ('name',)


@admin.register(AchievementCat)
class AchievementCatAdmin(admin.ModelAdmin):
	list_display = ('id', 'achievement', 'cat')
	autocomplete_fields = ('achievement', 'cat')
