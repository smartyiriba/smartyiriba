from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
@admin.register(User)
class BusinessUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Profil client', {'fields': ('customer_type', 'organization', 'phone', 'address', 'country', 'language')}),)
