import vk_api
from diploma.bot.BotVkontakte import BotVkontakte
from diploma.db.db_insert_main_user import write_main_user_data_in_db  # it shows environment of loading in db

if __name__ == '__main__':
    try:
        experimental = BotVkontakte()
        experimental.conversation_between_bot_and_person()
    except vk_api.exceptions.ApiError:
        print('Библиотека vk_api ограничевает кол-во сообщений. В ближайший час с этим TOKEN_FOR_BOT '
              'вы не сможете продолжить работу. Запустите программу заново через час, либо создайте новое '
              'сообщество и с его TOKEN_FOR_BOT запустите программу заново сейчас.')
