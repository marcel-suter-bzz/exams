from flask import make_response
from flask_restful import Resource, reqparse
from data.PersonDAO import PersonDAO
from model.Person import Person
from util.token import token_required


parser = reqparse.RequestParser()
parser.add_argument('email', location='form', help='email')
parser.add_argument('firstname', location='form', help='Vorname')
parser.add_argument('lastname', location='form', help='Nachname')
parser.add_argument('role', location='form', help='Rolle')


class PersonService(Resource):
    """
    short description

    author: Marcel Suter
    """
    method_decorators = [token_required]

    def __init__(self):
        """
        constructor

        Parameters:

        """
        pass

    def get(self, user, email):
        """
        gets a person identified by the email
        :param email: the unique key
        :return: http response
        """
        person_dao = PersonDAO()
        person = person_dao.read_exam(email)
        data = '{}'
        http_status = 404
        if person is not None:
            http_status = 200
            data = person.to_json()

        return make_response(
            data, http_status
        )

    def post(self, user):
        """
        creates a new person
        :return: http response
        """
        args = parser.parse_args()
        person = Person(
            args.email,
            args.firstname,
            args.lastname,
            args.role
        )
        person_dao = PersonDAO()
        person_dao.save_person(person)
        return person, 201

    def put(self, user):
        """
        updates an existing person
        :return: http response
        """
        return self.post()


if __name__ == '__main__':
    ''' Check if started directly '''
    pass
