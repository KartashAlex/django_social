from django.contrib import admin

from models import User, PlaceType, Place, PlaceTemplate, NetGroup as Group, Friend, Event

class EventsAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'user', 'group', 'type', 'sent']
    search_fields=['from_user__username', 'user__username']
admin.site.register(Event, EventsAdmin)

class UserAdmin(admin.ModelAdmin):
    search_fields=['username']
    raw_id_fields = ['country', 'city']
admin.site.register(User, UserAdmin)

class FriendAdmin(admin.ModelAdmin):
    raw_id_fields = ['friend', 'friend_of']
admin.site.register(Friend, FriendAdmin)

class PlaceTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(PlaceType, PlaceTypeAdmin)

class PlaceTemplateAdmin(admin.ModelAdmin):
    search_fields=['translations__name']
    raw_id_fields = ['city']
    list_display = ['city', 'name_ru']
admin.site.register(PlaceTemplate, PlaceTemplateAdmin)

class PlaceAdmin(admin.ModelAdmin):
    raw_id_fields = ['user', 'template']
admin.site.register(Place, PlaceAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'admins_list', 'members_count']
    raw_id_fields = ['owner']
admin.site.register(Group, GroupAdmin)
