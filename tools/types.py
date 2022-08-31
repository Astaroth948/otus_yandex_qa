from dataclasses import dataclass


@dataclass
class AuthData:
    url: str
    login: str
    password: str
