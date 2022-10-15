import json
from dataclasses import dataclass
from dateutil import parser
from datetime import datetime


@dataclass
class Token:
    """
    a refresh token for authentication

    author: Marcel Suter
    """

    email: str
    jwt: str
    expiration: datetime

    def to_json(self):
        jstring = '{"email":"' + self.email + '",' + \
            '"jwt":"' + self.jwt + '",' + \
            '"expiration":"' + str(self.expiration) + '"}'
        return jstring

    @property
    def emails(self):
        return self._emails

    @emails.setter
    def emails(self, value):
        self._emails = value

    @property
    def jwt(self):
        return self._jwt

    @jwt.setter
    def jwt(self, value):
        self._jwt = value

    @property
    def expiration(self):
        return self._expiration

    @expiration.setter
    def expiration(self, value):
        self._expiration = value