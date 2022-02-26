from bot import Bot

bot = Bot()

while True:
    request = input()
    answer = bot.get_response(request)
    print(f"Bot: {answer}")
