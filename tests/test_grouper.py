import pytest
from unittest.mock import AsyncMock, Mock, call

from geo_grouper.grouper import GeoGrouper
from geo_grouper.models import Location, User


@pytest.mark.asyncio
async def test_grouper_get_location__first_vendor():
    mock_vendor_1 = Mock()
    mock_vendor_1.forward_geocode = AsyncMock()
    mock_vendor_2 = Mock()
    mock_vendor_2.forward_geocode = AsyncMock()
    address = "address"

    grouper = GeoGrouper(vendors=[mock_vendor_1, mock_vendor_2])

    result = await grouper.get_location(address)

    mock_vendor_1.forward_geocode.assert_awaited_with(address)
    assert result is mock_vendor_1.forward_geocode.return_value
    mock_vendor_2.forward_geocode.assert_not_awaited()


@pytest.mark.asyncio
async def test_grouper_get_location__second_vendor():
    mock_vendor_1 = Mock()
    mock_vendor_1.forward_geocode = AsyncMock(return_value=None)
    mock_vendor_2 = Mock()
    mock_vendor_2.forward_geocode = AsyncMock()
    address = "address"

    grouper = GeoGrouper(vendors=[mock_vendor_1, mock_vendor_2])

    result = await grouper.get_location(address)

    mock_vendor_1.forward_geocode.assert_awaited_with(address)
    mock_vendor_2.forward_geocode.assert_awaited_with(address)
    assert result is mock_vendor_2.forward_geocode.return_value


@pytest.mark.asyncio
async def test_grouper_get_location__no_result():
    mock_vendor_1 = Mock()
    mock_vendor_1.forward_geocode = AsyncMock(return_value=None)
    mock_vendor_2 = Mock()
    mock_vendor_2.forward_geocode = AsyncMock(return_value=None)
    address = "address"

    grouper = GeoGrouper(vendors=[mock_vendor_1, mock_vendor_2])

    result = await grouper.get_location(address)

    mock_vendor_1.forward_geocode.assert_awaited_with(address)
    mock_vendor_2.forward_geocode.assert_awaited_with(address)
    assert result is None


@pytest.mark.asyncio
async def test_set_users_location():
    grouper = GeoGrouper(vendors=[Mock()])
    grouper.get_location = AsyncMock()
    user1_mock = Mock()
    user2_mock = Mock()
    user_list = [user1_mock, user2_mock]
    users = await grouper.set_users_location(user_list)

    grouper.get_location.assert_has_awaits(calls=[call(u.address) for u in user_list])
    for user in users:
        assert user.location is grouper.get_location.return_value
    assert user_list == users


def test_create_groups():  # Using real data instead of mocking library because if we switch geo lib we dont want errors
    grouper = GeoGrouper(vendors=[Mock()], group_radius=30)

    user1 = User(name='John', location=Location(lat=40.7128, lon=-74.0060), address='123 str')
    user2 = User(name='Jack', location=Location(lat=40.7128, lon=-74.0061), address='123 str')

    user3 = User(name='Jill', location=Location(lat=40.7138, lon=-74.0060), address='321 str')

    users = [user1, user2, user3]

    groups = grouper._group_users_by_location(users)

    assert len(groups) == 2

    assert user1 in groups[0].users
    assert user2 in groups[0].users
    assert user3 in groups[1].users


@pytest.mark.asyncio
async def test_group_users_by_location():
    grouper = GeoGrouper(vendors=[Mock()])
    grouper.set_users_location = AsyncMock()
    grouper._group_users_by_location = Mock()
    users_list = [Mock()]
    groups = await grouper.group_users_by_address(users_list)

    grouper.set_users_location.assert_awaited_with(users_list)
    grouper._group_users_by_location.assert_called_with(grouper.set_users_location.return_value)
    assert groups is grouper._group_users_by_location.return_value


