from django.contrib import admin
from comics.models import Comic
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
        os.unlink(old_file)

admin.site.register(Comic, ComicAdmin)
