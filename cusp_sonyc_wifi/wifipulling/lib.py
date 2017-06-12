# `lib` contains utility functions around generating tiles.
from ingestion.models import WifiScan
import math
import time
import os
import pandas as pd
import numpy as np
from scipy.misc import imresize
from matplotlib import cm
from PIL import Image, ImageDraw
from django.db import connection
from django.conf import settings
from django.db.models import Max


# ## getTopSSIDs

# Return a list of ssids which have a number of datapoints greater than
# `threshold`
def getTopSSIDs(threshold=settings.SSID_THRESHOLD):
    cursor = connection.cursor()
    cursor.execute('SELECT ssid FROM wifi_scan GROUP BY ssid HAVING COUNT(*) > %s;' % (threshold))
    return [i[0] for i in cursor.fetchall() if i[0]]


# ## getPath

# Get the path of a heatmap tile
def getPath(ssid, agg_function, zoom, x, y):
    path = os.path.join(
	settings.TILE_DIR, ssid, agg_function,
	str(zoom), str(x), '%s.png' % y
    )
    return path


# ## getGreyPath

# Get the path of a grey layer tile
def getGreyPath(zoom, x, y):
    path = os.path.join(
	settings.GREYTILE_DIR,
	str(zoom), str(x), '%s.png' % y
    )
    return path


# ## generateTiles

# generateTiles generates all the tiles for a given ssid from the minimum
# zoom level to the maximum zoom level and saves them all to disk.
def generateTiles(ssid):
    print("generateTiles",ssid)
    zoom_range=range(settings.ZOOM_MIN, settings.ZOOM_MAX+1)
    
    if ssid == "Known Open Wi-Fi":
        '''f = WifiScan.objects.filter(ssid__in=[
            '#flatiron free wifi', '.freewifibysurface', '@smartfi-open', 'attwifi', 
            'bryantpark.org', 'CableWiFi', 'cablewifi', 'DowntownBrooklynWiFi_Fon', 
            'linknyc free wi-fi', 'Metrotech', 'optimumwifi', 'TWCWiFi', 'twcwifi', 
            'usp park wifi', 'xfinitywifi'
        ])'''
        f = WifiScan.objects.filter(ssid__in=[
            '#flatiron free wifi', '.freewifibysurface', 
            'bryantpark.org', 'DowntownBrooklynWiFi_Fon', 
            'linknyc free wi-fi', 'Metrotech',
            'usp park wifi', 'Red Hook Wifi'
        ])
    elif ssid == "All Wi-Fi":
        f = WifiScan.objects
    else:
        f = WifiScan.objects.filter(ssid=ssid)

    df = pd.DataFrame.from_records(
        f.values('lat', 'lng', 'time').annotate(level=Max('level'))
    ).round(4)

    unique = df.drop_duplicates(subset=['lat', 'lng'])


    for zoom in zoom_range:
        generated = {}

        for row in unique.iterrows():
            loc = deg2num(row[1]['lat'], row[1]['lng'], zoom)
            x,y = loc
            if loc not in generated:
                generated[loc] = True

	        for agg_function in settings.AGGREGATION:
	            tile = generateTile(x, y, zoom, {
		        'ssid': ssid,
		        'agg_function': agg_function
	            }, df)

	            path = getPath(ssid, agg_function, zoom, x, y)
	            if not os.path.exists(os.path.dirname(path)):
		        os.makedirs(os.path.dirname(path))
	            tile.save(path)


# ## generateGreyTiles

# generateGreyTiles generates all the tiles for the grey layer from the minimum
# zoom level to the maximum zoom level and saves them all to disk.
def generateGreyTiles():
    zoom_range=range(settings.ZOOM_MIN, settings.ZOOM_MAX+1)

    df1 = pd.DataFrame.from_records(
	   WifiScan.objects.values('lat', 'lng')
    ).round(4)
    df = df1.drop_duplicates(subset=['lat','lng'])

    for zoom in zoom_range:
        generated = {}

        for row in df.iterrows():
            loc = deg2num(row[1]['lat'], row[1]['lng'], zoom)
            x,y = loc
            if loc not in generated:
                generated[loc] = True

                tile = generateGreyTile(x, y, zoom, df)

                # Store a tile only if it is not empty
                if tile != None:
                    path = getGreyPath(zoom, x, y)
                    if not os.path.exists(os.path.dirname(path)):
                        os.makedirs(os.path.dirname(path))
                    tile.save(path)


# ## num2deg

# Convert slippy map `x`,`y`,`zoom` to the corresponding latitude/longitude pair.
# Taken from the
# [openstreetmap wiki](http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python).
def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)


# ## deg2num

# Convert latitude/longitude/zoom to a the corresponding slippy map `x` and `y`.
# Taken from the
# [openstreetmap wiki](http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python).
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)


# ## generateTile

