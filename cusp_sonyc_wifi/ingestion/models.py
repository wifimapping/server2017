# Defines the models used by the WiFind server.

from django.db import models

# ## UniqueLocations

# A model for unique locations - a particular lat/lon pair that appears in the
# database.  Each pair will only have one entry in unique locations even
# if there are many scans that fall into that location.
class UniqueLocations(models.Model):
    idx = models.AutoField(primary_key=True)
    lat = models.DecimalField(max_digits=8, decimal_places=4)
    lng = models.DecimalField(max_digits=8, decimal_places=4)

    class Meta:
        unique_together = ('lat', 'lng')
        managed = True
        db_table = 'unique_locations'

    def __unicode__(self):
        return " / " + str(self.lat) + " / " + str(self.lng)

# ## TempUniqueLocations

class TempUniqueLocations(models.Model):
    idx = models.AutoField(primary_key=True)
    lat = models.DecimalField(max_digits=8, decimal_places=4)
    lng = models.DecimalField(max_digits=8, decimal_places=4)

    class Meta:
        managed = True
        db_table = 'temp_unique_locations'

    def __unicode__(self):
        return " / " + str(self.lat) + " / " + str(self.lng)

# ## WifiScan

# The model for each wifi scan.  Each row will be a single access point
# from a wifi scan.
class WifiScan(models.Model):
    idx = models.BigIntegerField(primary_key=True)
    # The latitude
    lat = models.FloatField()
    # The longitude
    lng = models.FloatField()
    # The accuracy of the GPS signal
    acc = models.FloatField()
    # The altitude in meters
    altitude = models.FloatField()
    # The time of the GPS scan
    time = models.DecimalField(max_digits=15, decimal_places=0)
    # The mac address of the phone
    device_mac = models.CharField(max_length=20)
    # The version of the app being run
    app_version = models.CharField(max_length=10)
    # The version of android
    droid_version = models.CharField(max_length=10)
    # The model of the phone
    device_model = models.CharField(max_length=50)
    # The SSID (network name) of the access point
    ssid = models.CharField(max_length=100)
    # The BSSID (mac address) of the access point
    bssid = models.CharField(max_length=20)
    # A string describing the capabilities of the access point, such as security
    # protocol.
    caps = models.CharField(max_length=100)
    # The signal strength of the wifi signal
    level = models.FloatField()
    # The frequency that the access point is being broadcast at.
    freq = models.FloatField()

    class Meta:
        managed = False
        db_table = 'wifi_scan'

    def __unicode__(self):
        return str(self.idx) + " / " + str(self.lat) + " / " + str(self.lng) + " / " + str(self.acc) + " / " + str(self.altitude) + " / " + str(self.time) + " / " + self.device_mac + " / " + self.app_version+ " / " + self.droid_version+ " / " + self.device_model+ " / " + self.ssid+ " / " + self.bssid+ " / " + self.caps+ " / " + str(self.level)+ " / " + str(self.freq)
