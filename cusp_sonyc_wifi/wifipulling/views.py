# Defines the controllers for the wifipulling component: tile, grey tile
# and API.

from django.shortcuts import render
from django.http import HttpResponse
from ingestion.models import WifiScan
import simplejson as json
import datetime
import time
import os
from django.db import connection
import math
import pandas as pd
import numpy as np
from scipy.misc import imresize
from matplotlib import cm
from PIL import Image
from lib import generateTile, getPath, getGreyPath
from django.conf import settings

col_name = {'idx':1, 'lat':1, 'lng':1, 'acc':1, 'altitude':1, 'time':1, 'device_mac':1, 'app_version':1, 'droid_version':1, 'device_model':1, 'ssid':1, 'bssid':1, 'caps':1, 'level':1, 'freq':1}

# ## Heatmap Tile API

# Return a heatmap tile for the given `zoom`, `x` and `y`.  The heatmap is the
# signal strength (`level`) of the given network aggregated geospacially by
# by squares created truncating the latitude and longitude of readings to
# 4 decimal places.
# The tile uses the
# [slippy map tile standard](http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames)
# The request must
# have the `ssid` and aggregation function (`agg_function`) specified in the
# GET parameters.  `agg_function` defaults to median.
def tile(request, zoom, x, y):
    # Specify that the response will be a png image
    response = HttpResponse(content_type="image/png")
    params =  {
        'ssid': request.GET.get('ssid', None),
        'agg_function': request.GET.get('agg_function', 'median')
    }

    # Check if the ssid is one of the ssids that we prerender
    parentPath = os.path.join(settings.TILE_DIR, params['ssid'])
    if os.path.exists(parentPath):
        # If it is, check to see if we have a tile
        # If the tile exists, open it.  Otherwise return a transparent tile.
        path = getPath(params['ssid'], params['agg_function'], zoom, x, y)
        if os.path.exists(path):
            Image.open(path).save(response, "PNG")
        else:
            Image.new("RGBA", (256, 256)).save(response, "PNG")
    else:
        # If the ssid is not precomputed, render on the fly
        generateTile(
            int(x), int(y), int(zoom), params
        ).save(response, "PNG")

    return response

# ## Grey Layer Tile API

# Return the grey layer tile for the given `zoom`, `x` and `y`.  The grey layer
# is a representation of everywhere that we have data and is displayed
# underneath the heatmap.  This enables uses to differentiate between lack
# of coverage of a Wi-Fi network and lack of coverage of our data.
# All grey tiles are prerendered and saved to disk. This function simply returns
# A tile if one exists for the given parameters.  See
# [lib.generateGreyTile](lib.html#section-27) for details.
def greyTile(request, zoom, x, y):
    response = HttpResponse(content_type="image/png")

    path = getGreyPath(zoom, x, y)
    if os.path.exists(path):
        Image.open(path).save(response, "PNG")
    return response

# ## Wifipulling API

