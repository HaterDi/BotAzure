from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, TextPrompt, DialogTurnResult
from botbuilder.dialogs.prompts import PromptOptions
from db import insert_user

class RegistrationDialog(ComponentDialog):
    def __init__(self, dialog_id: str = "registrationDialog"):
        super(RegistrationDialog, self).__init__(dialog_id)

        self.add_dialog(TextPrompt("TextPrompt"))
        self.add_dialog(WaterfallDialog("WFDialog", [
            self.ask_name,
            self.ask_surname,
            self.ask_email,
            self.ask_phone,
            self.ask_birth_date,
            self.ask_street,
            self.ask_house_number,
            self.ask_zip_code,
            self.ask_country,
            self.ask_city,
            self.summary
        ]))

        self.initial_dialog_id = "WFDialog"

    async def ask_name(self, step: WaterfallStepContext) -> DialogTurnResult:
        return await step.prompt("TextPrompt", PromptOptions(prompt="Hi! What's your first name?"))

    async def ask_surname(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["first_name"] = step.result
        return await step.prompt("TextPrompt", PromptOptions(prompt="Great, now your last name?"))

    async def ask_email(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["last_name"] = step.result
        return await step.prompt("TextPrompt", PromptOptions(prompt="What's your email?"))

    async def ask_phone(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["email"] = step.result
        return await step.prompt("TextPrompt", PromptOptions(prompt="Your phone number?"))

    async def ask_birth_date(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["phone"] = step.result
        return await step.prompt("TextPrompt", PromptOptions(prompt="What is your date of birth? (YYYY-MM-DD)"))

    async def ask_street(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["birth_date"] = step.result
        return await step.prompt("TextPrompt", PromptOptions(prompt="Your street name?"))

    async def ask_house_number(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["street"] = step.result
        return await step.prompt("TextPrompt", PromptOptions(prompt="House number?"))

    async def ask_zip_code(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["house_number"] = step.result
        return await step.prompt("TextPrompt", PromptOptions(prompt="Postal code (ZIP)?"))

    async def ask_country(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["zip_code"] = step.result
        return await step.prompt("TextPrompt", PromptOptions(prompt="Your country?"))

    async def ask_city(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["country"] = step.result
        return await step.prompt("TextPrompt", PromptOptions(prompt="And which city do you live in?"))

    async def summary(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["city"] = step.result

        user = {
            "first_name": step.values["first_name"],
            "last_name": step.values["last_name"],
            "birth_date": step.values["birth_date"],
            "email": step.values["email"],
            "phone": step.values["phone"],
            "street": step.values["street"],
            "house_number": step.values["house_number"],
            "zip_code": step.values["zip_code"],
            "city": step.values["city"],
            "country": step.values["country"]
        }

        insert_user(user)

        summary = (
            f"Thanks! Here's what I got:\n"
            f"Name: {user['first_name']} {user['last_name']}\n"
            f"Birth date: {user['birth_date']}\n"
            f"Email: {user['email']}\n"
            f"Phone: {user['phone']}\n"
            f"Address: {user['street']} {user['house_number']}, {user['zip_code']} {user['city']}, {user['country']}\n"
            f"✅ Your data has been saved!"
        )

        await step.context.send_activity(summary)
        return await step.end_dialog()
