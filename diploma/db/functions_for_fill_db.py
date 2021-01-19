import csv
import os
import requests
from urllib.parse import urljoin
from diploma.input_data import user_api_token, your_id
from diploma.service_and_auxiliary_files.log_decorator_function import decorator_with_way_to_file
from pprint import pprint  # do not delete this! It is for checking separately functions

api_base_url = 'https://api.vk.com/method/'
api_version = '5.21'
main_session_user_id = your_id


# PREVIOUS WE ARE GETTING ACCESS TO SCV FILE DATA WITH CANDIDATES IDS
@decorator_with_way_to_file(file_name='logs.log')
def get_list_with_liked_candidates():
    list_liked_candidates = []
    with open(f"{os.path.abspath('repository_of_candidates_ids.csv')}", newline='') as file:
        reader = csv.reader(file)
        for row in list(reader):
            list_liked_candidates.append(int(*row))
    return list_liked_candidates


# _______________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________
# -----------------------------------== FILLING DATABASE TABLE main_user ==---------------------------------------

@decorator_with_way_to_file(file_name='logs.log')
def filling_main_user_table(main_user_id=main_session_user_id):
    demand_url = urljoin(api_base_url, 'users.get')
    get_user_info_response = requests.get(demand_url, params={
        'access_token': user_api_token,
        'v': api_version,
        'user_ids': main_user_id,
        'album_id': 'profile',
        'fields': 'city, sex, followers_count, status'
    })
    id_ = get_user_info_response.json()['response'][0]['id']
    first_name_ = get_user_info_response.json()['response'][0]['first_name']
    last_name_ = get_user_info_response.json()['response'][0]['last_name']
    sex_ = get_user_info_response.json()['response'][0]['sex']
    status_ = get_user_info_response.json()['response'][0]['status']

    first_data_collected_list = [id_, sex_, first_name_, last_name_, status_]
    return first_data_collected_list


# _______________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________
# ----------------------------------== FILLING DATABASE TABLE candidates ==-------------------------------------
@decorator_with_way_to_file(file_name='logs.log')
def filling_candidates_table(main_user_id=main_session_user_id):
    second_data_collected_list = []
    for candidate_id in get_list_with_liked_candidates():
        begin_url = 'https://vk.com/'
        demand_url = urljoin(api_base_url, 'users.get')
        get_user_info_response = requests.get(demand_url, params={
            'access_token': user_api_token,
            'v': api_version,
            'user_ids': candidate_id,
            'album_id': 'profile',
            'fields': 'city, sex, followers_count, bdate'
        })
        id_ = get_user_info_response.json()['response'][0]['id']
        sex_ = get_user_info_response.json()['response'][0]['sex']
        first_name_ = get_user_info_response.json()['response'][0]['first_name']
        last_name_ = get_user_info_response.json()['response'][0]['last_name']
        link_ = urljoin(begin_url, f"id{id_}")
        referenced_main_user_id_ = main_user_id

        one_candidate_data = [id_, sex_, first_name_, last_name_, link_,
                              referenced_main_user_id_]
        second_data_collected_list.append(one_candidate_data)
    return second_data_collected_list


# _______________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________
# -----------------------------== FILLING DATABASE TABLE photos_of_candidates ==--------------------------------


first_auxiliary_list = []
second_auxiliary_list = []
third_auxiliary_list = []
final_main_list = []


