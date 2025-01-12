from dataclasses import dataclass

from hydrogram.types import CallbackQuery
from kink import inject

from userlixo.modules.abstract import CallbackQueryHandler
from userlixo.modules.common.settings import compose_settings_message
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class SettingsCallbackQueryHandler(CallbackQueryHandler):
    language_selector: LanguageSelector

    async def handle_callback_query(self, _c, query: CallbackQuery):
        lang = self.language_selector.get_lang()

        text, keyboard = compose_settings_message(lang)

        await query.edit(text, reply_markup=keyboard)
