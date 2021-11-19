from datetime import timedelta
from django.utils import timezone
from django.contrib import admin
from activities.models import Event
from users.models import User
from django.contrib.auth.models import Permission, Group


class UsersAdmin(admin.ModelAdmin):
    list_display = search_fields = ('is_active', 'username', 'first_name', 'last_name', 'email', 'date_joined',
                                    'last_login', 'modified', 'events_last_30_days')
    list_filter = ('is_active', 'first_name', 'last_name', 'date_joined', 'last_login', 'modified')

    def events_last_30_days(self, obj):
        last_30_days = [timezone.now() - timedelta(days=30), timezone.now()]
        return Event.objects.filter(users=obj, datetime__range=last_30_days).count()


class GroupsAdmin(admin.ModelAdmin):
    list_display = search_fields = ('name', 'members', 'permissions_assigned')

    def members(self, obj):
        return User.objects.filter(groups__name=obj.name).count()

    def permissions_assigned(self, obj):
        return obj.permissions.all().count()


class PermissionsAdmin(admin.ModelAdmin):
    list_display = search_fields = ('codename', 'name', 'content_type')
    list_filter = ('content_type',)


admin.site.unregister(Group)
admin.site.register(User, UsersAdmin)
admin.site.register(Permission, PermissionsAdmin)
admin.site.register(Group, GroupsAdmin)
