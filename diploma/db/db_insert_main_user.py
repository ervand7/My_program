import sqlalchemy
from pprint import pprint
from diploma.db.functions_for_fill_db import filling_main_user_table
from diploma.input_data import your_id
from diploma.input_data import db_name, db_owner, db_password

# создаем engine
# dialect+driver://username:password@host:port/database
engine = sqlalchemy.create_engine(
    f'postgresql://{db_owner}:{db_password}@localhost:5432/{db_name}')

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
