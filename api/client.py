import allure
import json
import requests
from requests import Response

from config.settings import settings


class APIClient:
    def __init__(self, base_url: str | None = None, token: str | None = None):
        self.base_url = (base_url or settings.base_url).rstrip("/")
        self.session = requests.Session()
        self.timeout = settings.timeout
        token = token if token is not None else settings.token
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.session.headers.update({"Accept": "application/json"})

    def _request(self, method: str, path: str, **kwargs) -> Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)

        with allure.step(f"{method.upper()} {url}"):
            if "json" in kwargs:
                allure.attach(
                    json.dumps(kwargs["json"], indent=2, ensure_ascii=False),
                    name="request body",
                    attachment_type=allure.attachment_type.JSON,
                )
            response = self.session.request(method, url, **kwargs)

            allure.attach(
                f"status: {response.status_code}\n"
                f"headers: {dict(response.headers)}\n"
                f"body: {response.text[:2000]}",
                name="response",
                attachment_type=allure.attachment_type.TEXT,
            )
        return response

    def get(self, path: str, **kwargs) -> Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> Response:
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> Response:
        return self._request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs) -> Response:
        return self._request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs) -> Response:
        return self._request("DELETE", path, **kwargs)

    def close(self):
        self.session.close()