# generateTile generates a single 256x256 pixel tile for the given parameters.
# `x`, `y` and `zoom` define the geospacial location of the tile in the
# slippy map standard. `params` is a dictionary containing the ssid and
# aggregation function to be used.  `allRecords` optionally contains a pandas
# DataFrame containing all the records for the given ssid.  If `None`, then
# the database will be queried.
def generateTile(x, y, zoom, params, allRecords=None):
    timestamp = int(time.time())
    ssid = params['ssid']
    agg_function = params['agg_function']

    # Get the corners
    nw_corner = num2deg(x, y, zoom)
    se_corner = num2deg(x+1, y+1, zoom)

    # Get lists of the two latitudes and two longitudes in ascending order
    lats = [min(nw_corner[0], se_corner[0]), max(nw_corner[0], se_corner[0])]
    lngs = [min(nw_corner[1], se_corner[1]), max(nw_corner[1], se_corner[1])]

    # Add a little bit of buffer around the edges to make sure to catch
    # squares that are on the edge of the tile and then round to 4 decimals.
    lats2 = np.around([lats[0] - .0002, lats[1] + .0002], decimals=4)
    lngs2 = np.around([lngs[0] - .0002, lngs[1] + .0002], decimals=4)

    # If allRecords is defined, then filter is based on the current tile
    # otherwise query the DB for the specific data and add it to a DataFrame
    if allRecords is not None:
        df = allRecords[
            (allRecords.lat >= lats2[0]) &
            (allRecords.lat <= lats2[1]) &
            (allRecords.lng >= lngs2[0]) &
            (allRecords.lng <= lngs2[1])
        ]

    else:
        records = WifiScan.objects.filter(
            ssid=ssid,
            lat__gte=lats2[0], lat__lte=lats2[1],
            lng__gte=lngs2[0], lng__lte=lngs2[1],
        ).values('lat', 'lng', 'time').annotate(level=Max('level'))
        #).values('lat', 'lng', 'level')

        df = pd.DataFrame.from_records(
            records
        )

        df = df.round(4)


    # If the tile is empty, just return a transparent tile
    if len(df) == 0:
        return Image.new("RGBA", (256,256))

    # Group the data into the .0001 lat x .0001 lng squares and aggregate
    groups = df.groupby(('lat', 'lng'), as_index=False)
    points = getattr(groups, agg_function)()

    # Get a list of the x/y bins for the data.
    bins = [
        np.arange(lngs2[0]-.00005, lngs2[1]+.00005, .0001),
        np.arange(lats2[0]-.00005, lats2[1]+.00005, .0001)
    ]

    # Bin the data
    zi, xi, yi = np.histogram2d(
        points['lng'], points['lat'], weights=points['level'], normed=False,
        bins=bins
    )

    # Scale the data to 0-255 and rotate correctly
    zi = np.ma.masked_equal(zi, 0)
    zi = ((np.clip(zi, -90, -29) + 91) * 4.25).astype(int)
    zi = np.rot90(zi)

    # Color the data
    color = np.uint8(cm.jet(zi/255.0)*255)

    # `s` is the size of the tile we will scale it up to _before_ cropping.
    # The tile needs to be cropped because we originally included some buffer
    # for catching all the data that might be on the edge of the tile.
    s = 1024
    color = imresize(color, size=(s,s), interp='nearest')

    # Now crop the data down to what the tile is _actually_ supposed to contain
    # and then scale to 256x256 pixels.
    lat_len = zi.shape[0]*.0001
    lng_len = zi.shape[1]*.0001

    x1 = int(((lngs[0]-(lngs2[0]-.00005))/lng_len)*s)
    x2 = int(s-(((lngs2[1]+.00005) - lngs[1])/lng_len)*s)

    y1 = int((((lats2[1]+.00005) - lats[1])/lat_len)*s)
    y2 = int(s-((lats[0]-(lats2[0]-.00005))/lat_len)*s)

    color = color[y1:y2+1,x1:x2+1]
    color = imresize(color, size=(256,256), interp='nearest')

    return Image.fromarray(color)


# ## generateGreyTile

def generateGreyTile(x, y, zoom, allRecords):
    timestamp = int(time.time())
    nw_corner = num2deg(x, y, zoom)
    se_corner = num2deg(x+1, y+1, zoom)

    lats = [min(nw_corner[0], se_corner[0]), max(nw_corner[0], se_corner[0])]
    lngs = [min(nw_corner[1], se_corner[1]), max(nw_corner[1], se_corner[1])]

    lats2 = np.around([lats[0] - .0002, lats[1] + .0002], decimals=4)
    lngs2 = np.around([lngs[0] - .0002, lngs[1] + .0002], decimals=4)

    timestamp = int(time.time())

    df = allRecords[
            (allRecords.lat >= lats2[0]) &
            (allRecords.lat <= lats2[1]) &
            (allRecords.lng >= lngs2[0]) &
            (allRecords.lng <= lngs2[1])
        ]
    df = df.reset_index(drop=True)
    timestamp = int(time.time())

    if len(df) != 0:

        bins = [
            np.arange(lngs2[0]-.00005, lngs2[1]+.00005, .0001),
            np.arange(lats2[0]-.00005, lats2[1]+.00005, .0001)
        ]

        zi, xi, yi = np.histogram2d(
            df['lng'], df['lat'],
            bins=bins, normed=False
        )

        zi = np.ma.masked_equal(zi, 0)
        zi = ((np.clip(zi, -90, -29) + 91) * 4.25).astype(int)
        zi = np.rot90(zi)

        s = 1024


        color = np.uint8(cm.gray(zi/225.0) * 225)
        color = imresize(color, size=(s,s), interp='nearest')

        lat_len = zi.shape[0]*.0001
        lng_len = zi.shape[1]*.0001

        x1 = int(((lngs[0]-(lngs2[0]-.00005))/lng_len)*s)
        x2 = int(s-(((lngs2[1]+.00005) - lngs[1])/lng_len)*s)

        y1 = int((((lats2[1]+.00005) - lats[1])/lat_len)*s)
        y2 = int(s-((lats[0]-(lats2[0]-.00005))/lat_len)*s)

        color = color[y1:y2+1,x1:x2+1]
        color = imresize(color, size=(256,256), interp='nearest')

        return Image.fromarray(color)
