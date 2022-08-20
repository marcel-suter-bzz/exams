from flask import Flask
from flask_restful import Resource, Api
from service.ExamService import ExamService
from service.ExamlistService import ExamlistService

app = Flask(__name__)
api = Api(app)

api.add_resource(ExamService, '/exam', '/exam/<exam_uuid>')
api.add_resource(ExamlistService, '/exams/<filter>')

if __name__ == '__main__':
    app.run(debug=True)
