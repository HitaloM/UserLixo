from dataclasses import dataclass

from hydrogram import Client
from hydrogram.types import CallbackQuery
from kink import inject

from userlixo.config import plugins
from userlixo.modules.abstract import CallbackQueryHandler
from userlixo.modules.assistant.common.plugins import (
    ask_and_handle_plugin_settings,
)
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class PluginSettingOpenCallbackQueryHandler(CallbackQueryHandler):
    language_selector: LanguageSelector

    async def handle_callback_query(self, client: Client, query: CallbackQuery):
        lang = self.language_selector.get_lang()

        plugin_name = query.matches[0].group("plugin_name")
        plugins_page = int(query.matches[0].group("plugins_page"))
        settings_page = int(query.matches[0].group("settings_page"))
        options_page = int(query.matches[0].group("options_page"))
        key = query.matches[0].group("key")

        plugin_info = plugins.get(plugin_name, None)
        if not plugin_info:
            return await query.answer(lang.plugin_not_found(name=plugin_name), show_alert=True)

        if not plugin_info.settings:
            return await query.answer(
                lang.plugin_settings_not_found(plugin_name=plugin_name), show_alert=True
            )

        if key not in plugin_info.settings:
            return await query.answer(
                lang.plugin_setting_not_found(plugin_name=plugin_name, key=key), show_alert=True
            )

        setting = plugin_info.settings[key]

        await ask_and_handle_plugin_settings(
            client,
            query,
            lang,
            setting,
            plugin_name,
            key,
            settings_page,
            options_page,
            plugins_page,
        )
        return None
