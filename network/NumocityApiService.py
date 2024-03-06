import requests
from pydantic import BaseModel
from typing import List

# Define the API base URL
BASE_URL :str

class NumocityDocument(BaseModel):
    GlobalJwtToken: str

# Define data classes using pydantic
class NumocityTokenResponse(BaseModel):
    Document: NumocityDocument

class NumocityConnector(BaseModel):
    connectorType: str
    ComputedStatus: str
    connectorModelPower: str
    rate: float

class NumocityStation(BaseModel):
    ChargeStationID: int
    ChargeStationName: str
    ChargeStationLat: float
    ChargeStationLong: float
    AccessType: str

# Define the API service class
class NumocityApiService:
    def __init__(self, base_url: str, cpo_name: str):
        self.base_url = base_url
        self.cpo_name = cpo_name

    def get_token(self) -> NumocityTokenResponse:
        response = requests.get(f"{self.base_url}/token/admin/v1/requesttoken/449a164913fc3e683194c7d5eded732c")
        response.raise_for_status()
        return NumocityTokenResponse.parse_obj(response.json())

    def get_all_stations(self, authorization: str)-> List[NumocityStation]:
        headers = {"authorization": authorization}
        response = requests.get(f"{self.base_url}/asset/mobile/get-map-info", headers=headers)
        response.raise_for_status()
        return [NumocityStation.parse_obj(station) for station in response.json()]

    def get_station_info(self, authorization: str, station_id: str)-> List[NumocityConnector]:
        headers = {"authorization": authorization}
        params = {"ChargeStationID": station_id}
        response = requests.get(f"{self.base_url}asset/mobile/get-connector-info?numotype=ocpp", headers=headers, params=params)
        response.raise_for_status()
        return [NumocityConnector.parse_obj(connector) for connector in response.json()]
