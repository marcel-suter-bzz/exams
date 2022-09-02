from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config, Exclude


@dataclass_json
@dataclass
class Person(dict):
    """
    a student, teacher or supervisor
    
    author: Marcel Suter
    """

    email: str
    firstname: str
    lastname: str

        
    @property
    def firstname(self):
        return self._firstname
    
    @firstname.setter
    def firstname(self, value):
        self._firstname = value
        
    @property
    def lastname(self):
        return self._lastname
    
    @lastname.setter
    def lastname(self, value):
        self._lastname = value
        
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self._email = value