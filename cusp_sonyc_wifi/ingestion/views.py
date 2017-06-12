# Controller for the ingestion API.

from django.shortcuts import render
from django.http import HttpResponse
from ingestion.models import WifiScan
from ingestion.models import UniqueLocations
import simplejson as json
from django.views.decorators.csrf import csrf_exempt
import traceback

# The ingestion API only has a single endpoint, the index.
# calls [`populate`](#section-3) when a POST body is included in the request.
@csrf_exempt
def index(request):
    if request.method == 'POST':
        print request.body
        if (len(request.body) <= 0):
            return HttpResponse("No Payload Received")
        response = populate(request.body)
        if response:
            return HttpResponse(response)
        else:
            return HttpResponse(status=500)
    else:
        return HttpResponse("Hello!")

# ## populate

# parses the JSON payload from the Android application and inserts it
# into the database one access point per record.
# Params: request body from application
# Returns: "1" if successful upload, error message otherwise.
def populate(info):

    # convert everything to unicode before loading it as json
    # to avoid odd characters and load in json format. if error
    # with this process, send error message to application.
    try:
        info = unicode(info, errors='ignore')
        scan = json.loads(info)
    except:
        print "INVALID JSON"
        return "Invalid JSON"

    access_points = list()

    # there should be only one main key in scan ("scans")
    for mainkey in scan:

        # check that the scan array contains information and send error
	# and send error message if it does not
        if (len(scan[mainkey]) < 1):
            print "EMPTY JSON"
            return "Empty JSON uploaded!!!"

        print "Len 1:",len(scan[mainkey])
	# iterate through every dictionary in the scan array
        for i in range(0, len(scan[mainkey])):

	    # empty lists to hold the dictionary elements with single values
	    # and multiple values (in the case of the scan readings)
            single = list()
            readings = list()

	    # to circumvent type errors
            try:

		# iterate through each key in the current dictionary
                for key in scan[mainkey][i]:

		    # check if the value of the key is a list (only readings
		    # will be a list)
                    if isinstance(scan[mainkey][i][key],list):

			# if a list, iterate through the list
                        for j in range(0,len(scan[mainkey][i][key])):
                            items = list()

			    # as each list element is a dictionary, iterate
			    # through keys in dictonary and add a tuple
			    # containing the key and value pair to the items array
                            for readkey in scan[mainkey][i][key][j]:
                                items.append((readkey,scan[mainkey][i][key][j][readkey]))

			    # before moving to the next dictionary in the list,
			    # add the items to the readings list
                            readings.append(items)

		    # if not a list, add a tuple of the key/value pair to the
		    # list for single elements (these include things like time
		    # and location as they are the same for multiple access
		    # points
                    else:
                        single.append((key, scan[mainkey][i][key]))

	    # if a TypeError is present, move on
            except(TypeError):
                pass

	    # list to hold the final set of dictionaries
            final_dicts = list()

	    # iterate through every element of the readings list
            for k in range(0, len(readings)):

		# a dictionary of the measurements
                measurement_dict = dict()

		# iterate through each tuple in the current reading
                for read_measure in readings[k]:

		    # default to the key being the first element of the tuple
		    # and the value being the second
                    measurement_key = read_measure[0]
                    measurement_value = read_measure[1]

		    # if the elements of the tuple are String Objects,
		    # change them to string types (instead of unicode) and lowercase
                    if isinstance(read_measure[0], basestring):
                        measurement_key = str(read_measure[0]).lower()
                    if isinstance(read_measure[1], basestring):
                        measurement_value = str(read_measure[1]).lower()

		    # add the key value pair to the measurement dictionary
                    measurement_dict[measurement_key] = measurement_value

		# iterate through the elements of the single measurements
		# and do the same as above
                for single_measure in single:

                    single_key = single_measure[0]
                    single_value = single_measure[1]

                    if isinstance(single_measure[0], basestring):
                        single_key = str(single_measure[0])
                    if isinstance(single_measure[1], basestring):
                        single_value = str(single_measure[1])

                    measurement_dict[single_key] = single_value

		# add the entire dictionary to the final list
                final_dicts.append(measurement_dict)

	    # iterate through each element of final_dicts
            for access_point in final_dicts:

		# add a WifiScan class insertion for each access point
		# in the final_dicts list to the access_points list.
		# See Models for WiFiScan class
                access_points.append(WifiScan(**access_point))

    # try to bulk create all of the WiFiScan model insertions in one database
    # connection and return "1" to Android application if successful
    try:
        print "LEN 2:",len(access_points)
        WifiScan.objects.bulk_create(access_points)
        return "1"

    # if there is an error creating new entries, send error to application
    except:
        print "ERROR DB!"
        traceback.print_exc()
        return None
