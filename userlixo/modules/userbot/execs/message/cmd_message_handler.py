from dataclasses import dataclass
from typing import BinaryIO

from hydrogram import Client
from hydrogram.types import Message
from kink import inject

from userlixo.modules.abstract import MessageHandler
from userlixo.modules.common.cmd import cmd
from userlixo.utils.services.language_selector import LanguageSelector


@inject
@dataclass
class CmdMessageHandler(MessageHandler):
    language_selector: LanguageSelector

    async def handle_message(self, _client: Client, message: Message):
        lang = self.language_selector.get_lang()

        code = message.matches[0].group("code")

        async def on_result(text: str):
            await message.reply(text, quote=True)

        async def on_huge_result(io: BinaryIO):
            await message.reply_document(io, quote=True)

        async def on_no_result():
            await message.reply(lang.executed_cmd, quote=True)

        await cmd(code, on_result, on_huge_result, on_no_result)
