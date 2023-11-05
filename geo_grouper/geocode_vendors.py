from abc import ABC, abstractmethod
from typing import Optional

from aiolimiter import AsyncLimiter
import aiohttp

from geo_grouper.models import Location, VendorsEnum
from geo_grouper.settings import settings


# Note: Protocol might be a better substitute for ABC
# Note: Currently vendors __init__ methods are similar and BaseVendor can implement __init__ to be called with
# super in child classes. Future vendors might use a vendor specific library and have a different __init__ thats why
# Im keeping them separate for now
class BaseVendor(ABC):
    @abstractmethod
    async def forward_geocode(self, address: str) -> Optional[Location]:
        pass


class MapsCoVendor(BaseVendor):
    def __init__(self, rate_limit: int = 2, base_url: str = "https://geocode.maps.co"):
        self.rate_limiter = AsyncLimiter(rate_limit, 1)
        self.base_url = base_url.rstrip('/')

    async def forward_geocode(self, address: str) -> Optional[Location]:
        search_url = f"{self.base_url}/search"
        async with self.rate_limiter:
            async with aiohttp.request("GET", search_url, params={"q": address}) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                if len(data) > 0:
                    rank_1_address = data[0]
                    return Location(lat=rank_1_address.get("lat"), lon=rank_1_address.get("lon"))
                return None


class GeoapifyVendor(BaseVendor):
    def __init__(self, api_key: str, rate_limit: int = 5, base_url: str = "https://api.geoapify.com/v1/geocode"):
        self.api_key = api_key
        self.rate_limiter = AsyncLimiter(rate_limit, 1)
        self.base_url = base_url.rstrip('/')

    async def forward_geocode(self, address: str) -> Optional[Location]:
        search_url = f"{self.base_url}/search"
        async with self.rate_limiter:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        search_url,
                        params={
                            "api_key": self.api_key,
                            "text": address
                        }
                ) as response:
                    if response.status != 200:
                        return None
                    response_json = await response.json()
                    features = response_json.get("features")
                    if isinstance(features, list) and len(features) > 0:
                        rank_1_address = features[0]["properties"]
                        return Location(lat=rank_1_address.get("lat"), lon=rank_1_address.get("lon"))
            return None


def get_maps_co_vendor() -> MapsCoVendor:
    """Factory function for maps.co vendor"""
    return MapsCoVendor(
        rate_limit=settings.maps_co_rate_limit,
        base_url=settings.maps_co_base_url
    )


def get_geoapify_vendor() -> GeoapifyVendor:
    return GeoapifyVendor(
        api_key=settings.geoapify_api_key,
        rate_limit=settings.geoapify_rate_limit,
        base_url=settings.geoapify_base_url
    )


vendors_map = {
    VendorsEnum.maps_co: get_maps_co_vendor,
    VendorsEnum.geoapify: get_geoapify_vendor
}
vendors = [vendors_map[vendor]() for vendor in settings.enabled_vendors]
