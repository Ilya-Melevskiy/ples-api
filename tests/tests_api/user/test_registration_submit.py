import allure

from api.endpoints import UserEndpoints


@allure.epic("Users")
@allure.feature("Регистрация")
@allure.story("Регистрация: Завершение регистрации")
class TestRegistrationSubmit:
    @allure.title(
        "POST /api/v1/auth/register/submit Успешная регистрация физического лица"
    )
    def test_registration_submit_natural_person_correct_body_200(
        self, api_client_no_auth, confirm_otp_phone, faker_ru
    ):
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            }
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Регистрация успешно завершена" in body["data"]["message"]
        assert body["data"]["redirectUrl"] == "/"
        assert body["errors"] == []

    @allure.title(
        "POST /api/v1/auth/register/submit Успешная регистрация юридического лица"
    )
    def test_registration_submit_legal_person_correct_body_200(
        self, api_client_no_auth, confirm_otp_phone, faker_ru, make_valid_inn_10
    ):
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            },
            "legal": {
                "inn": make_valid_inn_10,
                "shortName": faker_ru.company(),
                "fullName": f"Общество с ограниченной ответственностью '{faker_ru.company()}'",
                "kpp": faker_ru.kpp(),
                "ogrn": faker_ru.businesses_ogrn(),
                "bik": faker_ru.bic(),
                "bankName": faker_ru.bank(),
                "legalAddress": faker_ru.address(),
            },
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Регистрация успешно завершена" in body["data"]["message"]
        assert body["data"]["redirectUrl"] == "/"
        assert body["errors"] == []

    @allure.title(
        "POST /api/v1/auth/register/submit Успешная регистрация с указанием back_url"
    )
    def test_registration_submit_with_back_url_200(
        self, api_client_no_auth, confirm_otp_phone, faker_ru
    ):
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            }
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION,
            json=payload,
            params={"back_url": "/profile"},
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Регистрация успешно завершена" in body["data"]["message"]
        assert body["data"]["redirectUrl"] == "/profile"
        assert body["errors"] == []

    @allure.title(
        "POST /api/v1/auth/register/submit Submit без предварительного confirm"
    )
    def test_registration_submit_without_confirm_502(
        self, api_client_no_auth, faker_phone_number_starting_plus_7, faker_ru
    ):
        password = f"a1{faker_ru.password(length=4)}"
        phone = faker_phone_number_starting_plus_7()
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            }
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert (
            "Пользователь не подтвердил свой адрес электронной почты или номер телефона"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title("POST /api/v1/auth/register/submit Submit с занятым email")
    def test_registration_submit_existing_email_502(
        self,
        api_client_no_auth,
        registration_natural_person,
        faker_ru,
        confirm_otp_phone,
    ):
        email = registration_natural_person["email"]
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "email": email,
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            }
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert (
            f"Пользователь с таким email ({email}) уже существует"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title("POST /api/v1/auth/register/submit Submit с занятым ИНН (юрлицо)")
    def test_registration_submit_existing_inn_409(
        self,
        api_client_no_auth,
        registration_legal_person,
        faker_ru,
        confirm_otp_phone,
    ):
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        inn = registration_legal_person["inn"]
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            },
            "legal": {
                "inn": inn,
                "shortName": faker_ru.company(),
                "fullName": f"Общество с ограниченной ответственностью '{faker_ru.company()}'",
                "kpp": faker_ru.kpp(),
                "ogrn": faker_ru.businesses_ogrn(),
                "bik": faker_ru.bic(),
                "bankName": faker_ru.bank(),
                "legalAddress": faker_ru.address(),
            },
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 409
        body = response.json()
        assert body["status"] == "error"
        assert "Аккаунт с таким ИНН уже существует" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "INN_ALREADY_IN_USE"
        assert body["errors"][0]["customData"] is None

    @allure.title("POST /api/v1/auth/register/submit Запрос с пустым телом")
    def test_registration_submit_empty_body_400(self, api_client_no_auth):
        payload = {}
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert body["errors"]

    @allure.title(
        "POST /api/v1/auth/register/submit Запрос без обязательного поля email"
    )
    def test_registration_submit_without_email_400(
        self, api_client_no_auth, confirm_otp_phone, faker_ru
    ):
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            }
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert (
            "Значение поля не является адресом электронной почты"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "general.email"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/submit Запрос без обязательного поля phone"
    )
    def test_registration_submit_without_phone_400(
        self, api_client_no_auth, confirm_otp_email, faker_ru
    ):
        email = confirm_otp_email
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "email": email,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            }
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "general.phone"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/submit Запрос без обязательного поля password"
    )
    def test_registration_submit_without_password_400(
        self, api_client_no_auth, confirm_otp_phone, faker_ru
    ):
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            }
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert (
            "Значения поля не соответствует регулярному выражению"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "general.password"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/submit Запрос без обязательного поля passwordRepeat"
    )
    def test_registration_submit_without_password_repeat_400(
        self, api_client_no_auth, confirm_otp_phone, faker_ru
    ):
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            }
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert (
            "Значения поля не соответствует регулярному выражению"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "general.passwordRepeat"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/submit Запрос без обязательного поля firstName"
    )
    def test_registration_submit_without_first_name_400(
        self, api_client_no_auth, confirm_otp_phone, faker_ru
    ):
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            }
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert (
            "Длина строки должна быть не меньше, чем 2 знака"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "general.firstName"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/submit Запрос с password и passwordRepeat без цифр"
    )
    def test_registration_submit_password_without_numbers_400(
        self, api_client_no_auth, confirm_otp_phone, faker_ru
    ):
        phone = confirm_otp_phone
        password = faker_ru.pystr(min_chars=6, max_chars=6)
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            }
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert (
            "Значения поля не соответствует регулярному выражению"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "general.password"
        assert body["errors"][0]["customData"] is None
        assert (
            "Значения поля не соответствует регулярному выражению"
            in body["errors"][1]["message"]
        )
        assert body["errors"][1]["code"] == "general.passwordRepeat"
        assert body["errors"][1]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/submit Запрос с password и passwordRepeat без букв"
    )
    def test_registration_submit_password_without_letters_400(
        self, api_client_no_auth, confirm_otp_phone, faker_ru
    ):
        phone = confirm_otp_phone
        password = faker_ru.numerify(text="#" * 6)
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            }
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert (
            "Значения поля не соответствует регулярному выражению"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "general.password"
        assert body["errors"][0]["customData"] is None
        assert (
            "Значения поля не соответствует регулярному выражению"
            in body["errors"][1]["message"]
        )
        assert body["errors"][1]["code"] == "general.passwordRepeat"
        assert body["errors"][1]["customData"] is None

    @allure.title("POST /api/v1/auth/register/submit Запрос без обязательного поля inn")
    def test_registration_submit_legal_person_without_inn_400(
        self, api_client_no_auth, confirm_otp_phone, faker_ru
    ):
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            },
            "legal": {
                "shortName": faker_ru.company(),
                "fullName": f"Общество с ограниченной ответственностью '{faker_ru.company()}'",
                "kpp": faker_ru.kpp(),
                "ogrn": faker_ru.businesses_ogrn(),
                "bik": faker_ru.bic(),
                "bankName": faker_ru.bank(),
                "legalAddress": faker_ru.address(),
            },
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert "Некорректный ИНН" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "legal.inn"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/submit Запрос без обязательного поля shortName"
    )
    def test_registration_submit_legal_person_without_short_name_400(
        self, api_client_no_auth, confirm_otp_phone, faker_ru, make_valid_inn_10
    ):
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            },
            "legal": {
                "inn": make_valid_inn_10,
                "fullName": f"Общество с ограниченной ответственностью '{faker_ru.company()}'",
                "kpp": faker_ru.kpp(),
                "ogrn": faker_ru.businesses_ogrn(),
                "bik": faker_ru.bic(),
                "bankName": faker_ru.bank(),
                "legalAddress": faker_ru.address(),
            },
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert (
            "Короткое наименование организации должно быть не менее 3 и не более 255 символов"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "legal.shortName"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/submit Запрос без обязательного поля fullName"
    )
    def test_registration_submit_legal_person_without_full_name_400(
        self, api_client_no_auth, confirm_otp_phone, faker_ru, make_valid_inn_10
    ):
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            },
            "legal": {
                "inn": make_valid_inn_10,
                "shortName": faker_ru.company(),
                "kpp": faker_ru.kpp(),
                "ogrn": faker_ru.businesses_ogrn(),
                "bik": faker_ru.bic(),
                "bankName": faker_ru.bank(),
                "legalAddress": faker_ru.address(),
            },
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert (
            "Полное наименование организации должно быть не менее 3 и не более 255 символов"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "legal.fullName"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/submit Запрос без обязательного поля ogrn"
    )
    def test_registration_submit_legal_person_without_ogrn_400(
        self, api_client_no_auth, confirm_otp_phone, faker_ru, make_valid_inn_10
    ):
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            },
            "legal": {
                "inn": make_valid_inn_10,
                "shortName": faker_ru.company(),
                "fullName": f"Общество с ограниченной ответственностью '{faker_ru.company()}'",
                "kpp": faker_ru.kpp(),
                "bik": faker_ru.bic(),
                "bankName": faker_ru.bank(),
                "legalAddress": faker_ru.address(),
            },
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert "ОГРН должен содержать 13 или 15 цифр" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "legal.ogrn"
        assert body["errors"][0]["customData"] is None

    @allure.title("POST /api/v1/auth/register/submit Запрос без обязательного поля bik")
    def test_registration_submit_legal_person_without_bik_400(
        self, api_client_no_auth, confirm_otp_phone, faker_ru, make_valid_inn_10
    ):
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            },
            "legal": {
                "inn": make_valid_inn_10,
                "shortName": faker_ru.company(),
                "fullName": f"Общество с ограниченной ответственностью '{faker_ru.company()}'",
                "kpp": faker_ru.kpp(),
                "ogrn": faker_ru.businesses_ogrn(),
                "bankName": faker_ru.bank(),
                "legalAddress": faker_ru.address(),
            },
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert "Некорректный БИК" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "legal.bik"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/submit Запрос без обязательного поля bankName"
    )
    def test_registration_submit_legal_person_without_bank_name_400(
        self, api_client_no_auth, confirm_otp_phone, faker_ru, make_valid_inn_10
    ):
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            },
            "legal": {
                "inn": make_valid_inn_10,
                "shortName": faker_ru.company(),
                "fullName": f"Общество с ограниченной ответственностью '{faker_ru.company()}'",
                "kpp": faker_ru.kpp(),
                "ogrn": faker_ru.businesses_ogrn(),
                "bik": faker_ru.bic(),
                "legalAddress": faker_ru.address(),
            },
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert (
            "Наименование банка должно быть не менее 3 и не более 255 символов"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "legal.bankName"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/submit Запрос без обязательного поля legalAddress"
    )
    def test_registration_submit_legal_person_without_legal_address_400(
        self, api_client_no_auth, confirm_otp_phone, faker_ru, make_valid_inn_10
    ):
        phone = confirm_otp_phone
        password = f"a1{faker_ru.password(length=4)}"
        payload = {
            "general": {
                "email": faker_ru.email(),
                "phone": phone,
                "password": password,
                "passwordRepeat": password,
                "firstName": faker_ru.first_name(),
                "lastName": faker_ru.last_name(),
                "secondName": faker_ru.middle_name(),
            },
            "legal": {
                "inn": make_valid_inn_10,
                "shortName": faker_ru.company(),
                "fullName": f"Общество с ограниченной ответственностью '{faker_ru.company()}'",
                "kpp": faker_ru.kpp(),
                "ogrn": faker_ru.businesses_ogrn(),
                "bik": faker_ru.bic(),
                "bankName": faker_ru.bank(),
            },
        }
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_COMPLETION, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert (
            "Юр.адрес организации должен быть не менее 3 и не более 255 символов"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "legal.legalAddress"
        assert body["errors"][0]["customData"] is None
