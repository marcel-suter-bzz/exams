import json
import uuid

from data.PersonDAO import PersonDAO
from model.Exam import Exam


def condition(exam, student, teacher, date, status):
    """
    condition for filtering the examlist
    :param exam: an exam object to be examined
    :param student
    :param teacher
    :param date
    :param status
    :return: matches filter True/False
    """
    match = True
    if student is not None and student != "":
        student = student.lower()
        if student not in exam.student.firstname.lower() and student not in exam.student.lastname.lower():
            match = False
    if teacher is not None and teacher != "":
        teacher = teacher.lower()
        if teacher not in exam.teacher.firstname.lower() and teacher not in exam.teacher.lastname.lower():
            match = False
    if date is not None and date != "":
        if date != exam.event_uuid:
            match = False
    if status is None or status == "":
        status = "all"
    if status == "open" and exam.status not in ['pendent', 'offen', 'abgegeben', 'erhalten']:
        match = False
    if status == "closed" and exam.status not in ['erledigt', 'pnab', 'gelöscht']:
        match = False
    return match


class ExamDAO:
    """
    data access object for exams

    author: Marcel Suter
    """

    def __init__(self, examlist=''):
        """
        constructor

        Parameters:

        """
        self._examdict = {}
        self.load_exams()

    def filtered_list(self, student, teacher, date, status):
        """
        returns the filtered list of exams
        :param student
        :param teacher
        :param date
        :param status
        :return: list of exams
        """

        filtered = []
        for (key, exam) in self._examdict.items():
            if condition(exam, student, teacher, date, status):
                filtered.append(exam)
                if len(filtered) >= 20:
                    break
        return filtered

    def read_exam(self, uuid):
        """
        reads an exam by its uuid
        :param uuid: the unique key
        :return: Exam object
        """

        if uuid in self._examdict:
            return self._examdict[uuid]
        return None

    def save_exam(self, exam):
        """
        saves a new or changed exam
        :param exam:
        :return:
        """
        self._examdict[exam.exam_uuid] = exam
        exams_json = '['
        for key in self._examdict:
            data = self._examdict[key].to_json(False)
            exams_json += data + ','
        exams_json = exams_json[:-1] + ']'

        file = open('./files/exams.json', 'w')
        file.write(exams_json)
        file.close()

    def load_exams(self):
        """
        loads all exams into _examlist
        :return: none
        :rtype: none
        """
        person_dao = PersonDAO()
        file = open('./files/exams.json')
        exams = json.load(file)
        for item in exams:
            key = item['exam_uuid']
            teacher = person_dao.read_person(item['teacher'])
            student = person_dao.read_person(item['student'])
            exam = Exam(
                item['exam_uuid'],
                teacher,
                student,
                item['cohort'],
                item['module'],
                item['exam_num'],
                item['duration'],
                item['remarks'],
                item['tools'],
                item['event_uuid'],
                item['status']
            )
            self._examdict[key] = exam

if __name__ == '__main__':
    ''' Check if started directly '''
    dao = ExamDAO()
    dao.load_exams()
