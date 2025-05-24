from botbuilder.core import ActivityHandler, TurnContext, ConversationState, MemoryStorage
from botbuilder.dialogs import DialogSet
from bot.dialogs.registration_dialog import RegistrationDialog

class RegistrationBot(ActivityHandler):
    def __init__(self):
        self.dialog = RegistrationDialog()
        self.conversation_state = ConversationState(MemoryStorage())
        self.dialogs = DialogSet(self.conversation_state.create_property("DialogState"))
        self.dialogs.add(self.dialog)

    async def on_message_activity(self, turn_context: TurnContext):
        dialog_context = await self.dialogs.create_context(turn_context)
        results = await dialog_context.continue_dialog()
        if results.status.value == "Empty":
            await dialog_context.begin_dialog("registrationDialog")
        await self.conversation_state.save_changes(turn_context)