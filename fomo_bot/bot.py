import logging
import os

from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters

from fomo_bot.config import BotConfig


class FomoBot:
    TOKEN_ENV = "FOMO_BOT_TOKEN"

    def __init__(self, config: BotConfig):
        self.token = FomoBot.resolve_token(config.token)
        self.forward_channel_id = config.forward_channel_id
        self.allowed_source_ids = config.allowed_source_ids
        self.admin_users = config.admin_users

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
        username = update.effective_user.username
        if str(chat_id) not in self.allowed_source_ids and username not in self.admin_users:
            logging.warning(f"Illegal chat id {chat_id}")
            return

        if update.message:
            text = update.message.text
        elif update.channel_post:
            text = update.channel_post.text
        else:
            logging.warning(f"Cannot get text for update {update}")
            return

        if text == "/admin" and username in self.admin_users:
            context.bot.send_message(chat_id=chat_id, text=f"Chat id: {chat_id}")
        elif "#fomo" in text.lower():
            message_id = update.message.message_id
            link = update.message.link
            reply = update.message.reply_to_message
            if reply:
                message_id = reply.message_id
                link = reply.link
            if link:
                context.bot.send_message(
                    chat_id=self.forward_channel_id,
                    text=f"Link to message {link}"
                )
            context.bot.forward_message(
                chat_id=self.forward_channel_id,
                from_chat_id=chat_id,
                message_id=message_id,
            )

    @staticmethod
    def resolve_token(config_value: str) -> str:
        env_token = os.environ.get(FomoBot.TOKEN_ENV)
        if env_token:
            return env_token
        else:
            return config_value
