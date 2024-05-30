from bot import bot_app
if __name__ == '__main__':
    try:
        bot_app()
    except Exception as e:
        print(e)
