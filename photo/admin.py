from django.contrib import admin

from models import Photo, Album

class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'group']
    raw_id_fields = ['group', 'user']
admin.site.register(Album, AlbumAdmin)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'album']
    raw_id_fields = ['album']
admin.site.register(Photo, PhotoAdmin)

