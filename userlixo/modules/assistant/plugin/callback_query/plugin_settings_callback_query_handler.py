from dataclasses import dataclass

from hydrogram import Client
from hydrogram.types import CallbackQuery
from kink import inject

from userlixo.config import plugins
from userlixo.modules.abstract import CallbackQueryHandler
from userlixo.modules.assistant.common.plugins import compose_plugin_settings_message
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class PluginSettingsCallbackQueryHandler(CallbackQueryHandler):
    language_selector: LanguageSelector

    async def handle_callback_query(self, client: Client, query: CallbackQuery):
        lang = self.language_selector.get_lang()

        plugin_name = query.matches[0].group("plugin_name")
        plugins_page = int(query.matches[0].group("plugins_page"))
        settings_page = int(query.matches[0].group("settings_page"))

        plugin_info = plugins.get(plugin_name, None)
        if not plugin_info:
            return await query.answer(lang.plugin_not_found(name=plugin_name), show_alert=True)

        if not plugin_info.settings:
            return await query.answer(
                lang.plugin_settings_not_found(plugin_name=plugin_name), show_alert=True
            )

        await client.stop_listening(chat_id=query.message.chat.id)

        text, keyboard = compose_plugin_settings_message(
            lang, plugin_name, plugins_page, settings_page
        )

        await query.edit(text, reply_markup=keyboard)
        return None
