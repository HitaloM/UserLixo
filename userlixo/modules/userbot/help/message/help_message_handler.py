from dataclasses import dataclass

from hydrogram import Client
from hydrogram.types import Message
from kink import inject

from userlixo.modules.abstract import MessageHandler
from userlixo.modules.common.help import compose_help_message
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class HelpMessageHandler(MessageHandler):
    language_selector: LanguageSelector

    async def handle_message(self, _client: Client, message: Message):
        lang = self.language_selector.get_lang()

        text, keyboard = compose_help_message(lang)
        await message.reply(text, reply_markup=keyboard, quote=True)
