from dataclasses import dataclass

from hydrogram.helpers import array_chunk, ikb
from hydrogram.types import CallbackQuery
from kink import inject

from userlixo.modules.abstract import CallbackQueryHandler
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class SettingLanguageCallbackQueryHandler(CallbackQueryHandler):
    language_selector: LanguageSelector

    async def handle_callback_query(self, _client, query: CallbackQuery):
        lang = self.language_selector.get_lang()

        buttons = []
        for obj in lang.strings.values():
            text, data = (
                (f"✅ {obj["NAME"]}", "noop")
                if obj["LANGUAGE_CODE"] == lang.code
                else (obj["NAME"], f"set_language {obj["LANGUAGE_CODE"]}")
            )
            buttons.append((text, data))

        lines = array_chunk(buttons, 2)
        lines.append([(lang.back, "settings")])

        keyboard = ikb(lines)
        await query.edit(lang.choose_language, reply_markup=keyboard)
