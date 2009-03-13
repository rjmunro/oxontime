from django.db import models

# Create your models here.
class Region(models.Model):
  id = models.IntegerField(primary_key=True)
  last_updated = models.DateTimeField()
  updated_count = models.IntegerField(default=0)
  x = models.IntegerField()
  y = models.IntegerField()
  used = models.BooleanField()

class Bus(models.Model):
  region = models.ForeignKey(Region)
  vehicle = models.IntegerField()
  service = models.CharField(max_length=200)
  updated = models.DateTimeField()
  x = models.IntegerField()
  y = models.IntegerField()
