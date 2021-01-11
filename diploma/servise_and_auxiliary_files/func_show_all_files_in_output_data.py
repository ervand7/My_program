import os
from pprint import pprint


def show_all_directory():
    result_list = []
    for dir_path, dir_names, file_names in os.walk("../output_data"):
        # перебрать каталоги
        for dir_name in dir_names:
            directories_names = ("Каталог:", os.path.join(dir_path, dir_name))
            result_list.append(directories_names)
        # перебрать файлы
        for filename in file_names:
            files_names = ("Файл:", os.path.join(dir_path, filename))
            result_list.append(files_names)
    return result_list


# pprint(show_all_directory())
