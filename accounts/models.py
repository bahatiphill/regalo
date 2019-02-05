from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator

from django.contrib.auth.models import AbstractUser

# Create your models here.



class Churches(AbstractUser):

    username = models.CharField(unique=True, max_length=100) #this was because of Abstractbaseuser
    #name = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    slug = models.SlugField(unique=True)
    location = models.CharField(max_length=20)
    umushumba = models.CharField(max_length=20, blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['location', 'username']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
