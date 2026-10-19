import allure
import pytest
from faker import Faker


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
