from dataclasses import dataclass

from hydrogram import Client
from hydrogram.types import CallbackQuery
from kink import inject

from userlixo.modules.abstract import CallbackQueryHandler
from userlixo.modules.common.start import compose_start_message
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class StartCallbackQueryHandler(CallbackQueryHandler):
    language_selector: LanguageSelector

    async def handle_callback_query(self, _c: Client, cq: CallbackQuery):
        lang = self.language_selector.get_lang()

        text, keyboard = compose_start_message(lang)
        await cq.edit_message_text(text, reply_markup=keyboard)
