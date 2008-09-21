from django.contrib import admin

from models import Post, AdCategory

class PostAdmin(admin.ModelAdmin):
    list_display = ['added', 'subject', 'type']
admin.site.register(Post, PostAdmin)

class AdCatAdmin(admin.ModelAdmin):
    list_display = ['name', ]
admin.site.register(AdCategory, AdCatAdmin)

