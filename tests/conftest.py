import allure
import pytest
from faker import Faker
import re


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Автоматически прикрепляем детали падения к Allure.
    """
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        with allure.step("Test failed"):
            allure.attach(
                str(report.longrepr),
                name="failure details",
                attachment_type=allure.attachment_type.TEXT,
            )


@pytest.fixture
def faker_ru():
    return Faker("ru_RU")


@pytest.fixture
def faker_eu():
    return Faker()


@pytest.fixture
def faker_phone_number(faker_ru):
    phone = faker_ru.phone_number()
    digits = re.sub(r"\D", "", phone)
    formatted_phone = "+79" + digits[2:]

    return formatted_phone


@pytest.fixture
def faker_phone_number_starting_8(faker_ru):
    phone = faker_ru.phone_number()
    digits = re.sub(r"\D", "", phone)
    formatted_phone = "89" + digits[2:]

    return formatted_phone
