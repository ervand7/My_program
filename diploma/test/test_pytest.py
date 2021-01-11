from diploma.bot.functions_for_BotVkontakte import get_candidates_links, show_list_of_russia_cities, \
    show_liked_candidates
from diploma.db.functions_for_fill_db import get_list_with_liked_candidates, filling_main_user_table, \
    filling_candidates_table, filling_photos_of_candidates_table


class TestFunctionsMyProgram:

    def setup_class(self):
        print('method setup_class')

    def setup(self):
        print("method setup")

    def test_1_get_candidates_links(self):
        assert get_candidates_links(2, 18, 25, 6, 'Барнаул')[0][:20] == '1) https://vk.com/id'

    def test_2_show_list_of_russia_cities(self):
        assert show_list_of_russia_cities()[-2] == 'Углич'

    def test_3_show_liked_candidates(self):
        assert show_liked_candidates() == ['1) https://vk.com/id77239525', '2) https://vk.com/id12716695']

    def test_4_filling_main_user_table(self):
        assert filling_main_user_table(613295858) == [613295858, 1, 'Виктория', 'Самойлова',
                                                      'Международное брачное агентство ищет талантливых парней - '
                                                      'переводчиков от 21-35. Переходите на наш сайт👇🏻⭐']

    def test_5_get_list_with_liked_candidates(self):
        assert get_list_with_liked_candidates() == [77239525, 12716695]

    def test_6_filling_candidates_table(self):
        assert filling_candidates_table() != [
            [77239525, 1, 'Ольга', 'Старцева', 'https://vk.com/id77239525', 457199137],
            [12716695, 2, 'Алекс', 'Сотников', 'https://vk.com/id12716695', 457199137]]

    def test_7_filling_photos_of_candidates_table(self):
        assert filling_photos_of_candidates_table()[1] == {12716695: ((80,
                                                                       'https://sun9-63.userapi.com/c5318/u12716695/-6/y_6db39e38.jpg'),
                                                                      (24,
                                                                       'https://sun9-70.userapi.com/impf/c845124/v845124221/d7e75/1kTpca0XB8c.jpg?size=720x960&quality=96&proxy=1&sign=a5330159f73f1cba9b1a285699e53bbe&c_uniq_tag=qnocKv78mGn-o8-bMeAfPnkl5l2f3dl6m8ekBsCFnvk&type=album'),
                                                                      (10,
                                                                       'https://sun9-31.userapi.com/impf/c11024/v11024695/a97/ntCABkJXFpw.jpg?size=550x550&quality=96&proxy=1&sign=7df3dec76ece325fc7bf7acbcdc12bcd&c_uniq_tag=W35foCSUyOifJfAcGY6xkrz1HvlR-7ZZf4qxGZaT_2k&type=album'))}

    def teardown_class(self):
        print('method teardown_class')

    def teardown(self):
        print("method teardown")
