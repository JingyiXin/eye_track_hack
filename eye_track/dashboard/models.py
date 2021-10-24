from django.db import models
from django.urls import reverse

class DashboardDriver(models.Model):
    id = models.TextField(primary_key=True)  # This field type is a guess.
    time_blinking = models.FloatField()  # This field type is a guess.
    too_sleepy = models.BooleanField()  # This field type is a guess.
    username = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'dashboard_driver'

class Driver(models.Model):
    # id = models.TextField(primary_key=True)
    username = models.CharField(max_length=200, primary_key=True)
    time_blinking = models.FloatField()
    too_sleepy = models.BooleanField()

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})
    