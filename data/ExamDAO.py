import json
import uuid

from data.PersonDAO import PersonDAO
from model.Exam import Exam


def condition(exam, filter_value):
    """
    condition for filtering the examlist
    :param exam: an exam object to be examined
    :param filter_value: the filter condition
    :return: matches filter True/False
    """
    return True # FIXME
    filter_value = filter_value.lower()
    if (filter_value in exam.teacher.email.lower() or
            filter_value in exam.student.email.lower() or
            exam.datetime == filter_value):
        return True
    return False


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

    def filtered_list(self, filter_value):
        """
        returns the filtered list of exams
        :param filter_value: the filter to be applied
        :return: list of exams
        """

        filtered = []
        for (key, exam) in self._examdict.items():
            if condition(exam, filter_value):
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
        self.load_exams()
        if exam.exam_uuid is None:
            exam.exam_uuid = str(uuid.uuid4())
        self._examdict[exam.exam_uuid] = exam
        jstring = Exam.schema().dumps(list(self._examdict.values()), many=True)

        file = open('./files/exams.json', 'w')
        file.write(jstring)
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
                item['datetime'],
                item['status']
            )
            self._examdict[key] = exam


if __name__ == '__main__':
    ''' Check if started directly '''
    dao = ExamDAO()
    dao.load_exams()
