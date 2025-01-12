import math
from dataclasses import dataclass
from pathlib import Path

from hydrogram.helpers import ikb
from hydrogram.types import CallbackQuery
from kink import inject

from userlixo.config import plugins
from userlixo.modules.abstract import CallbackQueryHandler
from userlixo.utils.plugins import (
    get_plugin_info_from_folder,
    load_plugin,
    unload_and_remove_plugin,
    unzip_plugin_to_folder,
)
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class ConfirmAddPluginCallbackQueryHandler(CallbackQueryHandler):
    language_selector: LanguageSelector

    async def handle_callback_query(self, _client, query: CallbackQuery):
        lang = self.language_selector.get_lang()

        cache_filename = query.matches[0]["filename"]
        basename = Path(cache_filename).stem

        loading_keyboard = ikb([[("🕔", "dumb_button")]])

        await query.edit(
            lang.starting_plugin_installation(name=basename), reply_markup=loading_keyboard
        )

        try:
            unzip_plugin_to_folder(cache_filename, basename)
        except Exception as e:
            await query.edit(lang.plugin_could_not_unzip(e=str(e)))
            return

        await query.edit(
            lang.starting_plugin_elements_loading(name=basename), reply_markup=loading_keyboard
        )

        try:
            load_plugin(basename)
        except Exception as e:
            await query.edit(lang.plugin_could_not_load(e=str(e)))
            unload_and_remove_plugin(basename)
            return

        await query.edit(
            lang.starting_plugin_info_saving(name=basename), reply_markup=loading_keyboard
        )

        plugin_info = get_plugin_info_from_folder(basename)

        plugins[basename] = plugin_info

        # Discover which page is this plugin listed in
        quant_per_page = 4 * 2  # lines times columns
        page = math.ceil(len(plugins) / quant_per_page)

        keyboard = ikb([[(lang.see_plugin_info, f"info_plugin {basename} {page}")]])
        text = lang.plugin_added(name=basename)

        await query.edit(text, keyboard)
        return
