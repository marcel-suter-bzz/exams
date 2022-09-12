from functools import wraps
import jwt
from flask import Flask, jsonify, request, make_response, g

from data.PersonDAO import PersonDAO
from model.Person import Person

app = Flask(__name__)
app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'


def token_required(func):
    """
    checks if the authorization token is valid
    :param func: callback function
    :return:
    """

    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
            data = jwt.decode(token[7:], app.config['SECRET_KEY'], algorithms=["HS256"])
            email = data['email']
            person_dao = PersonDAO()
            g.user = person_dao.read_person(email)
        except:
            return make_response(jsonify({"message": "Invalid token!"}), 401)

        return func(*args, **kwargs)

    return decorator


def teacher_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if not g.user.role == 'teacher':
            return make_response(jsonify({"message": "not allowed for students"}), 401)
        return func(*args, **kwargs)

    return wrap


if __name__ == '__main__':
    ''' Check if started directly '''
    pass
