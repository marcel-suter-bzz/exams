from flask import make_response
from flask_restful import Resource

from util.authorization import token_required, teacher_required


class EmailService(Resource):
    """
    services for CRUD of a single exam

    author: Marcel Suter
    """

    def __init__(self):
        """
        constructor

        Parameters:

        """
        pass

    @token_required
    @teacher_required
    def post(self):
        """
        creates a new exam
        :return: http response
        """
        args = self.parser.parse_args()
        self.save(args)
        return make_response('exam saved', 200)