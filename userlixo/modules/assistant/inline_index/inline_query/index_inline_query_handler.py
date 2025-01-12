import json

from hydrogram.helpers import ikb
from hydrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from kink import inject

from userlixo.database import Message
from userlixo.modules.abstract import InlineQueryHandler


@inject
class IndexInlineQueryHandler(InlineQueryHandler):
    @staticmethod
    async def handle_inline_query(_c, iq: InlineQuery):
        index = int(iq.matches[0]["index"])
        message = Message.get_or_none(Message.key == index)
        if not message:
            results = [
                InlineQueryResultArticle(
                    title="undefined index",
                    input_message_content=InputTextMessageContent(f"Undefined index {index}"),
                )
            ]
            return await iq.answer(results, cache_time=0)

        reply_markup = json.loads(message.keyboard)
        keyboard = ikb(reply_markup)
        text = message.text

        results = [
            InlineQueryResultArticle(
                title="index",
                input_message_content=InputTextMessageContent(text, disable_web_page_preview=True),
                reply_markup=keyboard,
            )
        ]

        await iq.answer(results, cache_time=0)
        Message.get(Message.key == message.key).delete_instance()
        return None
