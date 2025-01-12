import re
from dataclasses import dataclass

from hydrogram import Client, filters

from userlixo.decorators import controller, on_message

from .cmd_message_handler import CmdMessageHandler
from .eval_message_handler import EvalMessageHandler
from .exec_message_handler import ExecMessageHandler


@controller
@dataclass
class ExecsMessageController:
    cmd_handler: CmdMessageHandler
    eval_handler: EvalMessageHandler
    exec_handler: ExecMessageHandler

    @on_message(filters.regex(r"^/(?P<command>cmd|sh)\s+(?P<code>.+)", flags=re.DOTALL))
    async def cmd_sh(self, client: Client, message):
        await self.cmd_handler.handle_message(client, message)

    @on_message(filters.regex(r"^/(?P<cmd>ex(ec)?)\s+(?P<code>.+)", flags=re.DOTALL))
    async def execs(self, client: Client, message):
        await self.exec_handler.handle_message(client, message)

    @on_message(filters.regex(r"^/(?P<cmd>ev(al)?)\s+(?P<code>.+)", flags=re.DOTALL))
    async def evals(self, client: Client, message):
        await self.eval_handler.handle_message(client, message)
