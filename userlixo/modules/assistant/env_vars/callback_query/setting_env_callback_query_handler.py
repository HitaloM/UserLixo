from dataclasses import dataclass

from hydrogram.helpers import array_chunk, ikb
from hydrogram.types import CallbackQuery
from kink import inject

from userlixo.config import bot
from userlixo.database import Config
from userlixo.modules.abstract import CallbackQueryHandler
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class SettingEnvCallbackQueryHandler(CallbackQueryHandler):
    language_selector: LanguageSelector

    async def handle_callback_query(self, _client, query: CallbackQuery):
        lang = self.language_selector.get_lang()

        if query.message:
            await query.message.chat.stop_listening()
        buttons = []
        for row in Config.select():
            btn = (f"👁‍🗨 {row.key}", f"view_env {row.key}")
            if query.message and query.message.from_user.id == bot.me.id:
                btn = (f"📝 {row.key}", f"edit_env {row.key}")
            buttons.append(btn)
        lines = array_chunk(buttons, 2)
        lines.append([(lang.back, "settings")])
        keyboard = ikb(lines)
        await query.edit(lang.settings_env_text, keyboard)
