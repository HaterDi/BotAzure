from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext, MemoryStorage, ConversationState
from botbuilder.schema import Activity, ActivityTypes
from aiohttp import web
import asyncio
import os
from registration_dialog import RegistrationDialog
from botbuilder.dialogs import DialogSet
from config import APP_ID, APP_PASSWORD

# Настройки адаптера
adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

# Хранилище и состояние
memory = MemoryStorage()
conversation_state = ConversationState(memory)
dialog_state = conversation_state.create_property("dialog_state")
dialogs = DialogSet(dialog_state)

# Добавляем наш диалог
dialogs.add(RegistrationDialog())

# Обработка входящего запроса
async def messages(req: web.Request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    async def turn_call(turn_context: TurnContext):
        dialog_context = await dialogs.create_context(turn_context)

        if dialog_context.active_dialog is None:
            await dialog_context.begin_dialog("registrationDialog")
        else:
            await dialog_context.continue_dialog()

        await conversation_state.save_changes(turn_context)

    await adapter.process_activity(activity, auth_header, turn_call)
    return web.Response(status=200)

# Запуск веб-сервера
app = web.Application()
app.router.add_post("/api/messages", bot_adapter.process_activity)

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 3978))
        web.run_app(app, port=port)
    except Exception as e:
        raise e
