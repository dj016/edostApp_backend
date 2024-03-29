from abc import abstractmethod
from typing import List, Dict

from models.StationBasicInfo import StationBasicInfo


class IStationInfoReposity():
    @abstractmethod
    def getStationList(self) -> List[StationBasicInfo]:
        pass
    
    # key 1: connectorType_PowerModel   key 2: status   key 3: count
    @abstractmethod
    def getStationInfo(stationId: str)-> Dict[str,Dict[str, Dict[str, int]]]:
        pass