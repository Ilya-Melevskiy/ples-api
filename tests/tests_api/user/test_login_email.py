import allure

from api.endpoints import UserEndpoints


@allure.epic("Users")
@allure.feature("Авторизация")
@allure.story("Вход по email")
class TestLoginEmail:
    @allure.title(
        "POST /api/v1/auth/login/email Успешный вход по email с валидными учётными данными"
    )
    def test_login_by_email_correct_body_200(
        self, api_client_no_auth, registration_natural_person
    ):
        email = registration_natural_person["email"]
        password = registration_natural_person["password"]
        payload = {"email": email, "password": password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_EMAIL, json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Авторизация прошла успешно" in body["data"]["message"]
        assert body["data"]["redirectUrl"] == "/"
        assert body["errors"] == []

    @allure.title(
        "POST /api/v1/auth/login/email Успешный вход по email через обёртку auth"
    )
    def test_login_by_email_correct_body_auth_wrapper_200(
        self, api_client_no_auth, registration_natural_person
    ):
        email = registration_natural_person["email"]
        password = registration_natural_person["password"]
        payload = {"auth": {"email": email, "password": password}}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_EMAIL, json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Авторизация прошла успешно" in body["data"]["message"]
        assert body["data"]["redirectUrl"] == "/"
        assert body["errors"] == []

    @allure.title(
        "POST /api/v1/auth/login/email Успешный вход с указанием back_url для редиректа"
    )
    def test_login_by_email_with_back_url_200(
        self, api_client_no_auth, registration_natural_person
    ):
        email = registration_natural_person["email"]
        password = registration_natural_person["password"]
        payload = {"email": email, "password": password}
        response = api_client_no_auth.post(
            UserEndpoints.LOGIN_BY_EMAIL, json=payload, params="back_url=/profile"
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Авторизация прошла успешно" in body["data"]["message"]
        assert body["data"]["redirectUrl"] == "/profile"
        assert body["errors"] == []

    @allure.title(
        "POST /api/v1/auth/login/email Вход с неверным паролем для существующего email"
    )
    def test_login_by_email_incorrect_password_502(
        self, api_client_no_auth, registration_natural_person, faker_ru
    ):
        email = registration_natural_person["email"]
        password = f"a1{faker_ru.password(length=4)}"
        payload = {"email": email, "password": password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_EMAIL, json=payload)

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Введен некорректный email или неверный пароль"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/login/email Вход с email несуществующего пользователя"
    )
    def test_login_by_email_nonexistent_user_502(self, api_client_no_auth, faker_ru):
        email = faker_ru.email()
        password = f"a1{faker_ru.password(length=4)}"
        payload = {"email": email, "password": password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_EMAIL, json=payload)

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            f"Пользователь с указанным email '{email}' не найден"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title("POST /api/v1/auth/login/email Запрос с пустым телом")
    def test_login_by_email_empty_body_400(self, api_client_no_auth):
        payload = {}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_EMAIL, json=payload)

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Значение поля не является адресом электронной почты"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "email"
        assert body["errors"][0]["customData"] is None

        assert "Значение поля не может быть пустым" in body["errors"][1]["message"]
        assert body["errors"][1]["code"] == "password"
        assert body["errors"][1]["customData"] is None

    @allure.title("POST /api/v1/auth/login/email Запрос без обязательного поля email")
    def test_login_by_email_without_email_400(self, api_client_no_auth, faker_ru):
        password = f"a1{faker_ru.password(length=4)}"
        payload = {"password": password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_EMAIL, json=payload)

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Значение поля не является адресом электронной почты"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "email"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/login/email Запрос без обязательного поля password"
    )
    def test_login_by_email_without_password_400(self, api_client_no_auth, faker_ru):
        email = faker_ru.email()
        payload = {"email": email}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_EMAIL, json=payload)

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Значение поля не может быть пустым" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "password"
        assert body["errors"][0]["customData"] is None

    @allure.title("POST /api/v1/auth/login/email Запрос c email без @")
    def test_login_by_email_email_without_at_400(
        self, api_client_no_auth, registration_natural_person
    ):
        email = registration_natural_person["email"]
        email_without_at = email.replace("@", "")
        password = registration_natural_person["password"]
        payload = {"email": email_without_at, "password": password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_EMAIL, json=payload)

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Значение поля не является адресом электронной почты"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "email"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/login/email Повторный вход уже авторизованного пользователя"
    )
    def test_login_by_email_user_authorized_400(
        self, api_client_no_auth, registration_natural_person
    ):
        email = registration_natural_person["email"]
        password = registration_natural_person["password"]
        payload = {"email": email, "password": password}
        api_client_no_auth.post(UserEndpoints.LOGIN_BY_EMAIL, json=payload)
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_EMAIL, json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Запрашиваемое действие разрешено только посетителям"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None
