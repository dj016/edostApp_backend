from flask import Flask, jsonify
from flask import request

# add the project path to the sys.path
import sys
import os
current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(current_script_dir)
sys.path.append(project_dir)

from  data.cache import cache

app = Flask(__name__)
allStationCache: cache=  cache()

@app.route('/api/getNearestStations', methods=['GET'])
def get_nearest_stations():
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)

    #add checks to verify if the latitude and logitude are valid
    # add checks to verify if the latitude and longitude are valid numbers
    if latitude is None or longitude is None:
        return jsonify({'error': 'Latitude and longitude are required.'}), 400

    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        return jsonify({'error': 'Latitude and longitude must be valid numbers.'}), 400
    
    allStations= allStationCache.getAllStations()

    # find the closest 10 stations to the given latitude and longitude
    # sort the stations by distance to the given latitude and longitude
    # return the 10 closest stations
    closestStations= sorted(allStations, key= lambda station: (station.latitude-latitude)**2+(station.longitude-longitude)**2)
    return jsonify([station.model_dump() for station in closestStations[:10]])


if __name__ == '__main__':
    app.run(debug=True, port=5000)


