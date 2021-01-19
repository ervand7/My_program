from random import randrange
import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from diploma.bot.functions_for_BotVkontakte import get_candidates_links, show_list_of_russia_cities, adding_in_ban_list, \
    reset_from_ban_list, collect_data_for_adding_to_csv_file, reset_from_liked, show_liked_candidates
from diploma.input_data import TOKEN_FOR_BOT
from diploma.db.db_insert_candidates_and_them_photos import write_candidate_data_in_db
import diploma.bot.messages


class BotVkontakte:
    def __init__(self):
        self.vk = vk_api.VkApi(token=TOKEN_FOR_BOT)
        self.longpoll = VkLongPoll(self.vk)

        # _______ parameters for fill list <self.search_func_params> _______
        self.sex = 0
        self.age_from = 0
        self.age_to = 0
        self.marital_status = 0
        self.city = ''
        self.start_dialog = False
        self.city_is_selected = False
        self.search_func_params = [self.sex, self.age_from, self.age_to, self.marital_status, self.city,
                                   self.start_dialog, self.city_is_selected]

        # _______ auxiliary parameters _______
        self.symbols_before_id = 19
        self.start_from_index = 0
        self.end_to_index = 2
        self.link_message_bracket = ')'
        self.underscore = '_'
        self.box_for_avoid_repeated_outputs = []

        # _______ boolean parameters _______
        self.dialog_was_started = 5
        self.all_parameters_are_filled = 6

        # _______ sex parameters _______
        self.woman_ = 1
        self.man_ = 2

        # _______ age parameters _______
        self.age_from_ = 1
        self.age_to_ = 2

        # _______ family status parameters _______
        self.marital_status_ = 3
        self.not_married = 1
        self.all_is_difficult = 6
        self.in_active_search = 5

        # _______ city parameters _______
        self.city_ = 4

    def write_msg(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

    def conversation_between_bot_and_person(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text

                    # here is a block of outputs _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
                    def output_default():
                        return self.write_msg(event.user_id, diploma.bot.messages.message_1)

                    def output_hello():
                        return self.write_msg(event.user_id, diploma.bot.messages.message_2)

                    def output_select_age():
                        return self.write_msg(event.user_id, diploma.bot.messages.message_3)

                    def output_select_marital_status():
                        return self.write_msg(event.user_id, diploma.bot.messages.message_4)

                    def output_select_city():
                        return self.write_msg(event.user_id, diploma.bot.messages.message_5)

                    def output_select_or_refuse_candidate():
                        return self.write_msg(event.user_id, diploma.bot.messages.message_6)

                    def output_adding_in_ban():
                        return self.write_msg(event.user_id, diploma.bot.messages.message_7)

                    def output_reset_from_ban_list():
                        return self.write_msg(event.user_id, diploma.bot.messages.message_8)

                    def output_adding_in_liked_list():
                        return self.write_msg(event.user_id, diploma.bot.messages.message_9)

                    def output_show_liked_candidates():
                        return self.write_msg(event.user_id, diploma.bot.messages.message_10)

                    def output_unliked():
                        return self.write_msg(event.user_id, diploma.bot.messages.message_11)

                    def output_dead_end():
                        return self.write_msg(event.user_id, diploma.bot.messages.message_12)

                    def output_end_of_candidates():
                        return self.write_msg(event.user_id, diploma.bot.messages.message_13)

                    def output_wait_10_sec():
                        return self.write_msg(event.user_id, diploma.bot.messages.message_14)

                    def output_good_bye():
                        return self.write_msg(event.user_id, diploma.bot.messages.message_15)

                    # here is a block of main logic _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
                    # _______ writing a greeting _______
                    if request == 'привет':
                        self.start_from_index = 0  # при каждом 'привет' идет сброс этих параметров
                        self.end_to_index = 2  # при каждом 'привет' идет сброс этих параметров
                        self.search_func_params[self.dialog_was_started] = True
                        output_hello()

                    # _______ variants of selecting sex _______
                    elif self.search_func_params[self.dialog_was_started] is True and request == 'м':
                        self.search_func_params[self.sex] = self.man_
                        output_select_age()

                    elif self.search_func_params[self.dialog_was_started] is True and request == 'ж':
                        self.search_func_params[self.sex] = self.woman_
                        output_select_age()

                    # _______ variants of selecting age range _______
                    elif self.search_func_params[self.sex] != 0 and request == '1':
                        self.search_func_params[self.age_from_] = 18
                        self.search_func_params[self.age_to_] = 25
                        output_select_marital_status()

                    elif self.search_func_params[self.sex] != 0 and request == '2':
                        self.search_func_params[self.age_from_] = 26
                        self.search_func_params[self.age_to_] = 32
                        output_select_marital_status()

                    elif self.search_func_params[self.sex] != 0 and request == '3':
                        self.search_func_params[self.age_from_] = 33
                        self.search_func_params[self.age_to_] = 42
                        output_select_marital_status()

                    elif self.search_func_params[self.sex] != 0 and request == '4':
                        self.search_func_params[self.age_from_] = 43
                        self.search_func_params[self.age_to_] = 55
                        output_select_marital_status()

                    elif self.search_func_params[self.sex] != 0 and request == '5':
                        self.search_func_params[self.age_from_] = 56
                        self.search_func_params[self.age_to_] = 100
                        output_select_marital_status()

                    # _______ variants of selecting marital status _______
                    elif self.search_func_params[self.age_to_] != 0 and request == 'а':
                        self.search_func_params[self.marital_status_] = self.not_married
                        output_select_city()

                    elif self.search_func_params[self.age_to_] != 0 and request == 'б':
                        self.search_func_params[self.marital_status_] = self.all_is_difficult
                        output_select_city()

                    elif self.search_func_params[self.age_to_] != 0 and request == 'в':
                        self.search_func_params[self.marital_status_] = self.in_active_search
                        output_select_city()

                    # _______ selecting city and first output with links _______
                    elif self.search_func_params[self.marital_status_] != 0 and str(
                            request).title() in show_list_of_russia_cities():
                        self.search_func_params[self.city_] = request
                        self.search_func_params[self.all_parameters_are_filled] = True
                        counter_ = 0
                        filled_params = get_candidates_links(self.search_func_params[0],
                                                             self.search_func_params[1],
                                                             self.search_func_params[2],
                                                             self.search_func_params[3],
                                                             self.search_func_params[4])
                        for i in filled_params[self.start_from_index:self.end_to_index]:

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
                    elif self.search_func_params[self.all_parameters_are_filled] is True and 'чс_' in str(request):
                        try:
                            for link in filled_params:
                                find_number = int(request[request.index(self.underscore) + 1:])
                                if int(find_number) == int(link[:link.index(self.link_message_bracket)]):
                                    adding_in_ban_list(int(link[link.index(self.link_message_bracket) +
                                                                self.symbols_before_id:]))
                        except vk_api.exceptions.ApiError:
                            print('')
                        output_adding_in_ban()

                    # _______ reset candidates from ban list _______
                    elif self.search_func_params[self.all_parameters_are_filled] is True and 'убрать_' in str(request):
                        try:
                            for link in filled_params:
                                find_number = int(request[request.index(self.underscore) + 1:])
                                if int(find_number) == int(link[:link.index(self.link_message_bracket)]):
                                    reset_from_ban_list(int(link[link.index(self.link_message_bracket) +
                                                                 self.symbols_before_id:]))
                        except vk_api.exceptions.ApiError:
                            print('')
                        output_reset_from_ban_list()

                    # _______ adding candidate in liked list (special csv file) _______
                    elif self.search_func_params[self.all_parameters_are_filled] is True and 'нравится_' in str(
                            request):
                        auxiliary_list = []
                        for link_ in filled_params:
                            find_number = int(request[request.index(self.underscore) + 1:])
                            if int(find_number) == int(link_[:link_.index(self.link_message_bracket)]):
                                auxiliary_list.append(link_[link_.index(self.link_message_bracket) +
                                                            self.symbols_before_id:])
                        list_for_csv_file = []
                        for i in auxiliary_list:
                            sub = i.split(', ')
                            list_for_csv_file.append(sub)
                        collect_data_for_adding_to_csv_file(list_for_csv_file)
                        output_adding_in_liked_list()

                    # _______ output of liked candidates _______
                    elif self.search_func_params[self.all_parameters_are_filled] is True and 'хочу' in str(request):
                        for i in show_liked_candidates():
                            self.write_msg(event.user_id, str(i))
                        output_show_liked_candidates()

                    # _______ repeated output of candidates _______
                    elif self.search_func_params[self.all_parameters_are_filled] is True and request == '0':
                        self.start_from_index += 2
                        self.end_to_index += 2
                        for i in filled_params[self.start_from_index:self.end_to_index]:
                            self.write_msg(event.user_id, str(i))
                            self.box_for_avoid_repeated_outputs.append(i)
                        output_select_or_refuse_candidate()

                    # _______ reset unliked candidates _______
                    elif self.search_func_params[self.all_parameters_are_filled] is True and 'разонравился_' in str(
                            request):
                        for i in show_liked_candidates():
                            find_number = int(request[request.index(self.underscore) + 1:])
                            if int(find_number) == int(i[:i.index(self.link_message_bracket)]):
                                reset_from_liked(find_number)
                        output_unliked()

                    # _______ when candidates with set parameters ended _______
                    elif self.search_func_params[self.all_parameters_are_filled] is True and request == 'т':
                        for i in filled_params:
                            if i in self.box_for_avoid_repeated_outputs:
                                continue
                            else:
                                self.write_msg(event.user_id, str(i))
                        output_dead_end()

                    # _______ ending of program and writing data in db_______
                    elif self.search_func_params[self.all_parameters_are_filled] is True and request == 'готово':
                        try:
                            output_wait_10_sec()
                            write_candidate_data_in_db()
                            output_good_bye()
                        except FileNotFoundError:
                            print('Вы ввели команду <готово> до того, как добавили кого-то в список понравившихся! '
                                  'Напишите <привет> боту и продолжите общение.')

                    # _______ user mistake warning _______
                    else:
                        time.sleep(1)
                        output_default()
