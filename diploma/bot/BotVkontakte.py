from random import randrange
import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from diploma.bot.functions_for_BotVkontakte import get_candidates_links, show_list_of_russia_cities, adding_in_ban_list, \
    reset_from_ban_list, collect_data_for_adding_to_csv_file, reset_from_liked, show_liked_candidates
from diploma.input_data import TOKEN_FOR_BOT
from diploma.db.db_insert_candidates_and_them_photos import write_candidate_data_in_db


class BotVkontakte:
    def __init__(self):
        self.vk = vk_api.VkApi(token=TOKEN_FOR_BOT)
        self.longpoll = VkLongPoll(self.vk)
        self.search_func_params = [0, 0, 0, 0, '', False, False]
        self.start = 0
        self.end = 2
        self.bracket = ')'
        self.underscore = '_'
        self.box_for_avoid_repeated_outputs = []

    def write_msg(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

    def conversation_between_bot_and_person(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text

                    # here is a block of outputs _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
                    def output_default():
                        return self.write_msg(event.user_id,
                                              "Дружище, попади правильно по клавиатуре :-(")

                    def output_hello():
                        return self.write_msg(event.user_id,
                                              f"Здравствуйте, уважаемый пользователь с id{event.user_id}. "
                                              f"Сейчас мы будем искать вам пару. Будем выводить только тех "
                                              f"пользователей, у которых аккаунт не закрыт, в наличие минимум 3 "
                                              f"фотографии категории 'wall', и рейтинг ВКонтакте = maximum. "
                                              f"Время моего ответа может составлять до 3 "
                                              f"секунд. "
                                              f"\n\nОбратите внимание, при длительном использовании программы, "
                                              f"библиотека vk_api прекратит работу с исключением: "
                                              f"<vk_api.exceptions.ApiError: [9] Flood control: too much messages "
                                              f"sent to user>."
                                              f"\nДавайте начнем с пола. "
                                              f"Введите 'м' или 'ж' и нажмите Enter.")

                    def output_select_age():
                        return self.write_msg(event.user_id,
                                              "Пол выбран! Выберите возрастную категорию и нажмите enter:\n"
                                              "1 - <18-25>\n"
                                              "2 - <26-32>\n"
                                              "3 - <33-42>\n"
                                              "4 - <43-55>\n"
                                              "5 - <55 + >\n")

                    def output_select_marital_status():
                        return self.write_msg(event.user_id,
                                              "Возраст выбран! Давайте определим семейный статус кандидата. "
                                              "Выберите категорию и нажмите enter:\n"
                                              "а - <не женат (не замужем)>\n"
                                              "б - <в активном поиске>\n"
                                              "в - <все сложно>")

                    def output_select_city():
                        return self.write_msg(event.user_id,
                                              "Семейный статус выбран! Осталось ввести название города, из которого "
                                              "вы хотите найти свою любовь, и нажать Enter.")

                    def output_select_or_refuse_candidate():
                        return self.write_msg(event.user_id,
                                              'Все параметры заполнены! Вам представлены несколько кандидатур. '
                                              'Они соответствуют заданным параметрам. Можно перейти по ссылке, '
                                              'посмотреть, нравится человек или нет.'
                                              '\n ● Если кто-то нравится, то в формате <нравится_2> введите '
                                              'номер претендента (добавлять можно только по одному) и нажмите '
                                              'Enter. Мы добавим его в список понравившихся.'
                                              '\n ● Если же хотите пополнить ваш черный список этими людьми, '
                                              'то введите номера ссылок на профили этих людей '
                                              'в формате <чс_1> (добавлять можно только по одному) и нажмите Enter.'
                                              '\n ● Если хотите пропустить все и перейти к следующим претендентам, то '
                                              'наберите 0 и нажмите Enter.'
                                              '\n ● Если хотите вернуться в начало поиска, наберите <привет> и '
                                              'нажмите Enter.')

                    def output_adding_in_ban():
                        return self.write_msg(event.user_id, "Супер! Все что нужно, мы переместили в чс :-) Можете "
                                                             "проверить это в настройках своего аккаунта Вконтаке."
                                                             "\n ● Будем повторно искать кандидатов с такими "
                                                             "параметрами? Наберите '0' и нажмите Enter."
                                                             "\n ● Если хотите кого-либо удалить из черного списка, "
                                                             "введите номер его ссылки в формате <убрать_2> "
                                                             "(убирать можно только по одному)")

                    def output_reset_from_ban_list():
                        return self.write_msg(event.user_id, "Супер! Все что нужно, удалено из чс :-) Можете "
                                                             "проверить это в настройках своего аккаунта Вконтаке."
                                                             "\n ● Будем повторно искать кандидатов с такими "
                                                             "параметрами? Наберите '0' и нажмите Enter."
                                                             "\n ● Если хотите вернуться в начало поиска, наберите "
                                                             "<привет> и нажмите Enter.")

                    def output_adding_in_liked_list():
                        return self.write_msg(event.user_id, "Супер! Все, что нужно, внесено в список понравившихся :-)"
                                                             "\n ● Будем повторно искать кандидатов с такими "
                                                             "параметрами? Наберите '0' и нажмите Enter."
                                                             "\n ● Если хотите просмотреть список понравившихся "
                                                             "кандидатов, наберите <хочу> и нажмите Enter.")

                    def output_show_liked_candidates():
                        return self.write_msg(event.user_id, "Вот все понравившиеся:-)"
                                                             "\n ● Удалить кого-нибудь из понравившихся? Если да, "
                                                             "то наберите номер ссылки в формате "
                                                             "<разонравился_2> (удалять можно только по одному) "
                                                             "и нажмите Enter."
                                                             "\n ● Если хотите заново начать поиск, наберите <привет> "
                                                             "и нажмите Enter.")

                    def output_unliked():
                        return self.write_msg(event.user_id, "Разонравившийся удален из списка понравившихся."
                                                             "\n ● Если хотите заново начать поиск, наберите <привет> "
                                                             "и нажмите Enter."
                                                             "\n ● Если хотите просмотреть список понравившихся "
                                                             "кандидатов, наберите <хочу> и нажмите Enter."
                                                             "\n ● Если хотите еще удалить кого-нибудь из "
                                                             "понравившихся, наберите номер ссылки в формате "
                                                             "<разонравился_2> (удалять можно только по одному) "
                                                             "и нажмите Enter.")

                    def output_dead_end():
                        return self.write_msg(event.user_id, "Все, по этим параметра больше никого нет. Вот все, "
                                                             "кто есть."
                                                             "\n ● Если кто-то нравится, то в формате <нравится_2> "
                                                             "введите номер претендента "
                                                             "(добавлять можно только по одному) и нажмите Enter. "
                                                             "Мы добавим его в список понравившихся."
                                                             "\n ● Если хотите заново начать поиск, наберите <привет> "
                                                             "и нажмите Enter."
                                                             "\n ● Если хотите просмотреть список понравившихся "
                                                             "кандидатов, наберите <хочу> и нажмите Enter.")

                    def output_end_of_candidates():
                        return self.write_msg(event.user_id, "Вам уже показывались люди по таким параметрам! "
                                                             "Если хотите еще увидеть подобных, то наберите <т> и "
                                                             "нажмите Enter.")

                    def output_wait_10_sec():
                        return self.write_msg(event.user_id, "Подождите 10 секунд :-), не уходите:-))")

                    def output_good_bye():
                        return self.write_msg(event.user_id, "Данные занесены базу данных. Программа завершена. "
                                                             "Теперь перейдите в вашем IDE в папку <output_data> "
                                                             "и запустите файл <json_dump>, после чего у вас появится "
                                                             "в той же директории файл <program_result_output.json> "
                                                             "с результатми работы данной программы. "
                                                             "\nА так же в корневой папке вы найдете файл <logs.log> "
                                                             "в котором представлен ход работы некоторых функций, "
                                                             "это интересно)."
                                                             "\nСпасибо, что выбрали нас :-).")

                    # here is a block of main logic _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
                    # _______ writing a greeting _______
                    if request == 'привет' or request == 'Привет':
                        time.sleep(1)
                        self.start = 0
                        self.end = 2
                        self.search_func_params[5] = True
                        output_hello()

                    # _______ variants of selecting sex _______
                    elif self.search_func_params[5] is True and request == 'м':
                        time.sleep(1)
                        self.search_func_params[0] = 2
                        output_select_age()

                    elif self.search_func_params[5] is True and request == 'ж':
                        time.sleep(1)
                        self.search_func_params[0] = 1
                        output_select_age()

                    # _______ variants of selecting age range _______
                    elif self.search_func_params[0] != 0 and request == '1':
                        time.sleep(1)
                        self.search_func_params[1] = 18
                        self.search_func_params[2] = 25
                        output_select_marital_status()

                    elif self.search_func_params[0] != 0 and request == '2':
                        time.sleep(1)
                        self.search_func_params[1] = 26
                        self.search_func_params[2] = 32
                        output_select_marital_status()

                    elif self.search_func_params[0] != 0 and request == '3':
                        time.sleep(1)
                        self.search_func_params[1] = 33
                        self.search_func_params[2] = 42
                        output_select_marital_status()

                    elif self.search_func_params[0] != 0 and request == '4':
                        time.sleep(1)
                        self.search_func_params[1] = 43
                        self.search_func_params[2] = 55
                        output_select_marital_status()

                    elif self.search_func_params[0] != 0 and request == '5':
                        time.sleep(1)
                        self.search_func_params[1] = 56
                        self.search_func_params[2] = 100
                        output_select_marital_status()

                    # _______ variants of selecting marital status _______
                    elif self.search_func_params[2] != 0 and request == 'а':
                        time.sleep(1)
                        self.search_func_params[3] = 1
                        output_select_city()

                    elif self.search_func_params[2] != 0 and request == 'б':
                        time.sleep(1)
                        self.search_func_params[3] = 6
                        output_select_city()

                    elif self.search_func_params[2] != 0 and request == 'в':
                        time.sleep(1)
                        self.search_func_params[3] = 5
                        output_select_city()

                    # _______ selecting city and first output with links _______
                    elif self.search_func_params[3] != 0 and str(request).title() in show_list_of_russia_cities():
                        self.search_func_params[4] = request
                        self.search_func_params[6] = True
                        counter_ = 0
                        for i in get_candidates_links(self.search_func_params[0],
                                                      self.search_func_params[1],
                                                      self.search_func_params[2],
                                                      self.search_func_params[3],
                                                      self.search_func_params[4])[self.start:self.end]:

                            if not i in self.box_for_avoid_repeated_outputs:
                                counter_ += 1
                                self.write_msg(event.user_id, str(i))
                                self.box_for_avoid_repeated_outputs.append(i)
                            else:
                                output_end_of_candidates()
                                break
                        if counter_ == 2:
                            output_select_or_refuse_candidate()

                    # _______ adding candidate in block list _______
                    elif self.search_func_params[6] is True and 'чс_' in str(request):
                        try:
                            for link in get_candidates_links(self.search_func_params[0],
                                                             self.search_func_params[1],
                                                             self.search_func_params[2],
                                                             self.search_func_params[3],
                                                             self.search_func_params[4]):
                                find_number = int(request[request.index(self.underscore) + 1:])
                                if int(find_number) == int(link[:link.index(self.bracket)]):
                                    adding_in_ban_list(int(link[link.index(self.bracket) + 19:]))
                        except vk_api.exceptions.ApiError:
                            print('')
                        output_adding_in_ban()

                    # _______ reset candidates from ban list _______
                    elif self.search_func_params[6] is True and 'убрать_' in str(request):
                        try:
                            for link in get_candidates_links(self.search_func_params[0],
                                                             self.search_func_params[1],
                                                             self.search_func_params[2],
                                                             self.search_func_params[3],
                                                             self.search_func_params[4]):
                                find_number = int(request[request.index(self.underscore) + 1:])
                                if int(find_number) == int(link[:link.index(self.bracket)]):
                                    reset_from_ban_list(int(link[link.index(self.bracket) + 19:]))
                        except vk_api.exceptions.ApiError:
                            print('')
                        output_reset_from_ban_list()

                    # _______ adding candidate in liked list (special csv file) _______
                    elif self.search_func_params[6] is True and 'нравится_' in str(request):
                        auxiliary_list = []
                        for link_ in get_candidates_links(self.search_func_params[0],
                                                          self.search_func_params[1],
                                                          self.search_func_params[2],
                                                          self.search_func_params[3],
                                                          self.search_func_params[4]):
                            find_number = int(request[request.index(self.underscore) + 1:])
                            if int(find_number) == int(link_[:link_.index(self.bracket)]):
                                auxiliary_list.append(link_[link_.index(self.bracket) + 19:])
                        list_for_csv_file = []
                        for i in auxiliary_list:
                            sub = i.split(', ')
                            list_for_csv_file.append(sub)
                        collect_data_for_adding_to_csv_file(list_for_csv_file)
                        output_adding_in_liked_list()

                    # _______ output of liked candidates _______
                    elif self.search_func_params[6] is True and 'хочу' in str(request):
                        time.sleep(1)
                        for i in show_liked_candidates():
                            self.write_msg(event.user_id, str(i))
                        output_show_liked_candidates()

                    # _______ repeated output of candidates _______
                    elif self.search_func_params[6] is True and request == '0':
                        self.start += 2
                        self.end += 2
                        for i in get_candidates_links(self.search_func_params[0],
                                                      self.search_func_params[1],
                                                      self.search_func_params[2],
                                                      self.search_func_params[3],
                                                      self.search_func_params[4])[self.start:self.end]:
                            self.write_msg(event.user_id, str(i))
                            self.box_for_avoid_repeated_outputs.append(i)
                        output_select_or_refuse_candidate()

                    # _______ reset unliked candidates _______
                    elif self.search_func_params[6] is True and 'разонравился_' in str(request):
                        time.sleep(1)
                        for i in show_liked_candidates():
                            find_number = int(request[request.index(self.underscore) + 1:])
                            if int(find_number) == int(i[:i.index(self.bracket)]):
                                reset_from_liked(find_number)
                        output_unliked()

                    # _______ when candidates with set parameters ended _______
                    elif self.search_func_params[6] is True and request == 'т':
                        for i in get_candidates_links(self.search_func_params[0],
                                                      self.search_func_params[1],
                                                      self.search_func_params[2],
                                                      self.search_func_params[3],
                                                      self.search_func_params[4]):
                            if i in self.box_for_avoid_repeated_outputs:
                                continue
                            else:
                                self.write_msg(event.user_id, str(i))
                        output_dead_end()

                    # _______ ending of program and writing data in db_______
                    elif self.search_func_params[6] is True and request == 'готово':
                        output_wait_10_sec()
                        write_candidate_data_in_db()
                        output_good_bye()

                    # _______ user mistake warning _______
                    else:
                        time.sleep(1)
                        output_default()