@decorator_with_way_to_file(file_name='logs.log')
def filling_photos_of_candidates_table():
    """NOW WE WANT TO GET A SIMILAR LIST WITH DICTS:
    [
    {user_id: ((photo_like_count, photo_link), (photo_like_count, photo_link), (photo_like_count, photo_link))},
    {another_user_id: ((photo_like_count, photo_link), (photo_like_count, photo_link), (photo_like_count, photo_link))}
    etc...
    ]
    This variant is comfortable to further data filling in db
    LET'S DO IT IN 8 STEPS!!!!!!"""

    def from_step_1_to_step_4():
        """__________ STEP_1: let's set parameters for parse __________"""
        sorted_list_of_likes_counts = []
        for candidate_id in get_list_with_liked_candidates():
            url_for_demand = urljoin(api_base_url, 'photos.get')
            photo_count_response = requests.get(url_for_demand, params={
                'access_token': user_api_token,
                'v': api_version,
                'owner_id': candidate_id,
                'album_id': 'profile',
                'extended': 1
            })

            # ____ STEP_2: before any iteration we need know amount of iterations; counter_of_elements will help us ____
            counter_of_elements = 0
            list_with_counts_of_photo_likes = []
            for element in photo_count_response.json()['response']['items']:
                counter_of_elements += 1

            # __________ STEP_3: let's create separate list with top-3 max counts of photo likes __________
            for index_ in range(counter_of_elements):
                count_of_likes_on_photo = photo_count_response.json()['response']['items'][index_]['likes']['count']
                list_with_counts_of_photo_likes.append(count_of_likes_on_photo)
                sorted_list_of_likes_counts = sorted(list_with_counts_of_photo_likes, reverse=True)[:3]

            # __________ STEP_4: let's choose photos from top-3 max counts of photo likes __________
            for item in range(counter_of_elements):
                album = photo_count_response.json()['response']['items']
                count_of_photo_ = photo_count_response.json()['response']['items'][item]['likes']['count']
                if 'photo_2560' in album[item] and count_of_photo_ in sorted_list_of_likes_counts:
                    first_auxiliary_list.append((album[item], count_of_photo_))
                elif 'photo_1280' in album[item] and count_of_photo_ in sorted_list_of_likes_counts:
                    first_auxiliary_list.append((album[item], count_of_photo_))
                elif 'photo_807' in album[item] and count_of_photo_ in sorted_list_of_likes_counts:
                    first_auxiliary_list.append((album[item], count_of_photo_))
                elif 'photo_604' in album[item] and count_of_photo_ in sorted_list_of_likes_counts:
                    first_auxiliary_list.append((album[item], count_of_photo_))
                elif 'photo_130' in album[item] and count_of_photo_ in sorted_list_of_likes_counts:
                    first_auxiliary_list.append((album[item], count_of_photo_))
                elif 'photo_75' in album[item] and count_of_photo_ in sorted_list_of_likes_counts:
                    first_auxiliary_list.append((album[item], count_of_photo_))
        return first_auxiliary_list

        # __________ STEP_5: let's remain from that photos only variants with the best quality __________

    def from_step_5_to_step_8():
        for item_ in from_step_1_to_step_4():
            if 'photo_2560' in item_[0]:
                second_auxiliary_list.append({item_[0]['owner_id']: (item_[1], item_[0]['photo_2560'])})
            elif 'photo_1280' in item_[0]:
                second_auxiliary_list.append({item_[0]['owner_id']: (item_[1], item_[0]['photo_1280'])})
            elif 'photo_807' in item_[0]:
                second_auxiliary_list.append({item_[0]['owner_id']: (item_[1], item_[0]['photo_807'])})
            elif 'photo_604' in item_[0]:
                second_auxiliary_list.append({item_[0]['owner_id']: (item_[1], item_[0]['photo_604'])})
            elif 'photo_130' in item_[0]:
                second_auxiliary_list.append({item_[0]['owner_id']: (item_[1], item_[0]['photo_130'])})
            elif 'photo_75' in item_[0]:
                second_auxiliary_list.append({item_[0]['owner_id']: (item_[1], item_[0]['photo_75'])})

        # __________ STEP_6: Now we can have extra entities in top-3 because some photos can have the same amount of
        # likes. And we want to get rid of them, and have only 3 photos in top-3, no more __________
        def getting_rid_of_extra_entities():
            counter = []
            counter2 = []
            upgrade_second_auxiliary_list = []

            for dct in second_auxiliary_list:
                for k, v in dct.items():
                    tuple_with_nested_tuple = ((k, v[0]), v[1])
                    counter.append(tuple_with_nested_tuple)

            for tpl_with_nested_tuple in counter:
                if not tpl_with_nested_tuple[0] in [tuple_[0] for tuple_ in counter2]:
                    counter2.append(tpl_with_nested_tuple)

            for tpl in counter2:
                x = tpl[0][0]
                y = tpl[0][1]
                z = tpl[1]
                upgrade_second_auxiliary_list.append({x: (y, z)})
            return upgrade_second_auxiliary_list

        # __________ STEP_7: let's split our list by 3 indexes. It will be needed for the next step while union of dicts
        # with the same keys, because the task demands exactly 3 photo for each candidate __________
        try:
            for i in range(0, len(getting_rid_of_extra_entities()), 3):
                a = [getting_rid_of_extra_entities()[i], getting_rid_of_extra_entities()[i + 1],
                     getting_rid_of_extra_entities()[i + 2]]
                third_auxiliary_list.append(a)
        except IndexError:
            print('')

        # __________ STEP_8: creating function for union dicts with the same keys; and using this function__________
        @decorator_with_way_to_file(file_name='logs.log')
        def merge_dict(dict1, dict2, dict3):
            """Merge dictionaries and keep values of common keys in list"""
            final_dict = {**dict1, **dict2, **dict3}
            for key, value in final_dict.items():
                if key in dict1 and key in dict2 and key in dict3:
                    final_dict[key] = (dict1[key], value, dict2[key])
            return final_dict

        for i in third_auxiliary_list:
            final_main_list.append(merge_dict(i[0], i[1], i[2]))
        return final_main_list

    return from_step_5_to_step_8()

# _______________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________
