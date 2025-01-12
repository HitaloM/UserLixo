import json
import os
from dataclasses import dataclass

from hydrogram.types import Message, ReplyKeyboardRemove
from kink import inject

from userlixo.config import sudoers, user
from userlixo.database import Config
from userlixo.modules.abstract.web_app_data_handler import WebAppDataHandler
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class SaveSettingsWebAppDataHandler(WebAppDataHandler):
    language_selector: LanguageSelector

    @staticmethod
    async def handle_web_app_data(_c, m: Message):
        def update_config(key, value):
            for obj in Config.select(Config.key == key):
                obj.value = value
                obj.save()
            os.environ[key] = value

        settings = json.loads(m.web_app_data.data.split("--", 1)[1])

        if "web_app_url" in settings:
            await update_config("WEB_APP_URL", settings["web_app_url"])
        if "logs_chat" in settings:
            await update_config("LOGS_CHAT", settings["logs_chat"])
        if "prefixes" in settings:
            await update_config("PREFIXES", settings["prefixes"])
        if "sudoers" in settings:
            await update_config("SUDOERS_LIST", settings["sudoers"])
            sudoers.clear()
            sudoers.append(user.me.id)
            sudoers.extend(settings["sudoers"].split(" "))
        if "language" in settings:
            await update_config("LANGUAGE", settings["language"])

        await m.reply(
            "The followings settings were set:\n" + json.dumps(settings, indent=2),
            reply_markup=ReplyKeyboardRemove(),
        )
