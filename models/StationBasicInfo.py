from pydantic import BaseModel
from typing import Dict

class StationBasicInfo(BaseModel):
    cpoName: str
    stationName: str
    longitude: float
    latitude: float
    stationID: str
    accessType: str

class StationCompleteInfo(BaseModel):
    stationBasicInfo: StationBasicInfo
    connectors: Dict[str,Dict[str, Dict[str, int]]]