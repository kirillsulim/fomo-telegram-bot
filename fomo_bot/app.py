import logging
import signal
from pathlib import Path

import datetime

from fomo_bot.bot import FomoBot
from fomo_bot.config import load_config


class FomoBotApp:
    CONFIG_FILE = "config.yaml"

    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s\t%(threadName)s\t%(name)s\t%(levelname)s\t%(message)s",
        )
        # Monkey patching
        logging.Formatter.formatTime = FomoBotApp.format_time
        config = load_config(Path() / self.CONFIG_FILE)
        self.bot = FomoBot(config.bot)

        signal.signal(signal.SIGINT, self.exit)

    def main(self) -> int:
        self.bot.run()
        return 0

    def exit(self, sig, frame):
        self.bot.stop()

    @staticmethod
    def format_time(self, record, datefmt):
        return datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc).isoformat()
