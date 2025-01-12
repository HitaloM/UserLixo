from dataclasses import dataclass

from hydrogram.types import CallbackQuery
from kink import inject

from userlixo.modules.abstract import CallbackQueryHandler
from userlixo.modules.assistant.common.sudoers import (
    compose_list_sudoers_message,
)
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class SettingSudoersCallbackQueryHandler(CallbackQueryHandler):
    language_selector: LanguageSelector

    async def handle_callback_query(self, _client, query: CallbackQuery):
        lang = self.language_selector.get_lang()

        text, keyboard = await compose_list_sudoers_message(
            lang, _client, from_user_id=query.from_user.id
        )
        await query.edit(text, reply_markup=keyboard)
