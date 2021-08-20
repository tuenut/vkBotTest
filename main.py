from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api import VkApi

from pprint import pprint


class SashinBot:
    def __init__(self):
        self.vk_api = VkApi(token=self.TOKEN)
        self.vk_api._auth_token()

        self.api = self.vk_api.get_api()

        self.longpoll = VkLongPoll(self.vk_api)

    def main_loop(self):
        while True:
            self.check_events()

    def check_events(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                self.handle_new_message(event)

    def handle_new_message(self, event):
        users = self.vk_api.method(
            "users.get",
            {"user_ids": event.user_id}
        )
        user_id = users[0]["id"]
        messages = self.vk_api.method(
            "messages.getConversations",
            {
                # "peer_ids": [users[0]["id"], ]
                "offset": 0,
                "count": 20,
                "filter": "unanswered"
            }
        )

        pprint(messages)

        try:
            conversation_from_current_user = list(filter(
                lambda item: item["last_message"]["peer_id"] == user_id,
                messages["items"]
            ))[0]
        except IndexError:
            return

        last_msg = conversation_from_current_user["last_message"]

        if last_msg["text"].lower() == "дай клаву":
            self.send_keyboard(users[0]["id"])

    def send_keyboard(self, peer_id):
        keyboard = VkKeyboard(one_time=True)

        keyboard.add_button('Белая кнопка', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()  # Переход на вторую строку
        keyboard.add_location_button()

        self.api.messages.send(
            peer_id=peer_id,
            random_id=get_random_id(),
            keyboard=keyboard.get_keyboard(),
            message='Пример клавиатуры'
        )


def main():
    bot = SashinBot()
    bot.main_loop()


if __name__ == "__main__":
    main()
