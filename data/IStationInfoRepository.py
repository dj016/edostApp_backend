from abc import abstractmethod
from typing import List, Dict

from models.StationBasicInfo import StationBasicInfo


class IStationInfoReposity():
    @abstractmethod
    def getStationList(self) -> List[StationBasicInfo]:
        pass
    
    @abstractmethod
    def getStationInfo(stationId: str)-> Dict[str, Dict[str, int]]:
        pass