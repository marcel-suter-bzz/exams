from flask_restful import Resource, fields, marshal_with, reqparse
from data.PersonDAO import PersonDAO
from model.Person import Person
from util.token import token_required

resource_fields = {
    'email': fields.String,
    'firstname': fields.String,
    'lastname': fields.String,
    'role': fields.String
}

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

    @marshal_with(resource_fields)
    def get(self, user, email):
        """
        gets a person identified by the email
        :param email: the unique key
        :return: http response
        """
        person_dao = PersonDAO()
        person = person_dao.read_exam(email)
        if person is None:
            return None, 404
        return person, 200

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
