from flask_restful import Resource, fields, reqparse
from flask import make_response

from data.EventDAO import EventDAO
from util.token import token_required


class EventService(Resource):
    """
    services for CRUD of a single event

    author: Marcel Suter
    """
    method_decorators = [token_required]

    def __init__(self):
        """
        constructor

        Parameters:

        """
        pass

    def get(self, user, event_uuid=None, date=None):
        """
        FIXME separate functions for get one / get all
        gets an event identified by the uuid or gets all events for a date
        :param event_uuid: the unique key
        :return: http response
        """
        event_dao = EventDAO()
        http_status = 404
        jstring = ''

        if event_uuid is not None:
            event = event_dao.read_event(event_uuid)
            if event is not None:
                http_status = 200
                jstring = event.to_json()
        else:
            events = event_dao.filtered_list(date)
            jstring = '['
            for event in events:
                http_status = 200
                data = event.to_json() + ","
                jstring += data
            jstring = jstring[:-1] + ']'



        return make_response(
            jstring, http_status
        )
