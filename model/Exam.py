from dataclasses import dataclass, field


@dataclass
class Exam(dict):
    """
    short description
    
    author: Marcel Suter
    """

    exam_uuid: str
    _exam_uuid: str = field(init=False, repr=False)
    teacher: str
    _teacher: str = field(init=False, repr=False)
    student: str
    _student: str = field(init=False, repr=False)
    cohort: str
    _cohort: str = field(init=False, repr=False)
    email: str
    _email: str = field(init=False, repr=False)
    module: str
    _module: str = field(init=False, repr=False)
    exam_num: str
    _exam_num: str = field(init=False, repr=False)
    duration: int
    _duration: int = field(init=False, repr=False)
    remarks: str
    _remarks: str = field(init=False, repr=False)
    tools: str
    _tools: str = field(init=False, repr=False)
    datetime: str
    _datetime: str = field(init=False, repr=False)
    status: str
    _status: str = field(init=False, repr=False)

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
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self._email = value
    
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
    def datetime(self):
        return self._datetime

    @datetime.setter
    def datetime(self, value):
        self._datetime = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value


if __name__ == '__main__':
    ''' Check if started directly '''
    pass
