from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Стандартный ответ об ошибке."""

    detail: str
    code: int | None = None
