from typing import Tuple
from logging import getLogger
from pprint import pformat

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkEventType


logger = getLogger(__name__)


class MessageHandler:
    REACTIONS = {
        "начать": "get_basic_keys",
        "сначала": "get_basic_keys",
        "давай сначала": "get_basic_keys",
        "покажи клавиатуру": "get_basic_keys",
        "покажи картинку": "get_random_image"
    }

    ERRORS = {
        "NotInteresting": "Not interesting event.",
    }

    MESSAGES = {
        "UnknownUserCommand": "Я вас не понял. Напишите что-нибудь внятное."
    }

    def __init__(self, client):
        self.client = client

    def handle_event(self, event) -> dict or None:
        result = None

        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handled, result = self.handle_new_message(event)

            if handled:
                logger.debug(
                    "Event was handled with answer: %s",
                    pformat(result)
                )
                return result

        error = result or self.ERRORS["NotInteresting"]

        logger.debug("Event was not handled due: %s", error)

        return None

    def handle_new_message(self, event) -> Tuple[bool, dict]:
        last_message = self.client.get_user_last_message(event.user_id)
        last_message_text = last_message["text"].lower()

        try:
            reaction_method_name = self.REACTIONS[last_message_text]
        except KeyError:
            return True, {"message": self.MESSAGES["UnknownUserCommand"]}
        else:
            reaction_method = getattr(self, reaction_method_name)
            answer = reaction_method()

            return True, answer

    def get_basic_keys(self, ) -> dict:
        keyboard = VkKeyboard(one_time=True)

        keyboard.add_button('Покажи картинку', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Как пользоваться?', color=VkKeyboardColor.POSITIVE)

        return {
            "keyboard": keyboard.get_keyboard(),
            "message": 'Что ж, давай начнем!'
        }

    def get_random_image(self):
        """
        нужно открыть файл с картинкой на чтение `open(file_path, "rb")`

        и вызвать `self.client.upload_image`

        вернуть cловарь
        {"attachments": "photo%s_%s" % (owner_id, media_id)}
        """
        raise NotImplemented
