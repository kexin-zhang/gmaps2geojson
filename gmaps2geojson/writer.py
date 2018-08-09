import requests
import polyline
import json
import os

class Writer:
    def __init__(self):
        self.features = []

    def query(self, src, dest, custom_label = None):
        request_url = 'https://maps.googleapis.com/maps/api/directions/json?origin="{0}"&destination="{1}"&key={2}'.format(src, dest, os.environ["GMAPS_KEY"])
        try:
            r = requests.get(request_url)
            results = r.json()
            route = results['routes'][0]['overview_polyline']['points']
            coords = polyline.decode(route)
        except Exception as e:
            print("Error querying for directions for {0} tp {1} -- {2}".format(src, dest, str(e)))
            return

        # reverse order to comply with geojson spec
        coords_list = [[lon, lat] for lat, lon in coords]

        default_name = "{0} to {1}".format(src, dest)

        self.features.append({
            "type": "Feature",
            "properties": {
                "name": custom_label or default_name
            },
            "geometry": {
                "type": "MultiLineString",
                "coordinates": [coords_list]
            }
        })
        return [[lat, lon] for lat, lon in coords]

    def save(self, filename):
        geojson = {"type": "FeatureCollection", "features": self.features}
        with open(filename, "w") as out:
            json.dump(geojson, out)
