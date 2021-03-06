import sqlalchemy
import json
import os
from diploma.input_data import db_name, db_owner, db_password

engine = sqlalchemy.create_engine(
    f'postgresql://{db_owner}:{db_password}@localhost:5432/{db_name}')

connection = engine.connect()

select_candidates_and_them_photos_from_db = connection.execute("""
SELECT c.candidate_link, p.first_photo_link, p.second_photo_link, p.third_photo_link FROM photos_of_candidates p
LEFT JOIN candidates c ON c.vk_id = p.candidate_vk_id;
""").fetchall()


def json_dump():
    json_value = []
    for candidate in select_candidates_and_them_photos_from_db:
        dct_candidate = {candidate[0]: (candidate[1], candidate[2], candidate[3])}
        json_value.append(dct_candidate)
    json_data = dict()
    json_data['info'] = json_value

    file_path = os.path.join(os.getcwd(), "program_result_output.json")
    with open(file_path, 'w+') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)


json_dump()
