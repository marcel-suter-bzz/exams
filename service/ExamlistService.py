from flask import make_response
from flask_restful import Resource

from data.ExamDAO import ExamDAO
from util.token import token_required


class ExamlistService(Resource):
    """
    services for reading lists of exams

    author: Marcel Suter
    """
    method_decorators = [token_required]

    def __init__(self):
        """
        constructor

        Parameters:

        """
        pass

    def get(self, user, filter_value):
        """
        get a list of exams
        :param filter_value: the filter to be applied
        :return: JSON object with the exams
        """
        exam_dao = ExamDAO()
        examlist = exam_dao.filtered_list(filter_value)
        exams_json = '['
        for exam in examlist:
            data = exam.to_json()
            exams_json += data + ','
        exams_json = exams_json[:-1] + ']'
        return make_response(
            exams_json, 200
        )


if __name__ == '__main__':
    ''' Check if started directly '''
    pass
