import vk_api
import os
import json
import csv
import requests
from diploma.input_data import user_api_token
from urllib.parse import urljoin
from diploma.servise_and_auxiliary_files.log_decorator_function import decorator_with_way_to_file
from pprint import pprint  # do not delete this!

vk_ = vk_api.VkApi(token=user_api_token, api_version="5.89")


# ____________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________

@decorator_with_way_to_file(file_name='logs.log')
def get_candidates_links(sex: int, age_from: int, age_to: int, marital_status: int, city: str):
    """STEP 1: SETTING PARAMS FOR METHOD 'users.search' (API VK). DEFINE SEX, AGE, MARITAL STATUS and CITY"""
    candidates = vk_.method('users.search',
                            {'sort': 0,
                             'sex': sex,
                             'status': marital_status,
                             'age_from': age_from,
                             'age_to': age_to,
                             'has_photo': 1,
                             'count': 1000,
                             'online': 1,
                             'hometown': city,
                             'is_closed': False,
                             'can_access_closed': False
                             })

    # STEP 2: CHOOSE ONLY OPEN ACCOUNTS
    counter_1 = 0
    for i in candidates['items']:
        if i['is_closed'] is False:
            counter_1 += 1

    filter_close_or_open_account = []
    if candidates['count'] < 1000:
        for candidate_index in range(counter_1):
            if str(candidates['items'][candidate_index]['is_closed']) == 'True':
                continue
            candidate_id = str(candidates['items'][candidate_index]['id'])
            filter_close_or_open_account.append(candidate_id)
    else:
        for candidate_index in range(950):
            if str(candidates['items'][candidate_index]['is_closed']) == 'True':
                continue
            candidate_id = str(candidates['items'][candidate_index]['id'])
            filter_close_or_open_account.append(candidate_id)

    # STEP 3: CHOOSE ACCOUNTS THAT HAVE AT LEAST 3 PROFILE PHOTO
    filter_at_least_three_photo = []
    try:
        for person in filter_close_or_open_account:
            api_base_url = 'https://api.vk.com/method/'
            api_version = '5.21'
            url_for_demand = urljoin(api_base_url, 'photos.get')
            photo_count_response = requests.get(url_for_demand, params={
                'access_token': user_api_token,
                'v': api_version,
                'owner_id': person,
                'album_id': 'profile'
            })

            if photo_count_response.json()['response']['count'] < 3:
                continue
            filter_at_least_three_photo.append(person)
    except KeyError:
        print('')

    # STEP 4: MAKING LINKS
    final_list_account_links = []
    for number, element in enumerate(filter_at_least_three_photo, 1):
        begin_url = 'https://vk.com/'
        link = f'{number}) ' + urljoin(begin_url, f"id{element}")
        final_list_account_links.append(link)
    return final_list_account_links


# # check:
# pprint(get_candidates_links(2, 18, 25, 6, 'Барнаул'))


# ____________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________

def show_list_of_russia_cities():
    with open(os.path.join(os.path.dirname(__file__), 'cities.json'), encoding='utf-8-sig') as f:
        json_data = json.load(f)
        list_of_cities = [i['Город'] for i in json_data]
    return list_of_cities


# # check:
# pprint(show_list_of_russia_cities())
# ____________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________

@decorator_with_way_to_file(file_name='logs.log')
def adding_in_ban_list(id_):
    vk_.method('account.ban',
               {'owner_id': id_})


# # check:
# print(adding_in_ban_list(57545445))


@decorator_with_way_to_file(file_name='logs.log')
def reset_from_ban_list(id_):
    vk_.method('account.unban',
               {'owner_id': id_})


# # check:
# print(reset_from_ban_list(57545445))


# ____________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________

@decorator_with_way_to_file(file_name='logs.log')
def collect_data_for_adding_to_csv_file(prepared_list_of_lists,
                                        mode='a+'):  # example [['1231233'], ['2334234'], ['3453446']]
    csv.register_dialect("customcsv", delimiter=",", quoting=csv.QUOTE_NONE, quotechar="`", escapechar="\\")
    file_path = os.path.join(os.getcwd(), "repository_of_candidates_ids.csv")
    with open(file_path, mode) as f:
        data_writer = csv.writer(f, "customcsv")
        data_writer.writerows(prepared_list_of_lists)


# # check:
# collect_data_for_adding_to_csv_file([['1231233'], ['2334234'], ['3453446']])


# ____________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________

@decorator_with_way_to_file(file_name='logs.log')
def show_liked_candidates():
    def get_list_with_liked_candidates():
        list_liked_candidates = []
        with open("repository_of_candidates_ids.csv", newline='') as file:
            reader = csv.reader(file)
            for row in list(reader):
                list_liked_candidates.append(int(*row))
        return list_liked_candidates

    def get_list_links_liked_candidates():
        list_with_made_links = []
        begin_url = 'https://vk.com/'
        for id_ in get_list_with_liked_candidates():
            made_link = urljoin(begin_url, f"id{str(id_)}")
            list_with_made_links.append(made_link)
        list_number_link = []
        for number, link in enumerate(list_with_made_links, 1):
            row_ = f'{number}) ' + link
            list_number_link.append(row_)
        return list_number_link

    return get_list_links_liked_candidates()


# pprint(show_liked_candidates())


# ____________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________

@decorator_with_way_to_file(file_name='logs.log')
def reset_from_liked(number):
    list_without_unliked_candidate = []
    bracket = ')'
    for link_ in show_liked_candidates():
        if int(number) == int(link_[:link_.index(bracket)]):
            continue
        list_without_unliked_candidate.append(link_)
    list_for_csv_file = []
    for elem in list_without_unliked_candidate:
        sub = elem[elem.index(bracket) + 19:].split(', ')
        list_for_csv_file.append(sub)
    collect_data_for_adding_to_csv_file(list_for_csv_file, 'w')

# ____________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________
