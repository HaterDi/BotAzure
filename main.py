from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
from bot.bots.registration_bot import RegistrationBot
import asyncio

app = Flask(__name__)
adapter_settings = BotFrameworkAdapterSettings("", "")
adapter = BotFrameworkAdapter(adapter_settings)
bot = RegistrationBot()

loop = asyncio.get_event_loop()

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")

    async def call_bot():
        await adapter.process_activity(activity, auth_header, bot.on_turn)

    try:
        loop.run_until_complete(call_bot())
        return Response(status=200)
    except Exception as e:
        print(f"Exception: {e}")
        return Response(status=500)

if __name__ == "__main__":
    app.run(debug=True)