from pydantic import BaseModel

class StationBasicInfo(BaseModel):
    cpoName: str
    stationName: str
    longitude: float
    latitude: float
    stationID: str
    accessType: str

class StationCompleteInfo(BaseModel):
    stationBasicInfo: StationBasicInfo
    connectors: dict[str,dict[str, dict[str, int]]]