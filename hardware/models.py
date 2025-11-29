from pyexpat import model
from subprocess import getoutput
from django.db import models

# Create your models here.
class UserCollection(models.Model):
    user_id = models.CharField(max_length=100)
    collect_name=models.CharField(max_length=100)
    cpu_id=models.CharField(max_length=100)
    gpu_id=models.CharField(max_length=100)
    disk_count=models.CharField(max_length=100)
    cpu_name=models.CharField(max_length=100,default='')
    gpu_name=models.CharField(max_length=100,default='')
    total_powerConsumption=models.CharField(max_length=100,default='')
    supportedMotherboard=models.CharField(max_length=100,default='')
    suggestMotherboard=models.CharField(max_length=100,default='')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_collection'