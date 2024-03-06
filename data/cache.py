import sys
import os
current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(current_script_dir)
sys.path.append(project_dir)


import time
from data.NumocityNetworkRepository import NetworkNumocityRepository
from models.StationBasicInfo import StationBasicInfo
from data.NumocityNetworkRepository import NetworkNumocityRepository
from network.NumocityApiService import NumocityApiService
from typing import List


#create a time variable to store the time when it was last fetched
class cache():
    def __init__(self):
        self.lastUpdate= time.time()
        self.data: List[StationBasicInfo]= None

        self.zeonApiService: NumocityApiService= NumocityApiService("https://csmszeon.numocity.com", "zeon")
        self.reluxApiService: NumocityApiService= NumocityApiService("https://csmsrelux.numocity.com", "relux")
        self.kurrentChargeApiService:NumocityApiService= NumocityApiService("https://csmskurrentcharge.numocity.com","kurrent charge") 

        self.zeonNetworkRepository= NetworkNumocityRepository(self.zeonApiService)
        self.reluxNetworkRepository= NetworkNumocityRepository(self.reluxApiService)
        self.kurrentChargeNetworkRepository= NetworkNumocityRepository(self.kurrentChargeApiService)
    
    def isDataOlderThanOneDay(self)-> bool:
        return time.time()-self.lastUpdate> 86400
    
    def shouldRefreshData(self)-> bool:
        return self.data is None or self.isDataOlderThanOneDay()
    
    def refreshData(self):
        zeonStations=self.zeonNetworkRepository.getStationList()
        reluxStations=self.reluxNetworkRepository.getStationList()
        kurrentChargeStations=self.kurrentChargeNetworkRepository.getStationList()

        self.data= zeonStations+reluxStations+kurrentChargeStations
        self.lastUpdate= time.time()


    def getAllStations(self)-> List[StationBasicInfo]:
        if self.shouldRefreshData():
            self.refreshData()
        return self.data
    
