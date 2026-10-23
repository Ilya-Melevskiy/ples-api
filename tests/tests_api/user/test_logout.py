import allure

from api.endpoints import UserEndpoints


@allure.epic("Users")
@allure.feature("Выход из профиля")
@allure.story("Выход из профиля")
class TestLogout:
    @allure.title(
        "POST /api/v1/auth/logout Успешный выход авторизованного пользователя"
    )
    def test_logout_correct_body_200(self, api_client_no_auth, login_by_email):
        login_by_email
        payload = {}
        response = api_client_no_auth.post(UserEndpoints.LOGOUT, json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert body["data"]["redirectUrl"] == "/"
        assert body["errors"] == []
