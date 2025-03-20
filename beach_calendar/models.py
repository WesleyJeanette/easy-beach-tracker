from django.db import models

# Create your models here.
# A model to represent a beach calendar entry
class BeachCalendarEntry(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    beach = models.CharField(max_length=100)
    walked = models.BooleanField(default=False)
    time_of_visit = models.TimeField(blank=True, null=True)
    tide = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    water_conditions = models.CharField(max_length=100, blank=True, null=True)
    weather_conditions = models.CharField(max_length=100, blank=True, null=True)
    air_temperature = models.SmallIntegerField(blank=True, null=True)
    water_temperature = models.SmallIntegerField(blank=True, null=True)
    swam = models.BooleanField(default=False)