# An API to query the database for raw data.
def index(request):

    batch = 10 #default
    offset = 0 #default
    b_size = request.GET.get('batch', '')
    off_size = request.GET.get('offset', '')
    if (b_size != ''):
        try:
            batch = int(b_size)
        except:
            pass
    if (off_size != ''):
        try:
            offset = int(off_size)
        except:
            pass
    idx_start = offset
    idx_end = offset + batch
    is_full_size = True if (b_size==''and off_size=='') else False

    q_idx = request.GET.get('idx', '')
    q_lat = request.GET.get('lat', '')
    q_lng = request.GET.get('lng', '')
    q_radius = request.GET.get('radius', '')
    q_acc = request.GET.get('acc', '')
    q_alt = request.GET.get('altitude', '')
    q_startdate = request.GET.get('startdate', '')
    q_enddate = request.GET.get('enddate', '')
    q_dev_mac = request.GET.get('device_mac', '')
    q_app_v = request.GET.get('app_version', '')
    q_dro_v = request.GET.get('droid_version', '')
    q_dev_m = request.GET.get('device_model', '')
    q_ssid = request.GET.get('ssid', '')
    q_bssid = request.GET.get('bssid', '')
    q_caps = request.GET.get('caps', '')
    q_lvl = request.GET.get('level', '')
    q_frq = request.GET.get('freq', '')
    q_colname = request.GET.get('columns', '')
    q_decimal = request.GET.get('decimal', '')

    response_data = []
    tem=[]
    if (q_decimal != ''):
        decimal_place = 8

        try:
            decimal_place = int(q_decimal)
        except:
            pass

        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT TRUNCATE(lat,%d),TRUNCATE(lng,%d) FROM wifi_scan' % (decimal_place, decimal_place))
        tem = cursor.fetchall()

    else:
        query_set = None
        try:
            query_set = WifiScan.objects.all()
        except:
            pass

        if (query_set != None):
            if (q_idx != ''): # int
                try:
                    query_set = query_set.filter(idx=q_idx)
                except:
                    pass
            if (q_acc != ''): #float
                try:
                    query_set = query_set.filter(acc__gte=q_acc)
                except:
                    pass
            if (q_alt != ''): #double
                try:
                    query_set = query_set.filter(altitude__gte=q_alt)
                except:
                    pass
            if (q_startdate != ''):
                try:
                    mth, day, year = q_startdate.split('/',2)
                    dt = datetime.date(int(year), int(mth), int(day))
                    t_stamp = time.mktime(dt.timetuple()) * 1000
                    query_set = query_set.filter(time__gte=t_stamp)
                except:
                    pass
            if (q_enddate != ''):
                try:
                    mth, day, year = q_enddate.split('/',2)
                    dt = datetime.date(int(year), int(mth), int(day))
                    t_stamp = time.mktime(dt.timetuple()) * 1000
                    query_set = query_set.filter(time__lt=t_stamp)
                except:
                    pass
            if (q_dev_mac != ''):
                query_set = query_set.filter(device_mac=q_dev_mac)
            if(q_app_v != ''):
                query_set = query_set.filter(app_version=q_app_v)
            if (q_dro_v != ''):
                query_set = query_set.filter(droid_version=q_dro_v)
            if (q_dev_m != ''):
                query_set = query_set.filter(device_model=q_dev_m)
            if (q_ssid != ''):
                try:
                    list_ssid = q_ssid.split('|')
                    multi_ssid = ''
                    for id in list_ssid:
                        if (id != ''):
                            multi_ssid += "ssid="+"\'" + id + "\'" + " OR "
                    query_set = query_set.extra(where=[multi_ssid[:-4]])
                except:
                    pass
            if (q_bssid != ''):
                query_set = query_set.filter(bssid=q_bssid)
            if(q_caps != ''):
                query_set = query_set.filter(caps__contains=q_caps)
            if (q_lvl != ''):
                try:
                    query_set = query_set.filter(level__gte=q_lvl)
                except:
                    pass
            if (q_frq != ''):
                try:
                    query_set = query_set.filter(freq=q_frq)
                except:
                    pass

            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            human_readable = 0
            q_timeformat = request.GET.get('timeformat', '')
            try:
                human_readable = int(q_timeformat)
            except:
                pass

            is_distinct = 0
            q_distinct = request.GET.get('distinct', '')
            try:
                is_distinct = int(q_distinct)
            except:
                pass

            list_name=[]
            if (q_colname == ''):
                if (is_distinct == 1):
                    tem=query_set.values().distinct()
                else:
                    tem=query_set.values()
            else:
                list_name = q_colname.split('|')
                args = []
                for name in list_name:
                    if name in col_name and name != 'device_mac':
                        args.append(name)
                if (is_distinct == 1):
                    tem=query_set.values(*args).distinct()
                else:
                    tem=query_set.values(*args)

            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if (is_full_size == False):
                tem = tem[idx_start:idx_end]

            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            key = 'time'
            if (q_colname == '' or key in list_name):
                if (human_readable == 1):
                    for item in tem:
                        item[key]=(datetime.datetime.fromtimestamp(item[key]/1000)).strftime('%m-%d-%Y %H:%M:%S')
                elif(human_readable == 2):
                    for item in tem:
                        item['time2']=(datetime.datetime.fromtimestamp(item[key]/1000)).strftime('%m-%d-%Y %H:%M:%S')

    response_data = list(tem)

    return HttpResponse(json.dumps(response_data), content_type="application/json")
