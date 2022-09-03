from flask import Flask, render_template, send_from_directory
from flask_restful import Resource, Api
from service.ExamService import ExamService
from service.ExamlistService import ExamlistService
from service.PersonService import PersonService
from service.PeopleListService import PeoplelistService

app = Flask(__name__)
api = Api(app)

api.add_resource(ExamService, '/exam', '/exam/<exam_uuid>')
api.add_resource(ExamlistService, '/exams/<filter_value>')
api.add_resource(PersonService, '/person')
api.add_resource(PeoplelistService, '/people/<filter_value>')

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/<path:path>')
def page(path):
    return send_from_directory('templates', path)

if __name__ == '__main__':
    app.run(debug=True)
