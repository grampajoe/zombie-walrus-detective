from django.contrib import admin
from comics.models import Comic

class ComicAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search = ('title')
    date_hierarchy = 'date'

admin.site.register(Comic, ComicAdmin)
