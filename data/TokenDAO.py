import json
from datetime import datetime
from dateutil import parser
from flask import current_app

from model.Token import Token


class TokenDAO:
    """
    data access object for refresh tokens

    author: Marcel Suter
    """

    def __init__(self):
        """
        constructor

        Parameters:

        """
        self._tokendict = {}
        self.load_tokens()

    def read_jwt(self, email):
        """
        reads a refresh token from the dict
        :param email: the key
        :return: jwt token
        """
        if email in self._tokendict:
            return self._tokendict[email].jwt
        return None

    def insert_token(self, token):
        """
        inserts a new refresh token into the file
        :param token: the refresh token to be safed
        :return: None
        """
        key = token.email
        self._tokendict[key] = token

        token_json = '['
        for key in self._tokendict:
            data = self._tokendict[key].to_json()
            token_json += data + ','
        token_json = token_json[:-1] + ']'

        file = open(current_app.config['DATAPATH'] + 'tokens.json', 'w')
        file.write(token_json)
        file.close()

    def load_tokens(self):
        """
        loads all active tokens into a dict
        :return:
        """
        now = str(datetime.utcnow())
        file = open(current_app.config['DATAPATH'] + 'tokens.json')
        tokens = json.load(file)
        for item in tokens:
            if now < item['expiration']:
                token = Token(
                    email=item['email'],
                    expiration=item['expiration'],
                    jwt=item['jwt']
                )
                self._tokendict[item['email']] = token


if __name__ == '__main__':
    ''' Check if started directly '''
    pass