import allure
import pytest

from api.endpoints import Endpoints
from api.models.user import User, UserCreate


@allure.epic("Users API")
@allure.feature("Users")
@pytest.mark.smoke
class TestUsersGet:
    @allure.story("Get list of users")
    @allure.title("GET /users returns 200 and non-empty list")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_users(self, api_client_no_auth):
        response = api_client_no_auth.get(Endpoints.USERS)

        assert response.status_code == 200
        users = [User.model_validate(u) for u in response.json()]
        assert len(users) > 0

    @allure.story("Get single user")
    @allure.title("GET /users/{id} returns correct user")
    @pytest.mark.parametrize("user_id", [1, 2, 3])
    def test_get_user_by_id(self, api_client_no_auth, user_id):
        response = api_client_no_auth.get(Endpoints.USER.format(user_id=user_id))

        assert response.status_code == 200
        user = User.model_validate(response.json())
        assert user.id == user_id

    @allure.story("Get single user")
    @allure.title("GET /users/{id} returns 404 for unknown id")
    @pytest.mark.negative
    def test_get_unknown_user(self, api_client_no_auth):
        response = api_client_no_auth.get(Endpoints.USER.format(user_id=999999))
        assert response.status_code == 404

    @allure.title("User created via factory can be fetched by id")
    def test_created_user_fetchable(self, api_client_no_auth, make_user):
        user = make_user()  # создали через фабрику
        response = api_client_no_auth.get(Endpoints.USER.format(user_id=user["id"]))

        assert response.status_code == 200
        fetched = response.json()
        assert fetched["id"] == user["id"]
        assert fetched["username"] == user["username"]


@allure.epic("Users API")
@allure.feature("Users")
@allure.story("Create user")
@pytest.mark.smoke
class TestUsersCreateSmoke:
    @allure.title("POST /users creates user with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self, api_client_no_auth, faker_ru):
        payload = UserCreate(
            name=faker_ru.name(),
            username=faker_ru.user_name(),
            email=faker_ru.email(),
        )

        response = api_client_no_auth.post(
            Endpoints.USERS,
            json=payload.model_dump(),
        )

        assert response.status_code == 201
        created = response.json()
        assert created["name"] == payload.name
        assert created["username"] == payload.username
        assert created["email"] == payload.email

    @allure.title("User created via factory can be fetched by id")
    def test_created_user_fetchable(self, api_client_no_auth, make_user):
        user = make_user()

        response = api_client_no_auth.get(Endpoints.USER.format(user_id=user["id"]))

        assert response.status_code == 200
        fetched = response.json()
        assert fetched["id"] == user["id"]
        assert fetched["username"] == user["username"]


@allure.epic("Users API")
@allure.feature("Users")
@allure.story("Users negative scenarios")
@pytest.mark.negative
class TestUsersNegative:
    @allure.title("GET /users/{user_id} returns 404 for unknown id")
    def test_get_unknown_user(self, api_client_no_auth):
        response = api_client_no_auth.get(Endpoints.USER.format(user_id=999999))
        assert response.status_code == 404

    @allure.title("POST /users rejects invalid email: {email}")
    @pytest.mark.parametrize(
        "email",
        [
            "not-an-email",
            "missing@",
            "@missing-local.com",
            "",
        ],
        ids=["no-at", "no-domain", "no-local", "empty"],
    )
    def test_create_user_invalid_email(self, api_client_no_auth, faker_ru, email):
        payload = {
            "name": faker_ru.name(),
            "username": faker_ru.user_name(),
            "email": email,
        }
        response = api_client_no_auth.post(Endpoints.USERS, json=payload)

        assert response.status_code in (400, 422)
