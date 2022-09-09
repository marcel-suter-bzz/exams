from dataclasses import dataclass
from model.Person import Person


@dataclass
class Exam(dict):
    """
    a exam to be taken
    
    author: Marcel Suter
    """

    exam_uuid: str
    teacher: Person
    student: Person
    cohort: str
    module: str
    exam_num: str
    duration: int
    remarks: str
    tools: str
    event_uuid: str
    status: str

    def to_json(self):
        jstring = '{"exam_uuid":"' + self.exam_uuid + '",' + \
                  '"cohort": "' + self.cohort + '", ' + \
                  '"module": "' + self.module + '", ' + \
                  '"exam_num": "' + self.exam_num + '", ' + \
                  '"duration": ' + str(self.duration) + ', ' + \
                  '"remarks": "' + self.remarks + '", ' + \
                  '"tools": "' + self.tools + '", ' + \
                  '"event_uuid": "' + self.event_uuid + '", ' + \
                  '"status": "' + self.status + '", ' + \
                  '"teacher": ' + self.teacher.to_json() + ',' + \
                  '"student": ' + self.student.to_json() + '}'
        return jstring

    @property
    def exam_uuid(self):
        return self._exam_uuid

    @exam_uuid.setter
    def exam_uuid(self, value):
        self._exam_uuid = value

    @property
    def teacher(self):
        return self._teacher

    @teacher.setter
    def teacher(self, value):
        self._teacher = value

    @property
    def student(self):
        return self._student

    @student.setter
    def student(self, value):
        self._student = value

    @property
    def cohort(self):
        return self._cohort

    @cohort.setter
    def cohort(self, value):
        self._cohort = value

    @property
    def module(self):
        return self._module

    @module.setter
    def module(self, value):
        self._module = value

    @property
    def exam_num(self):
        return self._exam_num

    @exam_num.setter
    def exam_num(self, value):
        self._exam_num = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def remarks(self):
        return self._remarks

    @remarks.setter
    def remarks(self, value):
        self._remarks = value

    @property
    def tools(self):
        return self._tools

    @tools.setter
    def tools(self, value):
        self._tools = value

    @property
    def event_uuid(self):
        return self._event_uuid

    @event_uuid.setter
    def event_uuid(self, value):
        self._event_uuid = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value


if __name__ == '__main__':
    ''' Check if started directly '''
    pass
