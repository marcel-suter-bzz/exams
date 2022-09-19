import json

from flask import make_response, current_app
from flask_mail import Mail, Message
from flask_restful import Resource
from fpdf import FPDF

from data.ExamDAO import ExamDAO
from data.EventDAO import EventDAO
from util.authorization import token_required, teacher_required
from util.replace import replace_text


class PrintService(Resource):
    """
    services for printing
    author: Marcel Suter
    """

    def __init__(self):
        """
        constructor

        Parameters:

        """
        pass

    #@token_required  FIXME
    #@teacher_required
    def get(self, exam_uuid):
        """
        sends a pdf
        :param exam_uuid: the unique key
        :return: http response
        """
        exam_dao = ExamDAO()
        exam = exam_dao.read_exam(exam_uuid)
        http_status = 404
        if exam is not None:
            output = self.create_pdf(exam)
            response = make_response(output)
            response.headers["Content-Type"] = "application/pdf"
            return response
        return make_response('not found', 404)

    def create_pdf(self, exam):
        """
        creates an email for the selected exam and type
        :param exam: the unique uuid for an exam
        :param type: the type of email (missed, ...)
        :return: pdf file
        """
        event_dao = EventDAO()
        event = event_dao.read_event(exam.event_uuid)
        filename = current_app.config['TEMPLATEPATH'] + 'sheet.json'
        file = open(filename)
        texts = json.load(file)
        data = {'student.firstname': exam.student.firstname,
                'student.lastname': exam.student.lastname,
                'teacher.firstname': exam.teacher.firstname,
                'teacher.lastname': exam.teacher.lastname,
                'cohort': exam.cohort,
                'missed': exam.missed,
                'module': exam.module,
                'exam_num': exam.exam_num,
                'duration': str(exam.duration),
                'event.date': event.timestamp.split(' ')[0],
                'event.time': event.timestamp.split(' ')[1],
                'room': exam.room,
                'tools': exam.tools,
                'remarks': exam.remarks
                }
        return self.send_email(texts, data)

    def send_email(self, contents, data):
        """
        creates a pdf
        :param contents: the contents of the pdf
        :param data: replacement values for the placeholders
        :return: pdf
        """
        margin_left = 15
        margin_top = 25
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('helvetica', '', 12)
        pdf.set_fill_color(r=192, g=192, b=192)
        pdf.set_line_width(0.5)
        for item in contents:
            xcoord = margin_left + item['xcoord'] * 4
            ycoord = margin_top + item['ycoord'] * 6
            if item['type'] == 'text':
                content = replace_text(data, item['content'])
                style = ''
                if item.get('bold') is not None:
                    style='B'
                pdf.set_font(style=style)
                pdf.text(xcoord, ycoord, content)
            elif item['type'] == 'line':
                ycoord -= 3
                xcoord_end = xcoord + item['width'] * 4
                ycoord_end = ycoord
                pdf.line(xcoord, ycoord, xcoord_end, ycoord_end)
            elif item['type'] == 'rect':
                ycoord -= 3
                width = item['width'] * 4
                height = item['height'] * 4
                if item.get('fill') is None:
                    pdf.rect(xcoord, ycoord, width, height)
                else:
                    pdf.rect(xcoord, ycoord, width, height, style='F', round_corners=True, corner_radius=4)
        return pdf.output()