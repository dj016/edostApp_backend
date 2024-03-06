from pydantic import BaseModel

class StationBasicInfo(BaseModel):
    cpoName: str
    stationName: str
    longitude: float
    latitude: float
    stationID: str
    accessType: str