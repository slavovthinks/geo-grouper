from typing import Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from geo_grouper.models import VendorsEnum


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    geoapify_api_key: Optional[str] = None
    geoapify_rate_limit: int = 5  # Requests per second
    geoapify_base_url: str = "https://api.geoapify.com/v1/geocode"
    maps_co_rate_limit: int = 2
    maps_co_base_url: str = "https://geocode.maps.co"
    group_radius: int = 30  # Max radius in meters that forms a group
    enabled_vendors: list[VendorsEnum]  # enabled vendors ordered by priority

    @model_validator(mode='after')
    def check_geopapify_api_key(self):

        if VendorsEnum.geoapify in self.enabled_vendors and self.geoapify_api_key is None:
            raise ValueError("GEOAPIFY_API_KEY is required when geoapify is an enabled vendor")
        return self

settings = Settings()
