import uuid

from dacite import from_dict
from model.Exam import Exam
import json


def condition(exam, filter_value):
    """
    condition for filtering the examlist
    :param exam: an exam object to be examined
    :param filter_value: the filter condition
    :return: matches filter True/False
    """
    if (exam.teacher == filter_value or
            exam.student == filter_value or
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
        self._examlist = []
        self.load_exams()

    def filtered_list(self, filter_value):
        """
        returns the filtered list of exams
        :param filter_value: the filter to be applied
        :return: list of exams
        """
        filtered = [exam for exam in self._examlist if condition(exam, filter_value)]
        return filtered

    def read_exam(self, uuid):
        """
        reads an exam by its uuid
        :param uuid: the unique key
        :return: Exam object
        """

        exam = [item for item in self._examlist if item.exam_uuid == uuid]
        return exam

    def save_exam(self, exam):
        self.load_exams()
        if exam.exam_uuid is None:
            exam.exam_uuid = str(uuid.uuid4())
        self._examlist.append(exam)
        jstring = '['
        for item in self._examlist:
            jstring += item.to_json() + ","
        jstring = jstring[:-1] + ']'

        file = open('./files/exams.json', 'w')
        file.write(jstring)
        file.close()

    def load_exams(self):
        """
        loads all exams into _examlist
        :return: none
        :rtype: none
        """
        file = open('./files/exams.json')
        data = json.load(file)
        for item in data:
            exam = from_dict(data_class=Exam, data=item)
            self._examlist.append(exam)


if __name__ == '__main__':
    ''' Check if started directly '''
    dao = ExamDAO()
    dao.load_exams()
