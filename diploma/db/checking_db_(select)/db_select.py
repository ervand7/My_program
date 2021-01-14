import psycopg2
import sqlalchemy
from pprint import pprint

# создаем engine
# dialect+driver://username:password@host:port/database
engine = sqlalchemy.create_engine(
    'postgresql://ingenious_db_user:ingenious_db_user@localhost:5432/ingenious_db')
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
