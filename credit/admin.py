from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.CreditRating)
class CreditRatingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'score',
    )
    prepopulated_fields = {'slug': ('user',)}
