
""" 
OSRM Service for calculating duration of rider from the seller
Author : Varnan 
Link : https://github.com/Project-OSRM/osrm-backend/blob/master/docs/http.md#service-trip

"""
import datetime
import requests
import json

# import base64
# import httplib2
# from django.conf import settings



class OsrmDistanceCalculation(object):

    """
    API : 
            http://{server}/{service}/v1/{profile}/{coordinates}?steps={true|false}&geometries={polyline|geojson}
                                            &overview={simplified|full|false}&annotations={true|false}

    EXAMPLE :
            http://router.project-osrm.org/table/v1/driving/13.388860,52.517037;13.397634,52.529407?destinations=0

    """
    SERVER = 'router.project-osrm.org'
    SERVICE = 'table'
    VERSION = 'v1'
    PROFILE = 'driving'
    response = {'data':[]}
    destination_index = 0

    

    def source_destination_distance_mapping(self, durations, sources, destination):
        if durations and sources and destination:
            for index,source in enumerate(sources):
                source_durations = {}
                source_durations['source'] = source['location']
                source_durations['destination'] = destination
                source_durations['duration'] = float(str(durations[index]).strip("[]"))
                print "source_durations ###",index,source_durations
                print "self.response['data'] ####",self.response['data']
                self.response['data'].append(source_durations)

            self.response['code'] = "success"
            self.response['message'] = "Success"
            return True
        else:
            self.response['code'] = "error"
            self.response['message'] = "Something wrong in Osrm Distance Calculation"
            return self.response

    def calculate_distance(self, sources = [[13.388860,52.517037],[13.397634,52.529407]], destination = [13.388860,52.517037]):
        if sources and destination and (type(sources) and type(destination) == list) :

            coordinates = ','.join([str(x) for x in destination])

            for source in sources:
                coordinates = coordinates+";"+(','.join([str(x) for x in source]))
            
            coordinates = coordinates.strip()

            url  = 'http://{0}/{1}/{2}/{3}/{4}?destinations={5}'.format(
                        self.SERVER, self.SERVICE, self.VERSION, self.PROFILE, coordinates, self.destination_index)

            try:
                resp = requests.get(url).json()
            except:
                self.response['code'] = "error"
                self.response['message'] = "Something wrong in Osrm Distance Calculation"
                return self.response

            if resp['code'].lower() == 'ok':
                durations = resp['durations']
                sources = resp['sources']
                source_dest_dict = self.source_destination_distance_mapping(durations, sources, destination)
            else:
                self.response['code'] = "error"
                self.response['message'] = "Something wrong in Osrm Distance Calculation"

        else:
            self.response['code'] = "error"
            self.response['message'] = "Enter valid list for sources and destination"
            
        return self.response


