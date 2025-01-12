from dataclasses import dataclass

from hydrogram import Client, filters
from hydrogram.types import Message

from userlixo.decorators import controller, on_message
from userlixo.modules.userbot.plugin.message.list_plugins_message_handler import (
    ListPluginsMessageHandler,
)
from userlixo.modules.userbot.plugin.message.plugin_action_message_handler import (
    PluginActionMessageHandler,
)
from userlixo.modules.userbot.plugin.message.process_python_file_message_handler import (
    ProcessPythonFileMessageHandler,
)


@controller
@dataclass
class PluginMessageController:
    plugin_action_handler: PluginActionMessageHandler
    process_python_file_handler: ProcessPythonFileMessageHandler
    list_plugins_handler: ListPluginsMessageHandler

    @on_message(filters.reply & filters.su_cmd(r"(plugin )?(?P<action>add|rm|\+|-)"))
    async def plugin_action(self, client: Client, message: Message):
        await self.plugin_action_handler.handle_message(client, message)

    @on_message(filters.document & filters.private & ~filters.me)
    async def process_python_file(self, client: Client, message: Message):
        if message.document.file_name.endswith(".zip"):
            await self.process_python_file_handler.handle_message(client, message)

    @on_message(filters.su_cmd(r"plugins$"))
    async def list_plugins(self, client: Client, message: Message):
        await self.list_plugins_handler.handle_message(client, message)
