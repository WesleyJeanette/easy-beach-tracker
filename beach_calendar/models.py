from django.db import models

# Create your models here.
# A model to represent a beach calendar entry
class BeachCalendarEntry(models.Model):
    date = models.DateField()
    beach = models.CharField(max_length=100)
    walked = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    water_conditions = models.CharField(max_length=100, blank=True, null=True)
    weather_conditions = models.CharField(max_length=100, blank=True, null=True)
    air_temperature = models.SmallIntegerField(blank=True, null=True)
    water_temperature = models.SmallIntegerField(blank=True, null=True)
    swam = models.BooleanField(default=False)