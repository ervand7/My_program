import sqlalchemy
from pprint import pprint
from diploma.input_data import db_name, db_owner, db_password

# создаем engine
# dialect+driver://username:password@host:port/database
engine = sqlalchemy.create_engine(
    f'postgresql://{db_owner}:{db_password}@localhost:5432/{db_name}')
# pprint(engine)

# установим соединение
connection = engine.connect()
# pprint(connection)

# Посмотрим, какие таблицы есть
# pprint(engine.table_names())

# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
# # # Проверим
select_main_user = connection.execute('''SELECT * FROM main_user;
''').fetchall()
# pprint(select_main_user)

select_candidates = connection.execute('''SELECT * FROM candidates;
''').fetchall()
# pprint(select_candidates)

select_photos_of_candidates = connection.execute('''SELECT * FROM photos_of_candidates;
''').fetchall()
# pprint(select_photos_of_candidates)
