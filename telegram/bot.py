from api.ask import AskAPI

api = AskAPI()

def handle_message(text):
    return api.ask(text)
