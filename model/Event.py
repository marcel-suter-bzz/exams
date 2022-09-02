from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Event:
    """
    short description

    author: Marcel Suter
    """

    event_uuid: str
    datetime: str


if __name__ == '__main__':
    ''' Check if started directly '''
    pass