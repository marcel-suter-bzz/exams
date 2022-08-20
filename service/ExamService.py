import json

import flask
from flask import Flask, Request
from flask_restful import Resource, fields, marshal_with, reqparse
from data.ExamDAO import ExamDAO
from model.Exam import Exam

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

parser = reqparse.RequestParser()
parser.add_argument('exam_uuid', location='form', help='uuid')
parser.add_argument('teacher', location='form', help='teacher')
parser.add_argument('student', location='form', help='student')
parser.add_argument('cohort', location='form', help='cohort')
parser.add_argument('email', location='form', help='email')
parser.add_argument('module', location='form', help='module')
parser.add_argument('exam_num', location='form', help='exam-num')
parser.add_argument('duration', location='form', type=str, help='Muss eine Ganzzahl sein')
parser.add_argument('remarks', location='form', help='remarks')
parser.add_argument('tools', location='form', help='tools')
parser.add_argument('datetime', location='form', help='datetime')
parser.add_argument('status', location='form', help='status')


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
        pass

    @marshal_with(resource_fields)
    def get(self, exam_uuid):
        exam_dao = ExamDAO()
        exam = exam_dao.read_exam(exam_uuid)
        if len(exam) == 0:
            return None, 404
        return exam, 200

    def post(self):
        args = parser.parse_args()
        exam = Exam(
            None,
            args.teacher,
            args.student,
            args.cohort,
            args.email,
            args.module,
            args.exam_num,
            args.duration,
            args.remarks,
            args.tools,
            args.datetime,
            args.status
        )
        exam_dao = ExamDAO()
        exam_dao.save_exam(exam)
        return exam, 201

    def put(self):
        args = parser.parse_args()
        exam = Exam(
            args.exam_uuid,
            args.teacher,
            args.student,
            args.cohort,
            args.email,
            args.module,
            args.exam_num,
            args.duration,
            args.remarks,
            args.tools,
            args.datetime,
            args.status
        )
        exam_dao = ExamDAO()
        exam_dao.save_exam(exam)
        return exam, 200

if __name__ == '__main__':
    ''' Check if started directly '''
    pass
