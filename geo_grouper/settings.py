from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from geo_grouper.models import VendorsEnum


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    geoapify_api_key: str
    geoapify_rate_limit: int = 5  # Requests per second
    geoapify_base_url: str = "https://api.geoapify.com/v1/geocode"
    maps_co_rate_limit: int = 2
    maps_co_base_url: str = "https://geocode.maps.co"
    group_radius: int = 30  # Max radius in meters that forms a group
    enabled_vendors: list[VendorsEnum]  # enabled vendors ordered by priority


settings = Settings()
