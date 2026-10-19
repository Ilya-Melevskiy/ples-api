from pydantic import EmailStr, Field, ConfigDict

from api.models.base_model import ApiModel


class Geo(ApiModel):
    lat: str
    lng: str


class Address(ApiModel):
    street: str = Field(min_lenght=1)
    suite: str
    city: str
    zipcode: str
    geo: Geo | None = None


class Company(ApiModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    catchPhrase: str
    bs: str


class User(ApiModel):
    model_config = ConfigDict(extra="forbid")
    id: int
    name: str
    username: str
    email: EmailStr
    phone: str
    website: str
    address: Address
    company: Company


class UserCreate(ApiModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    username: str
    email: EmailStr
