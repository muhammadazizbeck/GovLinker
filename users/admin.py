from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username','first_name','last_name','email','age','city','region','countryside','is_staff','is_active')
    search_fields = ('username','email', 'first_name', 'last_name', 'city')
    list_filter = ('region', 'countryside', 'is_active')


    fieldsets = UserAdmin.fieldsets + (
        (None,{'fields':('age','city','region','countryside')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None,{'fields':('age','city','region','countryside')}),
    )

admin.site.register(CustomUser,CustomUserAdmin)