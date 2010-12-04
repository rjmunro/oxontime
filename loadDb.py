#!/usr/bin/python
""" To make this run, you need to set the environment with:
export DJANGO_SETTINGS_MODULE=oxontime.settings
export PYTHONPATH=/home/rjmunro/oxontime-bus-stuff
"""

from oxontime.busses.models import *
import urllib
import datetime

baseUrl = "http://www.oxontime.com/pda/mainfeed.asp?type=INIT&mapLevel=3&SessionID=%s&systemid=35&stopSelected=0"

def addTile(num):
  updated = datetime.datetime.now()
  # Download tile
  file = urllib.urlopen(baseUrl % num)
  try:
    region = Region.objects.get(id=num)
    region.last_updated = updated
    region.updated_count = (region.updated_count or 0) + 1
  except Region.DoesNotExist:
    region = Region.objects.create(id=num,last_updated = updated, updated_count = 1)
  busses = []
  for line in file:
    line=line.strip()
    if line:
      (null,vehicle,null,service,null,coords) = line.split('|')
      y,x = map(int, coords.split(',')) # perverse
      bus = Bus(region=region,updated=updated,service=service,vehicle=vehicle,x=x,y=y)
      bus.save()
      busses.append((bus.service,bus.vehicle))
  region.save()
  return (region.x,region.y), busses


# The first tile is 331
# The most interesting tile is 2561
# The last tile is 4323

queries = ("""-- Fetch the busses that have recently disappeard
   select * from busses_region as br1 where (x,y) in
     (select x+"newX",y+"newY" from busses_region,silly where id in 

        (select region_id
          from busses_bus as b1 where
          (updated,vehicle) in (select max(updated),vehicle from busses_bus as b2 group by vehicle)
          and (updated,region_id) not in (select last_updated,id from busses_region as br3)
          and updated>now()- interval '15 minutes'
        )
      )
      and last_updated<now()-interval '2 minutes'
      order by x,y
   """,
   """-- Fetch the oldest tiles with age multiplied by historical number of busses
   select busses_region.id, (now()-last_updated-'00:02:00') as age from busses_region inner join
        (select region_id,count(*) as count from busses_bus 
          where updated = (select last_updated from busses_region where id=region_id)
          group by region_id order by count desc
        ) as counts
        on counts.region_id=busses_region.id
        order by (now()-last_updated-'00:02:00')*(coalesce(count,0)+1) desc limit 10
      """)

if __name__=="__main__":
  from time import sleep
  import sys
  if len(sys.argv)>1:
    for i in sys.argv[1:]:
      print i, addTile(int(i)) or ''
      sleep(1)
  else:
    from django.db import connection
    cursor = connection.cursor()
    nextQuery = 0
    while 1:
      nextQuery = (1,0)[nextQuery]
      print "Fetching batch '%s'" % ('the one that got away','oldest unchecked')[nextQuery]
      cursor.execute(queries[nextQuery],[])
      results = cursor.fetchall()
      for r in results:
        result = addTile(r[0])
        print r[0], result[0], result[1] or ''
        sleep(1)
