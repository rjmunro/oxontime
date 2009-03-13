#!/bin/python
from oxontime.busses.models import *
import urllib
import datetime

baseUrl = "http://www.oxontime.com/pda/menu.asp?sysid=35&mapid=%s&maplevel=3&naptan=0"
function = ""
def addTile(num):
  # Download tile
  file = urllib.urlopen(baseUrl % num)
  startregion = Region.objects.get(id=num)
  for line in file:
    line=line.strip()
    if line.startswith("function map"):
      function = line.split('map',1)[1].split('(')[0]
    if line.startswith("top.location.href ="):
      print line
      dictParts = [i.split('=',1) for i in line.split('&')]
      print dictParts
      tile = dict(dictParts)['mapid']
      newregion = Region.objects.get(id=tile)
      if function == "Left":
        newregion.x = startregion.x+1
        newregion.y = startregion.y
      if function == "Right":
        newregion.x = startregion.x-1
        newregion.y = startregion.y
      if function == "Up":
        newregion.x = startregion.x
        newregion.y = startregion.y+1
      if function == "Down":
        newregion.x = startregion.x
        newregion.y = startregion.y-1
      newregion.save()

# The first tile is 331
# The most interesting tiles are 2561 & 2598
# The last tile is 4323
if __name__=="__main__":
  from time import sleep
  import sys
  if len(sys.argv)>1:
    for i in sys.argv[1:]:
      addTile(int(i))
  else:
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("""select id from (
    select *, (select count(*) from busses_region as b2 where (b2.y=b1.y and (b2.x+1=b1.x or b2.x-1=b1.x)) or (b2.x=b1.x and (b2.y+1=b1.y or b2.y-1=b1.y))) as count from busses_region as b1
     where x is not null
       and y is not null
         ) as t
           where (y %% 2 = 0
             or x %% 2 = 0)
               and count<4
                order by id""",[])
    results = cursor.fetchall()
    for r in results:
      addTile(r[0])
