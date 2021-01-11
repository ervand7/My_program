from diploma.bot.BotVkontakte import BotVkontakte
from diploma.db.db_insert_main_user import write_main_user_data_in_db  # it shows environment of loading in db


if __name__ == '__main__':
    experimental = BotVkontakte()
    experimental.conversation_between_bot_and_person()


