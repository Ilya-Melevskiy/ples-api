import pytest
from faker import Faker

from api.client import APIClient
from api.endpoints import Endpoints
from config.settings import settings


@pytest.fixture(scope="session")
def auth_token():
    """
    Логин один раз за сессию.
    """
    raw = APIClient(token="")
    try:
        r = raw.post(
            Endpoints.LOGIN,
            json={
                "username": settings.username,
                "password": settings.password,
            },
        )
        r.raise_for_status()
        return r.json()["access_token"]
    finally:
        raw.close()


@pytest.fixture(scope="session")
def auth_client(auth_token):
    """
    Авторизованный APIClient на всю сессию.
    """
    api = APIClient(token=auth_token)
    yield api
    api.close()


@pytest.fixture
def api_client_no_auth():
    """
    Клиент без токена — для негативных тестов (401).
    """
    api = APIClient(token="")
    yield api
    api.close()


fake = Faker()


@pytest.fixture
def make_user(api_client_no_auth, faker_ru):
    """Фабрика: создаёт пользователя через API, удаляет в teardown."""
    created_ids = []

    def _make(**overrides) -> dict:
        payload = {
            "name": faker_ru.name(),
            "username": faker_ru.user_name(),
            "email": faker_ru.email(),
        }
        payload.update(overrides)

        r = api_client_no_auth.post(Endpoints.USERS, json=payload)
        if r.status_code != 201:
            raise AssertionError(f"Create user failed: {r.status_code} {r.text}")

        user = r.json()
        created_ids.append(user["id"])
        return user

    yield _make

    for user_id in created_ids:
        api_client_no_auth.delete(Endpoints.USER.format(user_id=user_id))
