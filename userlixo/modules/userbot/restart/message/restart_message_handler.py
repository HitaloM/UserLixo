from dataclasses import dataclass

from hydrogram import Client
from hydrogram.types import Message
from kink import inject

from userlixo.modules.abstract import MessageHandler
from userlixo.modules.common.restart import (
    compose_before_restart_message,
    save_before_restart_message_info,
    self_restart_process,
)
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class RestartMessageHandler(MessageHandler):
    language_selector: LanguageSelector

    async def handle_message(self, _client: Client, message: Message):
        lang = self.language_selector.get_lang()

        text = compose_before_restart_message(lang)
        msg = await message.reply(text)

        save_before_restart_message_info(msg.id, msg.chat.id, "user")

        self_restart_process()
