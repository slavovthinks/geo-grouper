from typing import Optional

from geopy.distance import geodesic

from geo_grouper.models import Location, User, UserGroup
from geo_grouper.geocode_vendors import BaseVendor, vendors
from geo_grouper.settings import settings


class GeoGrouper:
    def __init__(self, vendors: list[BaseVendor], group_radius: int = 30):
        self.vendors = vendors
        self.group_radius = group_radius

    async def get_location(self, address: str) -> Optional[Location]:
        for vendor in self.vendors:
            location = await vendor.forward_geocode(address)
            if location is not None:
                return location
        return None

    async def set_users_location(self, users: list[User]) -> list[User]:  # Not a pure function has side effect, tradeoff between dict and model usage :\
        for user in users:
            user.location = await self.get_location(user.address)
        return users

    def create_groups(self, users: list[User]) -> list[UserGroup]:  # separate function as it might be good to run it in a separate process if having large data
        groups: list[UserGroup] = []
        for user in users:
            added_to_group = False
            current_point = (user.location.lat, user.location.lon)
            for group in groups:
                group_center = (group.center.lat, group.center.lon)
                if geodesic(group_center, current_point).meters <= self.group_radius:
                    group.users.append(user)
                    added_to_group = True
                    break
            if not added_to_group:
                groups.append(UserGroup(center=user.location, users=[user, ]))
        return groups

    async def group_users_by_location(self, users: list[User]) -> list[UserGroup]:
        users = await self.set_users_location(users)
        return self.create_groups(users)


def get_grouper():
    return GeoGrouper(vendors=vendors, group_radius=settings.group_radius)


grouper = get_grouper()
