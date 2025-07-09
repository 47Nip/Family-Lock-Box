

# Register your models here.
from django.contrib import admin
from .models import UploadedFile, UserProfile,UserCodeMatch

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone')  # Adjust fields as per your model
    search_fields = ('username', 'email', 'phone')

@admin.register(UploadedFile)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'file', 'uploaded_at')
    search_fields = ('filename', 'file')

@admin.register(UserCodeMatch)
class UserCodeMatchAdmin(admin.ModelAdmin):
    list_display = ('logged_in_username', 'entered_code', 'matched_username')
    search_fields = ('logged_in_username', 'entered_code', 'matched_username')