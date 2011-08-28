from django.contrib import admin
from comics.models import Comic, Comment
import os

class ComicAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search = ('title')
    date_hierarchy = 'date'
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        base, ext = os.path.splitext(obj.image.name)
        old_file = obj.image.path[:]
        obj.image.save(obj.slug + ext, obj.image)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comic', 'name', 'email', 'date', 'approved')
    date_heirarchy = 'date'

admin.site.register(Comic, ComicAdmin)
admin.site.register(Comment, CommentAdmin)
