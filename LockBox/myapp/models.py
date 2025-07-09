
# Create your models here.
from django.db import models

TIME_ZONE = 'Asia/Kolkata'

class UserProfile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=100)
    full_name = models.CharField(max_length=150, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    generatecode = models.CharField(max_length=12,unique=True,null=True,blank=True)
    profilepicture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.username

class UserCodeMatch(models.Model):
    logged_in_username = models.CharField(max_length=100)
    entered_code = models.CharField(max_length=12)
    matched_username = models.CharField(max_length=100)
    matched_user_email = models.EmailField()
    matched_user_profilepicture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    matched_user_full_name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.logged_in_username} matched with {self.matched_username} using code {self.entered_code}"
    



class UploadedFile(models.Model):
    username = models.CharField(max_length=255)  # Link file to username
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploaded_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.filename}"


