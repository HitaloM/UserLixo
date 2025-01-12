import html
import io
import re
import traceback
from collections.abc import Callable
from contextlib import redirect_stdout

from hydrogram import Client
from hydrogram.types import Message


async def execs(  # noqa: PLR0917
    code: str,
    client: Client,
    message: Message,
    on_result: Callable | None = None,
    on_error: Callable | None = None,
    on_huge_result: Callable | None = None,
    on_no_result: Callable | None = None,
):
    reply = message.reply_to_message
    user = (reply or message).from_user
    chat = message.chat

    code_function = """
async def __ex(client, message, reply, user, chat):
    c = client
    m = message"""

    for line in code.split("\n"):
        code_function += f"\n    {line}"
    exec(code_function)

    strio = io.StringIO()
    with redirect_stdout(strio):
        try:
            await locals()["__ex"](client, message, reply, user, chat)
        except BaseException:
            traceback_string = traceback.format_exc()
            return f"<b>{html.escape(traceback_string)}</b>"

    output = strio.getvalue()
    if not output:
        return await on_no_result()

    if len(output) <= 4096:
        output = re.sub(f'([{re.escape("```")}])', r"\\\1", output)

        text = "```bash\n" + output + "\n```"
        return await on_result(text)

    strio = io.BytesIO()
    strio.name = "output.txt"
    strio.write(output.encode())
    await on_huge_result(strio)
    return None
