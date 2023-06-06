from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from MyApp.models import UserProfileModel, Results, Supervisor, InputModel

from MyApp.forms import NewUserForm, UpdateProfileForm
from django.contrib.auth.models import Group


class CustomUserAdmin(UserAdmin):
    add_form = NewUserForm
    form = UpdateProfileForm
    model = UserProfileModel
    list_display = ("username", "first_name", "last_name", "access_level","is_staff", "is_active",)
    list_filter = ("first_name", "last_name", "access_level", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "phone_number", "gender", "first_name", "middle_name",
                           "last_name", "tokens", "access_level", "uid")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "phone_number", "password1", "password2"
                       )}
         ),
    )
    search_fields = ("username", "last_name", )
    ordering = ("is_staff", "is_active", "access_level", "last_name")


# Register your models here.
admin.site.register(UserProfileModel, CustomUserAdmin)
admin.site.register(Results)
admin.site.register(Supervisor)
admin.site.register(InputModel)

admin.site.unregister(Group)
