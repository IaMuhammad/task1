from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'

    role = models.CharField(max_length=55, choices=Role.choices, default=Role.ADMIN)


class Stadium(models.Model):
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=255)
    price = models.DecimalField(verbose_name='Price of per hour', decimal_places=2, max_digits=10)
    address = gis_models.PointField()
    images = ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True)


class Order(models.Model):
    stadium = models.ForeignKey('apps.Stadium', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    phone_number = models.CharField(max_length=255)
    user = models.ForeignKey('apps.User', on_delete=models.CASCADE)


class Payment(models.Model):
    order = models.ForeignKey('apps.Order', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_amount = models.DecimalField(decimal_places=2, max_digits=10)
