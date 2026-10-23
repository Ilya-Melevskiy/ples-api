import allure

from api.endpoints import UserEndpoints


@allure.epic("Users")
@allure.feature("Авторизация")
@allure.story("Вход по phone")
class TestLoginPhone:
    @allure.title(
        "POST /api/v1/auth/login/phone Успешный вход по phone с валидными учётными данными"
    )
    def test_login_by_phone_correct_body_200(
        self, api_client_no_auth, registration_natural_person
    ):
        phone = registration_natural_person["phone"]
        password = registration_natural_person["password"]
        payload = {"phone": phone, "password": password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_PHONE, json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Авторизация прошла успешно" in body["data"]["message"]
        assert body["data"]["redirectUrl"] == "/"
        assert body["errors"] == []

    @allure.title(
        "POST /api/v1/auth/login/phone Успешный вход по телефону через обёртку auth"
    )
    def test_login_by_email_correct_body_auth_wrapper_200(
        self, api_client_no_auth, registration_natural_person
    ):
        phone = registration_natural_person["phone"]
        password = registration_natural_person["password"]
        payload = {"auth": {"phone": phone, "password": password}}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_PHONE, json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Авторизация прошла успешно" in body["data"]["message"]
        assert body["data"]["redirectUrl"] == "/"
        assert body["errors"] == []

    @allure.title(
        "POST /api/v1/auth/login/phone Успешный вход с указанием back_url для редиректа"
    )
    def test_login_by_phone_with_back_url_200(
        self, api_client_no_auth, registration_natural_person
    ):
        phone = registration_natural_person["phone"]
        password = registration_natural_person["password"]
        payload = {"phone": phone, "password": password}
        response = api_client_no_auth.post(
            UserEndpoints.LOGIN_BY_PHONE, json=payload, params="back_url=/profile"
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Авторизация прошла успешно" in body["data"]["message"]
        assert body["data"]["redirectUrl"] == "/profile"
        assert body["errors"] == []

    @allure.title(
        "POST /api/v1/auth/login/phone Вход с неверным паролем для существующего телефона"
    )
    def test_login_by_phone_incorrect_password_502(
        self, api_client_no_auth, registration_natural_person, faker_ru
    ):
        phone = registration_natural_person["phone"]
        password = f"a1{faker_ru.password(length=4)}"
        payload = {"phone": phone, "password": password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_PHONE, json=payload)

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Введен некорректный номер телефона или неверный пароль"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/login/phone Вход с телефоном несуществующего пользователя"
    )
    def test_login_by_phone_nonexistent_user_502(
        self, api_client_no_auth, faker_phone_number_starting_plus_7, faker_ru
    ):
        phone = faker_phone_number_starting_plus_7()
        password = f"a1{faker_ru.password(length=4)}"
        payload = {"phone": phone, "password": password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_PHONE, json=payload)

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            f"Пользователь с указанным номером телефона '{phone}' не найден"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title("POST /api/v1/auth/login/phone Запрос с пустым телом")
    def test_login_by_phone_empty_body_400(self, api_client_no_auth):
        payload = {}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_PHONE, json=payload)

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None

        assert "Значение поля не может быть пустым" in body["errors"][1]["message"]
        assert body["errors"][1]["code"] == "password"
        assert body["errors"][1]["customData"] is None

    @allure.title("POST /api/v1/auth/login/phone Запрос без обязательного поля phone")
    def test_login_by_phone_without_phone_400(self, api_client_no_auth, faker_ru):
        password = f"a1{faker_ru.password(length=4)}"
        payload = {"password": password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_PHONE, json=payload)

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/login/phone Запрос без обязательного поля password"
    )
    def test_login_by_phone_without_password_400(
        self, api_client_no_auth, registration_natural_person, faker_ru
    ):
        phone = registration_natural_person["phone"]
        payload = {"phone": phone}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_PHONE, json=payload)

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Значение поля не может быть пустым" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "password"
        assert body["errors"][0]["customData"] is None

    @allure.title("POST /api/v1/auth/login/phone Запрос с телефоном из 10 цифр")
    def test_login_by_phone_phone_10_numbers_400(
        self, api_client_no_auth, registration_natural_person
    ):
        phone = registration_natural_person["phone"]
        new_phone = phone[:-1]
        password = registration_natural_person["phone"]
        payload = {"phone": new_phone, "password": password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_PHONE, json=payload)

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None

    @allure.title("POST /api/v1/auth/login/phone Запрос с телефоном из 12 цифр")
    def test_login_by_phone_phone_12_numbers_400(
        self, api_client_no_auth, registration_natural_person
    ):
        phone = registration_natural_person["phone"]
        new_phone = f"{phone}1"
        password = registration_natural_person["phone"]
        payload = {"phone": new_phone, "password": password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_PHONE, json=payload)

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None

    @allure.title("POST /api/v1/auth/login/phone Запрос с телефоном с 8 в начале")
    def test_login_by_phone_phone_starting_8_400(
        self, api_client_no_auth, faker_phone_number_starting_8, faker_ru
    ):
        phone = faker_phone_number_starting_8
        password = faker_ru.password()
        payload = {"phone": phone, "password": password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_PHONE, json=payload)

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/login/phone Повторный вход уже авторизованного пользователя"
    )
    def test_login_by_phone_user_authorized_400(
        self, api_client_no_auth, registration_natural_person
    ):
        phone = registration_natural_person["phone"]
        password = registration_natural_person["password"]
        payload = {"phone": phone, "password": password}
        api_client_no_auth.post(UserEndpoints.LOGIN_BY_PHONE, json=payload)
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_PHONE, json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "error"
        assert (
            "Запрашиваемое действие разрешено только посетителям"
            in body["errors"][0]["message"]
        )
        assert body["data"] is None
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None
