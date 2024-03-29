from flask import Flask, jsonify
from flask import request

# add the project path to the sys.path
import sys
import os

from models.StationBasicInfo import StationCompleteInfo
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
    StationsSortedByDistance= sorted(allStations, key= lambda station: (station.latitude-latitude)**2+(station.longitude-longitude)**2)
    TenClosestStations= StationsSortedByDistance[:5]
    
    # get real time status for all the ten stations
    # call getStationInfo for each station
    # return the status for each station
    returnList= []
    for station in TenClosestStations:
        stationInfo= allStationCache.getStationInfo(station.cpoName, station.stationID)
        returnList.append(StationCompleteInfo(stationBasicInfo= station, connectors= stationInfo))

    return jsonify([station.model_dump() for station in returnList])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug= True)


