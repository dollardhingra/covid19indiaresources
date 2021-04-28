from telegram import Update


class CustomLogger:
    @staticmethod
    def get_formatted_str(update: Update) -> str:
        return f"chat_id:{update.effective_chat.id}|user_id:{update.effective_user.id}|first_name:{update.effective_user.first_name}"
