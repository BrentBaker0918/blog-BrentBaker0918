from django.contrib import admin
from . import CreditRating
# Register your models here.
@admin.register(models.Model)
class CreditRating(admin.ModelAdmin):
    list_display = (
        'user',
        'score',
    )
    prepopulated_fields = {'slug': ('user',)}
