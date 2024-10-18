# models.py

from django.db import models

class UserProfile(models.Model):
    uid = models.CharField(max_length=255, unique=True)  
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15) 
    lvl = models.CharField(max_length=10, default='1')  
    time = models.CharField(max_length=100,default='0')  
    chances_left = models.CharField(max_length=10, default='5') 
    started = models.CharField(max_length=5, default='0') 
    digits = models.CharField(max_length=1000,default="NIL")

    def __str__(self):
        return f"{self.name} - {self.phone}"
    
class leaderboard(models.Model):
    rank=models.CharField(max_length=3)
    name=models.CharField(max_length=100)
    level=models.CharField(max_length=10)
    avg_time=models.CharField(max_length=30)
    eliminated=models.CharField(max_length=10)

    def __str__(self):
        return f"self.name"
