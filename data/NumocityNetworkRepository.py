from typing import List
from data.IStationInfoRepository import IStationInfoReposity
from models.StationBasicInfo import StationBasicInfo
from network.NumocityApiService import NumocityApiService
from typing import List, Dict


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

    def getStationInfo(self, stationId)-> Dict[str,Dict[str, Dict[str, int]]]:
        token= self.getToken()
        connectors= self.apiService.get_station_info(token, stationId)
        # group connectors by connectorType and powerModel
        connectorDict= {}
        for connector in connectors:
            # check if connectorDict contains a key of connctor.connectorType
            if connector.connectorType not in connectorDict:
                connectorDict[connector.connectorType]= {}
            # check if connectorDict[connector.connectorType] contains a key of connector.connectorModelPower
            if connector.connectorModelPower not in connectorDict[connector.connectorType]:
                connectorDict[connector.connectorType][connector.connectorModelPower]= {}
            # check if connectorDict[connector.connectorType][connector.connectorModelPower] contains a key of connector.ComputedStatus
            if connector.ComputedStatus not in connectorDict[connector.connectorType][connector.connectorModelPower]:
                connectorDict[connector.connectorType][connector.connectorModelPower][connector.ComputedStatus]= 0
            
            connectorDict[connector.connectorType][connector.connectorModelPower][connector.ComputedStatus]+= 1
        
        return connectorDict
  
    def getToken(self) -> str:
        return "Bearer "+ self.apiService.get_token().Document.GlobalJwtToken
