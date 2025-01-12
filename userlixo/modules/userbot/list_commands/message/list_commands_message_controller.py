from dataclasses import dataclass

from hydrogram import Client, filters
from hydrogram.types import Message

from userlixo.decorators import controller, on_message
from userlixo.modules.userbot.list_commands.message.list_commands_message_handler import (
    ListCommandsMessageHandler,
)


@controller
@dataclass
class ListCommandsMessageController:
    handler: ListCommandsMessageHandler

    @on_message(filters.su_cmd("(commands|cmds)"))
    async def list_commands(self, client: Client, message: Message):
        await self.handler.handle_message(client, message)
