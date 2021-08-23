from logging import getLogger
from Bot import Bot
from utils.logger import configure_logger

from settings import NAME

try:
    from secret import TOKEN
except ImportError:
    raise ImportError(
        "Не удалось найти токен.\nСоздайте файл `secret.py` и в нем в строковую"
        " переменную `TOKEN` положите ваш токен. "
    )


def main():
    logger = getLogger(__name__)

    logger.info("Starting %s..." % NAME)

    logger.info("Initializing Bot...")
    bot = Bot(TOKEN)
    logger.info("Bot was initialized.")

    logger.info("Bot starts work.")
    bot.main_loop()


if __name__ == "__main__":
    configure_logger()
    main()
