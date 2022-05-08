from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters

from fomo_bot.config import BotConfig


class FomoBot:
    def __init__(self, config: BotConfig):
        self.token = config.token

        self.updater = Updater(
            token=self.token,
            use_context=True,
        )
        dispatcher = self.updater.dispatcher

        message_handler = MessageHandler(Filters.text, self.handle_message)
        dispatcher.add_handler(message_handler)

    def run(self):
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()

    def handle_message(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        text = update.message.text
        context.bot.sendMessage(chat_id=chat_id, text=text)
