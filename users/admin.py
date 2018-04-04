from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, UserProfile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

admin.site.register(CustomUser, CustomUserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('user', 'dob', 'public_token', 'access_token', 'item_id',)
    ordering = ('user',)
    list_select_related = ('user',)


admin.site.register(UserProfile, UserProfileAdmin)


class UserProfileAdminInline(admin.TabularInline):
    model = UserProfile
