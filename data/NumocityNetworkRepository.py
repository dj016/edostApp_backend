from typing import List
from data.IStationInfoRepository import IStationInfoReposity
from models.StationBasicInfo import StationBasicInfo
from network.NumocityApiService import NumocityApiService
from typing import List


class NetworkNumocityRepository(IStationInfoReposity):
    def __init__(self, apiService: NumocityApiService):
        self.apiService = apiService

    def getStationList(self) -> List[StationBasicInfo]: 
        token = self.getToken()
        rawList = self.apiService.get_all_stations(token)
        return [
        StationBasicInfo(
            stationID=str(station.ChargeStationID),
            stationName=station.ChargeStationName,
            latitude=station.ChargeStationLat,
            longitude=station.ChargeStationLong,
            accessType=station.AccessType,
            cpoName= self.apiService.cpo_name
        )
        for station in rawList
    ]

    def getStationInfo(self, stationId):
        token= self.getToken()
        connectors= self.apiService.get_station_info(token, stationId)
        connectorMap = {}
        for connector in connectors:
            key = f"{connector.connectorType}_{connector.connectorModelPower}"
            if key not in connectorMap:
                connectorMap[key] = {}
            statusConnectors = connectorMap[key]
            status = connector.ComputedStatus
            if status not in statusConnectors:
                statusConnectors[status] = 0
            statusConnectors[status] += 1
        return connectorMap

    def getToken(self) -> str:
        return "Bearer "+ self.apiService.get_token().Document.GlobalJwtToken
