# My chat bot program!
### Программа для знакомств людей во ВКонтакте.
![Bootstrap](https://github.com/ervand7/HTML/blob/master/logic.png?raw=true)

### Инструкция.
___

1. Откройте папку 'diploma', а в ней файл input_data. Заполните:

    * **user_api_token** - токен юзера ВКонтакте. Примечание: инструкция по получению этого токена находится по пути diploma -> servise_and_auxiliary_files -> how_get_user_api_token.py;
    
    * **TOKEN_FOR_BOT** - токен сообщества ВКонтакте. Примечание: инструкция по получению этого токена находится по пути diploma -> servise_and_auxiliary_files -> how_get_TOKEN_FOR_BOT.py;
    * **your_id** - ваш id ВКонтакте. 
    
2. В той же директории откройте файл 'main' и запустите его.
    
3. Начните общение с ботом в вашей группе со слова 'привет' и нажмите Enter. Для более полноценного использования возможностей программы, ознакомьтесь ограничениями, прописанными в колонке "Ограничения в программе".
    
4. Для завершения программы и сохранения данных в БД напишите боту 'готово' и нажмите Enter.
    
5. После завершения программы запустите файл 'json_dump.py' находящийся по пути diploma -> output_data -> json_dump.py. Это нужно для получения итогового файла 'program_result_output.json' с выгрузкой из БД, который создастся и будет находиться по пути diploma -> output_data -> program_result_output.json.
    
6. После завершения программы в корневой папке проекта будет находиться log-файл 'logs.log', вы так же можете его посмотреть. Кроме того, файлы-логи будут находиться и в некоторых других папках. 

7. Протестируйте программу с помощью тестов, находящихся по пути diploma -> test -> test_pytest.py. Примечание: некоторые тесты могут выдавать в разное время ошибочные результаты, так как в качестве аргументов там представлены id реальных пользователей вконтаке, которые, возможно, могут удалить свою страницу, либо их могут заблокировать и тп.  


### Логика работы программы.
![Bootstrap](https://github.com/ervand7/HTML/blob/master/logic.png?raw=true)

### Ограничения в программе.
1. Во временном файле 'repository_of_candidates_ids' во время занесения данных в БД должно быть не более 9 (включительно) id кандидатов. В противном случае мы получим исключение KeyError.

2. Для каждой сессии используется уникальный id ВКонтакте. То есть, если вы захотите воспользоваться программой больше одного раза, вам нужно будет вставить в файле 'input_data' в колонку 'your_id' новый уникальный id ВКонтакте. Это установленное требование спроектированной мною базы данных.

3. В программу установлена минимально мною заполненная (для проверки) БД, в которую пользователь будет записывать данные и из которой будет выводить данные в json-файл. Структуру этой БД и прочую информацию о ней вы можете найти по пути diploma -> db -> schemas_and_create_queries.

4. Программа выдает пользователю только тех кандидатов, у которых:
    * открытый аккаунт;
    * в наличии не менее 3 фотографий категории 'profile';
    * максимальный рейтинг во ВКонтакте.

5. При повторном поиске по уже ранее заданным в текущей сессии параметрам бот не будет выводить пользователю кандидатов, которых пользователь ранее уже видел. Вместо этого бот спросит у пользователя, показывать ли еще новых кандидатов по этим параметрам. Если бот получит положительный ответ, то он выведет пользователю новых кандидатов.

6. При длительном использовании программы библиотека vk_api, на основе которой работает наш бот, выдаст исключение "vk_api.exceptions.ApiError: [9] Flood control: too much messages sent to user".

7. При слабом интернете, либо, если после начала работы вы оставили программу на долгое время в бездействии, библиотека vk_api выдаст исключение HTTPConnectionError.

8. Необходимо следовать строму синтаксису запросов, прдлагаемых ботом для общения с ним. В противном случае бот выдает текст: "Дружище, попади правильно по клавиатуре :-(".

9. Время ответа бота на пользовательские запросы составляет несколько секунд. Это в первую очередь зависит от скорости работы интернета. В тех случаюх, когда боту нужно длительное время, он предупреждает об этом.

10. Добавлять людей в черный список своего аккаунта и удалять оттуда этих людей пользователь может до того, как в первый раз кого-либо занесет в список понравившихся.

11. Пользователь может в любое время работы программы добавлять кандидатов в список понравившихся и удалять их из него. Все это до того момента, как пользователь наберет слово 'готово', нажмет Enter, и программа завершится.
***
## Само дипломное задание.
Используя данные из VK нужно сделать бота как Tinder. Искать людей, подходящих под условия, на основании информации о пользователе из VK:
- диапазон возраста
- пол
- город
- семейное положение


У тех людей, которые подошли по требованиям пользователю, получать топ-3 популярных фотографии с аватара. Популярность определяется по количеству лайков.

Результаты сохраняются в базу данных.
Бот должен предоставлять текстовый интерфейс для работы с пользователем.  
- уточняет предпочтения (если надо) и начинается подбор;
- если кто-то понравился - отмечает и человек заносится в БД;
- если нет - пропускает;
- вывод всех понравившихся людей;
- удалить из списка понравившихся людей человека;  
- вносить и удалять людей из черного списка.





### Требование к сервису:
1. Код программы удовлетворяет PEP8.
2. Получать токен от пользователя с нужными правами.
3. Программа декомпозирована на функции/классы/модули/пакеты.
4. База данных PostgreSQL
5. Люди не должны повторяться при повторном поиске.
6. Реализовать тесты на базовую функциональность.
7. Не запрещается использовать внешние библиотеки для vk.
8. Если используете библиотеки, не забудьте оформить requirements.txt.
9. Строки с токенами оставлять пустыми!


 
