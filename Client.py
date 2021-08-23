from logging import getLogger
from pprint import pformat

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
from vk_api.utils import get_random_id

logger = getLogger(__name__)


class Client:
    def __init__(self, token):
        self.vk_api = VkApi(token=token)
        self.vk_api._auth_token()

        self.longpoll = VkLongPoll(self.vk_api)

    def listen_events(self):
        return self.longpoll.listen()

    def get_user_chat_history(self, peer_id):
        return self.vk_api.method("messages.getHistory", {"user_id": peer_id})

    def get_user_last_message(self, peer_id):
        history = self.get_user_chat_history(peer_id)

        user_messages = list(filter(
            lambda msg: not msg["out"],
            history["items"]
        ))

        logger.debug(pformat(user_messages[0]))

        return user_messages[0]

    def send_message(self, peer_id, message_object: dict):
        message_object = {
            "peer_id": peer_id,
            "random_id": get_random_id(),
            **message_object
        }

        return self.vk_api.method("messages.send", message_object)

    def upload_image(self, file):
        """
        нужно потыкать в `photos.getMessagesUploadServer`
        так получим url, куда надо отправит POST-запрос с файлом

        отпрвать POST-запрос примерно так
        `requests.post(upload_url, files={"photo": pic_file})`

        сохранить фото тыкнув сюда `photos.saveMessagesPhoto`
        """
    raise NotImplemented
