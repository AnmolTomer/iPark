from django.db import models
""" This we are importing so that django doen not give any exception
    while we change the date time DateField"""
from django.utils.timezone import datetime

from django.contrib.auth.models import User
# Create your models here.

class Car(models.Model):
    number_plate  = models.CharField(max_length = 11,unique=True,default=None)
    entry_time = models.DateTimeField(default = datetime.now )
    service_used = models.IntegerField(default = 0)
    name = models.CharField(max_length = 20,default=None,null=True)
    email = models.EmailField(max_length =100,default=None,null=True)
    phone = models.IntegerField(default=None,null=True)
    status = models.CharField(max_length = 50, choices= (
        ('Allowed', 'Allowed'),
        ('Not Allowed', 'Not Allowed')
    ) )
    sl_no = models.ForeignKey('Contact' , on_delete=models.SET_NULL ,blank = True,  null=True)
    def __str__(self):
        return self.number_plate

class Contact(models.Model):
    manager = models.ForeignKey(User , on_delete=models.CASCADE , default=None)
    sl_no = models.CharField(max_length = 20,unique=True)
    number_plate = models.ForeignKey(Car , on_delete=models.SET_NULL ,blank = True,  null=True)
    info = models.CharField(max_length = 50, choices= (
        ('Normal Customer', 'Normal Customer'),
        ('Premium Customer', 'Premium Customer')
    ) )
    avalibility = models.CharField(max_length = 50, choices= (
        ('empty', 'Empty'),
        ('occupied', 'Occupied')
    ) )

    # for image we need to install pillow so we do :: pip install pillow
    image = models.ImageField(upload_to = 'image/', blank = True)
    # Old - date_added = models.DateField(auto_now_add = True)
    """ NEW """
    date_added = models.DateTimeField(default = datetime.now )

    def __str__(self):
        return self.sl_no

class Meta:
    ordering = ['-id']
