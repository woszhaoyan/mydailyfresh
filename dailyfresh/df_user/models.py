from __future__ import unicode_literals
from django.db import models

from django.db import models

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=20)
    user_passwd = models.CharField(max_length=40)
    user_email = models.CharField(max_length=40)
    user_addr = models.CharField(max_length=100, default='')
    user_phone = models.CharField(max_length=11, default='')

    def __unicode__(self):
        return self.user_name


class ReceiveInfo(models.Model):
    receive_name = models.CharField(max_length=20)
    receive_addr = models.CharField(max_length=100)
    receive_phone = models.CharField(max_length=11)
    receive_user = models.ForeignKey(User)

    def __unicode__(self):
        return self.receive_name