from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, TextPrompt, DialogTurnResult

class RegistrationDialog(ComponentDialog):
    def __init__(self, dialog_id: str = "registrationDialog"):
        super(RegistrationDialog, self).__init__(dialog_id)

        self.add_dialog(TextPrompt("TextPrompt"))
        self.add_dialog(WaterfallDialog("WFDialog", [
            self.ask_name,
            self.ask_surname,
            self.ask_email,
            self.ask_phone,
            self.ask_city,
            self.summary
        ]))

        self.initial_dialog_id = "WFDialog"

    async def ask_name(self, step: WaterfallStepContext) -> DialogTurnResult:
        return await step.prompt("TextPrompt", "Hi! What's your first name?")

    async def ask_surname(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["first_name"] = step.result
        return await step.prompt("TextPrompt", "Great, now your last name?")

    async def ask_email(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["last_name"] = step.result
        return await step.prompt("TextPrompt", "What's your email?")

    async def ask_phone(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["email"] = step.result
        return await step.prompt("TextPrompt", "Your phone number?")

    async def ask_city(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["phone"] = step.result
        return await step.prompt("TextPrompt", "And which city do you live in?")

    async def summary(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["city"] = step.result
        summary = (
            f"Thanks! Here's what I got:
"
            f"Name: {step.values['first_name']} {step.values['last_name']}
"
            f"Email: {step.values['email']}
"
            f"Phone: {step.values['phone']}
"
            f"City: {step.values['city']}"
        )
        await step.context.send_activity(summary)
        return await step.end_dialog()