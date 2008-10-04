from django.contrib import admin

from models import User, PlaceType, Place, NetGroup as Group, Friend

class UserAdmin(admin.ModelAdmin):
    search_fields=['username']
admin.site.register(User, UserAdmin)

class FriendAdmin(admin.ModelAdmin):
    raw_id_fields = ['friend', 'friend_of']
admin.site.register(Friend, FriendAdmin)

class PlaceTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(PlaceType, PlaceTypeAdmin)

class PlaceAdmin(admin.ModelAdmin):
    raw_id_fields = ['user', 'city']
admin.site.register(Place, PlaceAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'admins_list', 'members_count']
    raw_id_fields = ['owner']
admin.site.register(Group, GroupAdmin)
