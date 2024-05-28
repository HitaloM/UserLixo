from dataclasses import dataclass

from hydrogram import Client
from hydrogram.types import Message
from kink import inject

from userlixo.modules.abstract import MessageHandler
from userlixo.modules.common.plugins import handle_add_plugin_request
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class ProcessPythonFileMessageHandler(MessageHandler):
    language_selector: LanguageSelector

    async def handle_message(self, client: Client, message: Message):
        lang = self.language_selector.get_lang()

        await handle_add_plugin_request(lang, client, message)
