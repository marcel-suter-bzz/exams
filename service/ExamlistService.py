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

class ExamlistService(Resource):
    """
    services for reading lists of exams

    author: Marcel Suter
    """

    def __init__(self):
        """
        constructor

        Parameters:

        """
        self._foo = ''

    @marshal_with(resource_fields)
    def get(self, filter):
        """
        get a list of exams
        :param filter: the filter to be applied
        :return: JSON object with the exams
        """
        exam_dao = ExamDAO()
        examlist = exam_dao.filtered_list(filter)
        return examlist


if __name__ == '__main__':
    ''' Check if started directly '''
    pass
