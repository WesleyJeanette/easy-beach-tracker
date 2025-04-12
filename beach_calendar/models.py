from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# A model to represent a beach calendar entry
class BeachCalendarEntry(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Link each entry to a user
    date = models.DateField()
    beach = models.CharField(max_length=100)
    walked = models.BooleanField(default=False)
    time_of_visit = models.TimeField(blank=True, null=True)
    tide = models.FloatField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    water_conditions = models.CharField(max_length=100, blank=True, null=True)
    weather_conditions = models.CharField(max_length=100, blank=True, null=True)
    air_temperature = models.FloatField(blank=True, null=True)
    water_temperature = models.FloatField(blank=True, null=True)
    swam = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.beach} on {self.date} by {self.user.username}"