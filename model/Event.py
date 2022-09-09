import json
from dataclasses import dataclass

import datetime as datetime


@dataclass
class Event:
    """
    an event for exam repetitions

    author: Marcel Suter
    """

    event_uuid: str
    datetime: datetime.datetime
    rooms: list
    supervisors: list

    def to_json(self):
        jstring = '{"event_uuid":"' + self.event_uuid + '",' + \
                  '"datetime": "' + self.datetime.strftime('%Y-%m-%d %H:%M:%S') + ',' + \
                  '"supervisors":' + json.dumps(self.supervisors) + ',' + \
                  '"rooms":' + json.dumps(self.rooms) + '}'
        return jstring


if __name__ == '__main__':
    ''' Check if started directly '''
    pass
