from dataclasses import dataclass

from hydrogram.types import CallbackQuery
from kink import inject

from userlixo.modules.abstract import CallbackQueryHandler
from userlixo.modules.common.help import compose_help_message
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class HelpCallbackQueryHandler(CallbackQueryHandler):
    language_selector: LanguageSelector

    async def handle_callback_query(self, _c, query: CallbackQuery):
        lang = self.language_selector.get_lang()

        text, keyboard = compose_help_message(lang, append_back=True)
        await query.edit(text, reply_markup=keyboard)
