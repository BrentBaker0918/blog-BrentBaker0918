from django.contrib import admin
from . import models
# Register your models here.
class CommentInline(admin.TabularInline):
    model = models.Comment
    fields= (
        'name',
        'email',
        'text',
        'approved',
    )
    readonly_fields = (
        'name',
        'email',
        'text',
    )


class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
    list_display = (
        'title',
        'author',
        'created',
        'updated',

    )

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )
    list_filter = ('status', 'topics')
    prepopulated_fields = {'slug':('title',)}

admin.site.register(models.Post, PostAdmin)

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'name',
        'text',
        'approved',
        'created',
        'updated',
    )
    prepopulated_fields = {'slug': ('name',)}
