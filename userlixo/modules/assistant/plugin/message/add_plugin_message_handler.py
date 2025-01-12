from dataclasses import dataclass

from hydrogram.types import Message
from kink import inject

from userlixo.modules.abstract import MessageHandler
from userlixo.modules.common.plugins import handle_add_plugin_request
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class AddPluginMessageHandler(MessageHandler):
    language_selector: LanguageSelector

    async def handle_message(self, _client, message: Message):
        lang = self.language_selector.get_lang()

        await handle_add_plugin_request(lang, _client, update=message)
