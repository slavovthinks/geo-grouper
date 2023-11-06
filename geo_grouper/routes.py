from fastapi import APIRouter, Depends

from geo_grouper.models import post_json_group_request, post_json_group_response, User
from geo_grouper.grouper import grouper
from geo_grouper.file_utils import load_users_from_csv

grouping_router = APIRouter(prefix='/groups', tags=['groups'])


@grouping_router.post('/')
async def group_from_json(users: post_json_group_request) -> post_json_group_response:
    users = [user.to_app_user() for user in users]
    return await grouper.group_users_by_address(users)


@grouping_router.post('/csv')
async def group_from_csv(users=Depends(load_users_from_csv)) -> post_json_group_response:
    return await grouper.group_users_by_address(users)

