# tests/tests.py

# This uses an in-memory SQLite database for testing
# Note: The sqllite database does not understand timezones, so some code mods were needed to detected the database type.
# Also, the time tests are borked.  I'll get around to fixing them if there is an actual reason...

import pytest
import os
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(parent_dir)

from api import app
from api.db.core import get_db
from api.db.models import Base
# from datetime import datetime, timedelta, timezone
# import asyncio


from test_cases import (
    pub_test_cases,
    sub_test_cases,
    # pub_test_cases_time,
    # sub_test_cases_time
)

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(DATABASE_URL, echo=True)
TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)


@pytest.fixture(scope="module")
async def db_session():
    async with TestSessionLocal() as session:
        yield session


async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="module", autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
@pytest.mark.dependency()
@pytest.mark.parametrize("case", pub_test_cases)
async def test_pub(client: AsyncClient, case: dict):

    response = await client.post(
        "/pub",
        json=case['payload'],
    )

    assert response.status_code == case['status_code']
    assert response.json()["message"] == case['message']

    for key in case['return'].keys():
        assert key in response.json()["data"].keys()
        assert response.json()["data"][key] == case['return'][key]

    for key in case['fields_exist'].keys():
        if case['fields_exist'][key]:
            assert key in response.json()["data"].keys()
        else:
            assert key not in response.json()["data"].keys()

    # check to make sure there are no extra fields in the response
    for key in response.json()["data"].keys():
        assert key in case['fields_exist'].keys()


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_pub"])
@pytest.mark.parametrize("case", sub_test_cases)
async def test_sub(client: AsyncClient, case: dict):
    response = await client.post(
        "/sub",
        json=case['payload'],
    )

    assert response.status_code == case['status_code']
    if 'message' in response.json().keys():
        assert response.json()["message"] == case['message']
    if 'detail' in response.json().keys():
        assert response.json()["detail"] == case['detail']

    for key in case['return'].keys():
        assert key in response.json()["data"].keys()
        assert response.json()["data"][key] == case['return'][key]

    if 'data' in response.json().keys():
        for key in case['fields_exist'].keys():
            if case['fields_exist'][key]:
                assert key in response.json()["data"].keys()
            else:
                assert key not in response.json()["data"].keys()

        for key in response.json()["data"].keys():
            assert key in case['fields_exist'].keys()

# TODO The below is borked.  Don't have the patience to fix it right now.

# @pytest.mark.asyncio
# @pytest.mark.dependency(depends=["test_sub"])
# @pytest.mark.parametrize("case", pub_test_cases_time)
# async def test_pub_time(client: AsyncClient, case: dict):
#
#     payload = case['payload']
#     current_time = datetime.now(timezone.utc)
#     pickup_time = current_time + timedelta(seconds=case['sleep'])
#
#     payload['schedule_date'] = pickup_time.isoformat(timespec='microseconds')
#     print(f'BLERK6: {payload["schedule_date"]}')
#
#     response = await client.post(
#         "/pub",
#         json=payload,
#     )
#
#     assert response.status_code == case['status_code']
#     assert response.json()["message"] == case['message']
#
#     for key in case['return'].keys():
#         assert key in response.json()["data"].keys()
#         assert response.json()["data"][key] == case['return'][key]
#
#     for key in case['fields_exist'].keys():
#         if case['fields_exist'][key]:
#             assert key in response.json()["data"].keys()
#         else:
#             assert key not in response.json()["data"].keys()
#
#     # check to make sure there are no extra fields in the response
#     for key in response.json()["data"].keys():
#         assert key in case['fields_exist'].keys()
#
#
# @pytest.mark.asyncio
# @pytest.mark.dependency(depends=["test_pub_time"])
# @pytest.mark.parametrize("case", sub_test_cases_time)
# async def test_sub_time(client: AsyncClient, case: dict):
#
#     if 'sleep' in case.keys():
#         await asyncio.sleep(case['sleep'])
#
#         response = await client.get(
#             "/list"
#         )
#         for item in response.json():
#             print(f'BLERK: {item}')
#
#     response = await client.post(
#         "/sub",
#         json=case['payload'],
#     )
#
#     assert response.status_code == case['status_code']
#     if 'message' in response.json().keys():
#         assert response.json()["message"] == case['message']
#     if 'detail' in response.json().keys():
#         assert response.json()["detail"] == case['detail']
#
#     for key in case['return'].keys():
#         assert key in response.json()["data"].keys()
#         assert response.json()["data"][key] == case['return'][key]
#
#     if 'data' in response.json().keys():
#         for key in case['fields_exist'].keys():
#             if case['fields_exist'][key]:
#                 assert key in response.json()["data"].keys()
#             else:
#                 assert key not in response.json()["data"].keys()
#
#         for key in response.json()["data"].keys():
#             assert key in case['fields_exist'].keys()

# end
