from django.contrib import admin
from comics.models import Comic, Comment

class ComicAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search = ('title')
    date_hierarchy = 'date'
    prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comic', 'name', 'email', 'date', 'approved')
    date_heirarchy = 'date'

admin.site.register(Comic, ComicAdmin)
admin.site.register(Comment, CommentAdmin)
