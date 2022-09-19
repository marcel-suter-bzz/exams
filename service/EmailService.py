from flask import make_response, current_app
from flask_mail import Mail, Message
from flask_restful import Resource

from data.ExamDAO import ExamDAO
from data.EventDAO import EventDAO
from util.authorization import token_required, teacher_required
from util.replace import replace_text


class EmailService(Resource):
    """
    services for sending emails
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
    def get(self, exam_uuid, type):
        """
        sends an email
        :param exam_uuid: the unique key
        :param type: the type of email to be sent
        :return: http response
        """
        exam_dao = ExamDAO()
        exam = exam_dao.read_exam(exam_uuid)
        http_status = 404
        if exam is not None:
            self.create_email(exam, type)
        return make_response('email sent', 200)

    def create_email(self, exam, type):
        """
        creates an email for the selected exam and type
        :param exam: the unique uuid for an exam
        :param type: the type of email (missed, ...)
        :return: successful
        """
        event_dao = EventDAO()
        event = event_dao.read_event(exam.event_uuid)
        filename = current_app.config['TEMPLATEPATH']
        if type == 'missed':
            filename += 'missed.txt'
            sender = exam.teacher.email
        elif type == 'invitation':
            filename += 'invitation.txt'
            sender = event.supervisors[0]
        file = open(filename)
        text = file.read()
        data = {'student.lastname': exam.student.lastname,
                'teacher.firstname': exam.teacher.firstname,
                'teacher.lastname': exam.teacher.lastname,
                'missed': exam.missed,
                'module': exam.module,
                'event.date': event.timestamp.split(' ')[0],
                'event.time': event.timestamp.split(' ')[1],
                'room': 'H100',  # FIXME from exam or event?
                'tools': exam.tools
                }
        text = replace_text(data, text)
        self.send_email(sender, exam.student.email, text)
        return True

    def send_email(self, sender, recipient, content):
        '''
        mail = Mail(current_app)
        msg = Message('Verpasste Prüfung', sender='marcel@ghwalin.ch', recipients=[recipient], reply_to=sender)
        msg.body = content
        mail.send(msg)
        '''
        print ('From: ' + sender)
        print ('To:' + recipient)
        print (content)
