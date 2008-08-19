from django.contrib import admin

from models import User, PlaceType, Place

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)

class PlaceTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(PlaceType, PlaceTypeAdmin)

class PlaceAdmin(admin.ModelAdmin):
    raw_id_fields = ['user', 'city']
admin.site.register(Place, PlaceAdmin)
