from django.contrib.gis.geos import Point
from django.contrib.gis.db import models

OFFSET_X, OFFSET_Y = (411026.07074929884, 131988.22506181369)
OFFSET_X, OFFSET_Y = (415026.07074929884, 256088.22506181369)
OFFSET_X, OFFSET_Y = (414721.07074929884, 256043.22506181369)
SCALE_X, SCALE_Y = (2.2004998202088553, 2.1987468516915558)

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

  location = models.PointField(srid=27700)

  def save(self, *args, **kwargs):
      x = OFFSET_X + (self.region.x * 418 + self.x) * SCALE_X
      y = OFFSET_Y - (self.region.y * 418 + self.y) * SCALE_Y

      self.location = Point(x, y, srid=27700)

      super(Bus, self).save(*args, **kwargs)
