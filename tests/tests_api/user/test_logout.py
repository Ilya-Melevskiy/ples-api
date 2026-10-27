import allure

from api.endpoints import UserEndpoints


@allure.epic("Users")
@allure.feature("Выход из профиля")
@allure.story("Выход из профиля")
class TestLogout:
    @allure.title(
        "POST /api/v1/auth/logout Успешный выход авторизованного пользователя"
    )
    def test_logout_correct_body_200(self, login_by_email):
        api_client_auth = login_by_email["api_client_auth"]
        payload = {}
        response = api_client_auth.post(UserEndpoints.LOGOUT, json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert body["data"]["redirectUrl"] == "/"
        assert body["errors"] == []

    @allure.title("POST /api/v1/auth/logout Успешный выход с указанием back_url")
    def test_logout_with_back_url_200(self, login_by_email):
        api_client_auth = login_by_email["api_client_auth"]
        payload = {}
        response = api_client_auth.post(
            UserEndpoints.LOGOUT, json=payload, params={"back_url": "/profile"}
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert body["data"]["redirectUrl"] == "/profile"
        assert body["errors"] == []

    @allure.title("POST /api/v1/auth/logout Повторный login после logout")
    def test_logout_login_after_logout_200(self, login_by_email):
        api_client_auth = login_by_email["api_client_auth"]
        email = login_by_email["email"]
        password = login_by_email["password"]
        payload = {}
        api_client_auth.post(UserEndpoints.LOGOUT, json=payload)
        payload = {"email": email, "password": password}
        response = api_client_auth.post(UserEndpoints.LOGIN_BY_EMAIL, json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Авторизация прошла успешно" in body["data"]["message"]
        assert body["data"]["redirectUrl"] == "/"
        assert body["errors"] == []

    @allure.title("POST /api/v1/auth/logout Logout гостем (без авторизации)")
    def test_logout_without_login(self, api_client_no_auth):
        payload = {}
        response = api_client_no_auth.post(UserEndpoints.LOGOUT, json=payload)

        assert response.status_code == 401
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert body["errors"][0]["message"] == "Необходимо авторизоваться на сайте"
        assert body["errors"][0]["code"] == "invalid_authentication"
        assert body["errors"][0]["customData"] is None
