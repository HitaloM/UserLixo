from dataclasses import dataclass

from hydrogram import Client, filters

from userlixo.decorators import controller, on_callback_query

from .upgrade_callback_query_handler import UpgradeCallbackQueryHandler


@controller
@dataclass
class UpgradeCallbackQueryController:
    handler: UpgradeCallbackQueryHandler

    @on_callback_query(filters.regex("^upgrade"))
    async def upgrade(self, client: Client, query):
        await self.handler.handle_callback_query(client, query)
