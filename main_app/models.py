from django.db import models
from django.db.models.fields import CharField
from django.urls import reverse

# Create your models here.


class Activity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Trail(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    length = models.IntegerField()
    activities = models.ManyToManyField(Activity)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'trail_id': self.id})
