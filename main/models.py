# models.py

from django.db import models
import uuid

class UserProfile(models.Model):
    uid = models.CharField(max_length=255, unique=True)  
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15) 
    lvl = models.CharField(max_length=10, default='1')  
    time = models.CharField(max_length=100,default='0')  
    chances_left = models.CharField(max_length=10, default='5') 
    started = models.CharField(max_length=5, default='0') 
    digits = models.CharField(max_length=1000,default="NIL")
    update = models.CharField(max_length=5,default="1")

    def __str__(self):
        return f"{self.name} - {self.phone}"
    @classmethod
    def reset_all_updates(cls):
        cls.objects.update(update='0')

    @classmethod
    def set_all_updates(cls):
        cls.objects.update(update='1')
    
class leaderboard(models.Model):
    rank=models.CharField(max_length=3)
    name=models.CharField(max_length=100)
    level=models.CharField(max_length=10)
    avg_time=models.CharField(max_length=30)
    eliminated=models.CharField(max_length=10)

    def __str__(self):
        return f"self.name"

class GuestProfile(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Auto-generated UUID
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.name} - {self.email}"

    @classmethod
    def reset_all_profiles(cls):
        cls.objects.update(name='', email='')

    @classmethod
    def delete_all_profiles(cls):
        cls.objects.all().delete()