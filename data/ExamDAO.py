import uuid

from model.Exam import Exam


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

        '''
        jstring = '['
        for item in self._examdict.values():
            jstring += item.to_json() + ","
        jstring = jstring[:-1] + ']'

'''
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
        exams = Exam.schema().loads(file.read(), many=True)
        for exam in exams:
            key = exam.exam_uuid
            self._examdict[key] = exam


if __name__ == '__main__':
    ''' Check if started directly '''
    dao = ExamDAO()
    dao.load_exams()
