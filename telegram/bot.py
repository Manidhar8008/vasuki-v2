from api.ask import AskAPI
from telegram import Bot

API_TOKEN = "YOUR_TOKEN"

bot = Bot(token=API_TOKEN)
api = AskAPI()

def handle_message(chat_id, text):
    result = api.ask(text)
    bot.send_message(chat_id=chat_id, text=str(result))
