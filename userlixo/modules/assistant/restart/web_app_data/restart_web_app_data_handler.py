from dataclasses import dataclass

from hydrogram.types import Message
from kink import inject

from userlixo.modules.abstract.web_app_data_handler import WebAppDataHandler
from userlixo.modules.common.restart import (
    compose_before_restart_message,
    save_before_restart_message_info,
    self_restart_process,
)
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class RestartWebAppDataHandler(WebAppDataHandler):
    language_selector: LanguageSelector

    async def handle_web_app_data(self, _c, m: Message):
        lang = self.language_selector.get_lang()

        text = compose_before_restart_message(lang)
        msg = await m.reply(text)

        save_before_restart_message_info(msg.id, msg.chat.id, "bot")

        self_restart_process()
