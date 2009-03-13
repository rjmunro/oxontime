from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from models import *
from datetime import datetime,date
from django.conf import settings

xsize = 69
ysize = 92
def home(request):
  table = '<table>\n'
  table += "  <tr><td></td>\n"
  for x in range(1,xsize+1):
    table += '    <td class="h">%s</td>\n' % (x)
  table += "  </tr>\n"
  for y in range(1,ysize+1):
    table += "  <tr><td>%s</td>\n" % (y)
    for x in range(1,xsize+1):
      try:
        r = Region.objects.get(x=x,y=y)
        c = r.bus_set.filter(updated=r.last_updated).count()
        c2 = r.bus_set.count()
        table += '    <td class="c%s">%s<br />%s</td>\n' % (c2, c,r.id)
      except Region.DoesNotExist:
        table += '    <td class="empty">&nbsp;</td>\n'
    table += "  </tr>\n"
  table += "</table>\n"
  return render_to_response('home.fbml', {'table': table})

