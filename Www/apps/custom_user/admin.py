from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Www.apps.custom_user.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super(UserAdmin, self).get_fieldsets(request, obj))
        # update the `fieldsets` with your specific fields
        fieldsets.append(
            ('Informacion Laboral', {
                'fields': ('type', 'avatar',)
            })
        )
        return fieldsets
