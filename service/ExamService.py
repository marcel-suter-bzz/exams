import json

from flask_restful import Resource, fields, marshal_with
from data.ExamDAO import ExamDAO

resource_fields = {
    'exam_uuid': fields.String,
    'teacher': fields.String,
    'student': fields.String,
    'module': fields.String,
    'exam_num': fields.String,
    'duration': fields.Integer,
    'remarks': fields.String,
    'tools': fields.String,
    'datetime': fields.String,
    'status': fields.String
}


class ExamService(Resource):
    """
    services for CRUD of a single exam

    author: Marcel Suter
    """

    def __init__(self):
        """
        constructor

        Parameters:

        """
        self._foo = ''

    @marshal_with(resource_fields)
    def get(self, exam_uuid):
        exam_dao = ExamDAO()
        exam = exam_dao.read_exam(exam_uuid)
        if len(exam) == 0:
            return None,404
        return exam,200


if __name__ == '__main__':
    ''' Check if started directly '''
    pass
