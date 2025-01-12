from dataclasses import dataclass

from hydrogram import filters

from userlixo.decorators import controller, on_callback_query

from .help_callback_query_handler import HelpCallbackQueryHandler


@controller
@dataclass
class HelpCallbackQueryController:
    handler: HelpCallbackQueryHandler

    @on_callback_query(filters.regex("^help"))
    async def help(self, c, callback_query):
        await self.handler.handle_callback_query(c, callback_query)
