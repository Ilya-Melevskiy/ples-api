import allure

from api.endpoints import AuthEndpoints


@allure.epic("Users")
@allure.feature("Авторизация")
class TestLoginByEmail:
    @allure.title("GET /users Успешный вход по email с валидными учётными данными")
    def test_login_by_email_200(self, api_client_no_auth):
        payload = {"email": "test599@mail.ru", "password": "232323qq"}
        response = api_client_no_auth.post(AuthEndpoints.LOGIN_BY_EMAIL, json=payload)
        body = response.json()

        assert response.status_code == 200
        assert body["status"] == "success"
        assert "успешно" in body["data"]["message"]
        assert body["data"]["redirectUrl"] == "/"
        assert body["errors"] == []
