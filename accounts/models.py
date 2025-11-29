from django.db import models
from django.utils import timezone


# Create your models here.
class UserInfo(models.Model):
    user_id = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=64)
    user_avatar = models.TextField()
    app_name = models.CharField(max_length=10)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    vip_time = models.DateTimeField(default=timezone.now)
    contact_ad = models.CharField(max_length=50)
    pwd = models.CharField(max_length=32)


class CAPTCHA(models.Model):
    contact_ad = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now=True)
    target_type = models.CharField(max_length=10)
    code = models.CharField(max_length=6)


class RestCount(models.Model):
    user_id = models.CharField(max_length=100)
    rest_count = models.IntegerField(default=20)
    app_name = models.CharField(max_length=10)


class Meta:
    db_table = 'user_info'
