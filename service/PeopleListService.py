from flask_restful import Resource, fields, marshal_with

from data.PersonDAO import PersonDAO
from util.token import token_required

resource_fields = {
    'firstname': fields.String,
    'lastname': fields.String,
    'email': fields.String
}


class PeoplelistService(Resource):
    """
    services for reading lists of people

    author: Marcel Suter
    """
    method_decorators = [token_required]

    def __init__(self):
        """
        constructor

        Parameters:

        """
        self._foo = ''

    @marshal_with(resource_fields)
    def get(self, user, filter_value):
        """
        get a list of people
        :param filter_value: the filter to be applied
        :return: JSON object with the people
        """
        person_dao = PersonDAO()
        peoplelist = person_dao.filtered_list(filter_value)
        return peoplelist


if __name__ == '__main__':
    ''' Check if started directly '''
    pass
