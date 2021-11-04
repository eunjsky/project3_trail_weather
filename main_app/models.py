from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Activity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Weather(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Trail(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=2, default="CA")
    description = models.CharField(max_length=100)
    length = models.IntegerField()
    activities = models.ManyToManyField(Activity)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'trail_id': self.id})
