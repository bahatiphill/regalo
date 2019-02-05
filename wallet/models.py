from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator

from accounts.models import Churches

# Create your models here.

class Abatuye(models.Model):

    name = models.CharField(max_length=20, blank=True, null=True)
    amount = models.IntegerField(blank=False, validators=[MaxValueValidator(200000), MinValueValidator(100)])
    to_church = models.ForeignKey(Churches, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, blank=False)
    location = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, unique=True)
    reason = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return self.name



class SentPayments(models.Model):

    church = models.ForeignKey(Churches, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length = 10)
    amount = models.IntegerField()
    transaction_id = models.CharField(max_length = 100)
    success = models.BooleanField(default=False)
    #reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return self.phone_number



class Ikofi(models.Model):
    church = models.OneToOneField(Churches,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    class Meta:
        ordering = ['amount']

    def __str__(self):
        return self.church.username
