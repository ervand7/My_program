import sqlalchemy
from pprint import pprint
from diploma.db.functions_for_fill_db import filling_candidates_table, filling_photos_of_candidates_table
from diploma.input_data import your_id
import os
import time

# создаем engine
# dialect+driver://username:password@host:port/database
engine = sqlalchemy.create_engine(
    'postgresql://ingenious_db_user:ingenious_db_user@localhost:5432/ingenious_db')

connection = engine.connect()


def write_candidate_data_in_db(input_main_user_id=your_id):
    main_user_id = input_main_user_id

    # _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    # # # Insert. Добавим данные в candidates
    try:
        for i in filling_candidates_table(main_user_id):
            user_id = i[0]
            user_sex = i[1]
            user_first_name = i[2]
            user_last_name = i[3]
            user_link = i[4]
            user_referenced_main_user_id = i[5]

            insert_candidates = connection.execute(
                f'''INSERT INTO candidates(vk_id, sex, first_name, last_name, candidate_link, main_user_id)
                VALUES ({user_id}, '{user_sex}', '{user_first_name}', '{user_last_name}',
            '{user_link}', '{user_referenced_main_user_id}');
                ''')
            pprint(insert_candidates)
        time.sleep(3)  # without this program can be broken because of too many parse requests to API VK
        # _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
        # # # Insert. Добавим данные в photos_of_candidates
        try:
            for i in filling_photos_of_candidates_table():
                for k, v in i.items():
                    insert_photos_of_candidates = connection.execute(
                        f'''INSERT INTO photos_of_candidates(candidate_vk_id, first_photo_likes_count, first_photo_link,
                        second_photo_likes_count, second_photo_link, third_photo_likes_count, third_photo_link)
                        VALUES ('{k}', '{v[0][0]}', '{v[0][1]}', '{v[1][0]}', '{v[1][1]}', '{v[2][0]}', '{v[2][1]}');
                        ''')
                    pprint(insert_photos_of_candidates)
        except TypeError:
            print('Возможно, за то время, что вам понравился этот кандидат, его заблокировали, либо он удалил '
                  'свою страницу, либо он закрыл свою страницу.')
    except KeyError:
        print('Временное хранилище кандидатов в корневой папке проекта <repository_of_candidates_ids.csv> было '
              'переполнено, а сейчас этого файла уже больше нет! Во временном хранилище может находиться не более '
              '9 кандидатов перед загрузкой данных в БД. Сейчас вам нужно вставить новый <your_id> в файл '
              '<input_data>, запустить файл <main> и заново пройти диалог с ботом :-( В следующий раз будьте '
              'внимательнее!')
    # _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    # # # Удалим временный файл repository_of_candidates_ids
    time.sleep(1)  # without this program can be broken because of file can ce deleted before file data is written in db
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        f"{os.path.abspath('repository_of_candidates_ids.csv')}")
    os.remove(path)
