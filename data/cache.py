from typing import Dict, List
from network.NumocityApiService import NumocityApiService
from models.StationBasicInfo import StationBasicInfo
from data.NumocityNetworkRepository import NetworkNumocityRepository
import time
import sys
import os
current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(current_script_dir)
sys.path.append(project_dir)


# create a time variable to store the time when it was last fetched
class cache():
    def __init__(self):
        self.lastUpdate = time.time()
        self.data: List[StationBasicInfo] = None

        # self.zeonApiService: NumocityApiService= NumocityApiService("https://csmszeon.numocity.com", "zeon")
        self.reluxApiService: NumocityApiService = NumocityApiService(
            "https://csmsrelux.numocity.com", "relux")
        self.kurrentChargeApiService: NumocityApiService = NumocityApiService(
            "https://csmskurrentcharge.numocity.com", "kurrent charge")

        # self.zeonNetworkRepository= NetworkNumocityRepository(self.zeonApiService)
        self.reluxNetworkRepository = NetworkNumocityRepository(
            self.reluxApiService)
        self.kurrentChargeNetworkRepository = NetworkNumocityRepository(
            self.kurrentChargeApiService)

    def isDataOlderThanOneDay(self) -> bool:
        return time.time()-self.lastUpdate > 86400

    def shouldRefreshData(self) -> bool:
        return self.data is None or self.isDataOlderThanOneDay()

    def refreshData(self):
        # zeonStations=self.zeonNetworkRepository.getStationList()
        reluxStations = self.reluxNetworkRepository.getStationList()
        kurrentChargeStations = self.kurrentChargeNetworkRepository.getStationList()

        # self.data= zeonStations+reluxStations+kurrentChargeStations
        self.data = reluxStations + kurrentChargeStations
        self.lastUpdate = time.time()

    def getAllStations(self) -> List[StationBasicInfo]:
        if self.shouldRefreshData():
            self.refreshData()
        return self.data

    def getStationInfo(self, cpoName: str, stationId: str) -> Dict[str, Dict[str, Dict[str, int]]]:
        if (cpoName == "relux"):
            return self.reluxNetworkRepository.getStationInfo(stationId)
        elif (cpoName == "kurrent charge"):
            return self.kurrentChargeNetworkRepository.getStationInfo(stationId)
