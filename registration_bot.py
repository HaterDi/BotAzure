from botbuilder.core import TurnContext, ActivityHandler
from botbuilder.dialogs import Dialog

class RegistrationBot(ActivityHandler):
    def __init__(self, dialog: Dialog):
        super().__init__()
        self.dialog = dialog

    async def on_message_activity(self, turn_context: TurnContext):
        await self.dialog.run(turn_context, turn_context.turn_state.get("dialog_state"))

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello! I will help you register. Just follow the questions.")
