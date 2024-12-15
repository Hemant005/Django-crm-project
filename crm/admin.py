from django.contrib import admin
from . import models
from .models import UserProfile


# Register your models here.
admin.site.register(models.Client)
admin.site.register(models.Opportunity)
admin.site.register(models.Product)
admin.site.register(models.Invoice)
admin.site.register(models.Shipping_Receipt)

class UserProfileAdmin(admin.ModelAdmin):
    # Display user, department, phone, gender, and age in the admin list
    list_display = ('user','get_first_name', 'get_last_name','department','role', 'phone', 'gender', 'age')

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'  # Column header in the admin interface

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'  

    # Only superusers can add or edit profiles
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if obj is not None and request.user.is_superuser:
            return True
        return False

admin.site.register(UserProfile, UserProfileAdmin)

from django import forms

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'department', 'phone', 'gender', 'age']  # Specify all fields


