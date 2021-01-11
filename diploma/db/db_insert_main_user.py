import sqlalchemy
from pprint import pprint
from diploma.db.functions_for_fill_db import filling_main_user_table
from diploma.input_data import your_id

# создаем engine
# dialect+driver://username:password@host:port/database
engine = sqlalchemy.create_engine(
    'postgresql://test_user_03_01_2021:test_user_03_01_2021@localhost:5432/diploma_empty_database')

connection = engine.connect()


# # # Insert. Добавим данные в main_user
def write_main_user_data_in_db(input_main_user_id=your_id):
    main_user_id = input_main_user_id
    user_id = filling_main_user_table(main_user_id)[0]
    user_sex = filling_main_user_table(main_user_id)[1]
    user_first_name = filling_main_user_table(main_user_id)[2]
    user_last_name = filling_main_user_table(main_user_id)[3]
    user_status = filling_main_user_table(main_user_id)[4]

    insert_main_user = connection.execute(f'''INSERT INTO main_user(vk_id, sex, first_name, last_name, status)
        VALUES ({user_id}, '{user_sex}', '{user_first_name}', '{user_last_name}', '{user_status}');
        ''')
    pprint(insert_main_user)


write_main_user_data_in_db()