import json
import os
import urllib
from dataclasses import dataclass

import psutil
from hydrogram.helpers import kb
from hydrogram.types import Message, WebAppInfo
from kink import inject

from userlixo.config import cmds, plugins, user
from userlixo.modules.abstract import MessageHandler
from userlixo.utils import shell_exec
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class WebAppMessageHandler(MessageHandler):
    language_selector: LanguageSelector

    @staticmethod
    async def handle_message(_c, m: Message):
        local_version = int((await shell_exec("git rev-list --count HEAD"))[0])
        p = psutil.Process(os.getpid())
        start_time = p.create_time()

        info = await user.get_me()

        info_json = json.dumps({
            "version": local_version,
            "start_time": start_time,
            "name": info.full_name,
            "id": info.id,
            "picture": f"https://t.me/i/userpic/160/{info.username}.jpg",
        })
        settings_json = json.dumps({
            "language": os.getenv("LANGUAGE"),
            "sudoers": os.getenv("SUDOERS_LIST"),
            "logs_chat": os.getenv("LOGS_CHAT"),
            "prefixes": os.getenv("PREFIXES"),
            "web_app_url": os.getenv("WEB_APP_URL"),
        })

        cmds_json = json.dumps([k for k, v in cmds.items()])
        plugins_json = json.dumps(plugins)

        params = {
            "settings": settings_json,
            "info": info_json,
            "commands": cmds_json,
            "plugins": plugins_json,
        }
        query = urllib.parse.urlencode(params)

        web_app_url = os.getenv("WEB_APP_URL")
        web_app_info = WebAppInfo(url=f"{web_app_url}?{query}")

        keyboard = kb(
            [
                [
                    {
                        "text": "Settings",
                        "web_app": web_app_info,
                    }
                ]
            ],
            resize_keyboard=True,
            placeholder="Update your setting below...",
        )
        await m.reply("Here is your webapp for settings...", reply_markup=keyboard)
