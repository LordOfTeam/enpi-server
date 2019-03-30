from flask_restful import reqparse


class ApplyTicketFormParser(object):
    def __init__(self):
        self.post_ticket_form = reqparse.RequestParser()
        self.post_ticket_form.add_argument('apply_json', type=dict, required=True)
