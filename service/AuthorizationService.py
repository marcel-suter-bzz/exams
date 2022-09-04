from datetime import datetime, timedelta

import jwt
from flask import make_response, jsonify, Flask
from flask_restful import Resource, reqparse

from data.PersonDAO import PersonDAO

app = Flask(__name__)
app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'

parser = reqparse.RequestParser()
parser.add_argument('email', location='form', help='email')
parser.add_argument('password', location='form', help='password')


class AuthorizationService(Resource):
    """
    short description

    author: Marcel Suter
    """

    def __init__(self):
        """
        constructor

        Parameters:

        """
        pass

    def post(self):
        """
        authenticates a user
        :return: http response
        """
        args = parser.parse_args()
        person_dao = PersonDAO()
        person = person_dao.read_person(args.email, args.password)

        if person is not None:
            token = jwt.encode({
                'email': args.email,
                'role': person.role,
                'exp': datetime.utcnow() + timedelta(minutes=45)
            },
                app.config['SECRET_KEY'], "HS256")

            return jsonify({
                'token': token,
                'email': person.email,
                'role': person.role
            })

        return make_response('could not verify', 404, {'Authentication': '"login failed"'})


if __name__ == '__main__':
    ''' Check if started directly '''
    pass
