import os
import time
from typing import Optional
from csv import DictReader
from geopy.distance import geodesic

import requests  # Was using requests for the POC


GROUP_RADIUS_METERS = 30  # Acceptable radius for a group


def get_long_lat_maps_co(address: str) -> Optional[dict]:
    BASE_URL = "https://geocode.maps.co/search"
    res = requests.get(
        BASE_URL,
        params={
            "q": address
        }
    )
    response = res.json()
    if len(response) > 0:
        rank_1_address = response[0]
        return {"lat": rank_1_address.get("lat"), "lon": rank_1_address.get("lon")}
    return None


def get_long_lat_geoapify(address: str) -> Optional[dict]:

    API_KEY = os.getenv("GEOAPIFY_API_KEY")
    BASE_URL = "https://api.geoapify.com/v1/geocode/search"
    res = requests.get(
        BASE_URL,
        params={
            "api_key": API_KEY,
            "text": address
        }
    )
    response = res.json()
    features = response.get("features")
    if features is not None and len(features) > 0:
        rank_1_address = features[0]["properties"]
        return {
            "lat": rank_1_address.get("lat"),
            "lon": rank_1_address.get("lon")
        }
    return None

def get_long_lat(address: str):
    if location := get_long_lat_maps_co(address):
        return location
    return get_long_lat_geoapify(address)

def load_csv(path: str) -> list:
    # TODO: validate input
    # later it will be a file stream from user upload
    with open(path, 'r', encoding='utf-8-sig') as f:
        dict_reader = DictReader(f)
        # sorted(dict_reader.fieldnames) == sorted(expected)
        return list(dict_reader)


def group_users_by_location(users: list):
    groups = []
    for user in users:
        added_to_group = False
        current_point = (user['location']['lat'], user['location']['lon'])
        for group in groups:
            if geodesic(group['center'], current_point).meters <= GROUP_RADIUS_METERS:
                group['users'].append(user['name'])
                added_to_group = True
                break
        if not added_to_group:
            groups.append({'center': current_point, 'users': [user['name']]})
    return groups


def groups_as_response(groups: list) -> list:
    return list(group['users'] for group in groups)


def get_users_locations(users_addresses: list) -> list:
    users_locations = []
    for user in users_addresses:
        # Vendors will implement their own rate limiting
        time.sleep(0.5)
        users_locations.append({"name": user["Name"], "location": get_long_lat(user["Address"])})
    return users_locations


users_addresses = load_csv('ResTecDevTask-sample_input_v1.csv')
users_locations = get_users_locations(users_addresses)
groups = group_users_by_location(users_locations)
print(groups_as_response(groups))
