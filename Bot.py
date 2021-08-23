from logging import getLogger
from pprint import pformat

from Client import Client
from Handler import MessageHandler

logger = getLogger(__name__)


class Bot:
    def __init__(self, token):
        self.client = Client(token)
        self.handler = MessageHandler(client=self.client)

    def main_loop(self):
        logger.debug("Start listening events.")

        for event in self.client.listen_events():
            logger.debug("Event: \n%s" % pformat(event.__dict__))

            answer = self.handler.handle_event(event)

            if answer:
                self.client.send_message(event.user_id, answer)
