# My chat bot program!
### Программа для знакомств людей во ВКонтакте.
![Bootstrap](https://i0.wp.com/citeia.com/wp-content/uploads/2019/09/a-complete-guide-to-chatbot-development-from-tools-to-best-practices-featured.jpg?resize=780%2C470&ssl=1)

### Инструкция.
___
1. Скачайте себе на локальную машину этот репозиторий и откройте загруженную папку в вашем IDE. Примечание: я весь проект разрабатывал в PyCharm.
2. Установите зависимости (содержимое файла requirements.txt). Примечание: PyCharm мне при открытии папки сам предложил автоматически создать виртуальное окружение и загрузить туда зависимости. Мне оставалось только нажать "Ok".
3. Этим этапом мы создаем базу данных конкретно для этой программы. Установите 'pgadmin4-4.23' и создайте суперпользователя postgres. Откройте Терминал и поочередно введите следующие команды. Примечание: В зависимости от операционной системы Терминал может просить ввода пароля владельца ПК после некоторых нижепредставленных команд. Итак, введите поочередно:
    * postgres -V
    * pg_ctl -D /usr/local/var/postgres start (Внимание! Эта команда только для MAC OS)
    * psql -U postgres
    * create user ingenious_db_user with password 'ingenious_db_user';
    * create database ingenious_db with owner ingenious_db_user;
    * \q
    * psql -U ingenious_db_user -d ingenious_db
    * Вставьте в Терминал содержимое файла 'queries.sql' и нажмите Enter. Этот файл находится по пути diploma -> db -> schemas_and_create_queries -> create queries.sql
4. Откройте папку 'diploma', а в ней файл input_data. Заполните:

    * **user_api_token** - токен юзера ВКонтакте;
    * **TOKEN_FOR_BOT** - токен сообщества ВКонтакте;
    * **your_id** - ваш id ВКонтакте. 
    
5. В той же директории откройте файл 'main' и запустите его. Через секунду вы можете в вашем IDE на экране вывода информации увидеть, что таблица БД main_user заполнилась. 
    
6. Перейдите на сайт ВКонтакте и начните общение с ботом в вашей группе со слова 'привет' и нажмите Enter. Для более полноценного использования возможностей программы, ознакомьтесь ограничениями, прописанными в колонке этого README.md, которая называется "Ограничения в программе".
    
7. Для завершения программы и сохранения данных в БД напишите боту 'готово' и нажмите Enter.
    
8. После завершения программы запустите файл 'json_dump.py' находящийся по пути diploma -> output_data -> json_dump.py. Это нужно для получения итогового файла 'program_result_output.json' с выгрузкой из БД, который создастся и будет находиться по пути diploma -> output_data -> program_result_output.json.
    
9. После завершения программы в корневой папке проекта будет находиться log-файл 'logs.log', вы так же можете его посмотреть. Кроме того, файлы-логи будут находиться и в некоторых других папках. 

10. Протестируйте программу с помощью тестов, находящихся по пути diploma -> test -> test_pytest.py. Примечание: некоторые тесты могут выдавать в разное время ошибочные результаты, так как в качестве аргументов там представлены id реальных пользователей вконтаке, которые, возможно, могут удалить свою страницу, либо их могут заблокировать и тп.

11. Вы также по завершении программы можете проверить БД select-запросами. Данный файл, уже подготовленный для запуска, находится по пути diploma -> db -> checking_db_(select) -> db_select.py. Нужно будет перед запуском просто раскомментировать нужные принты.


### Логика работы программы.
![Bootstrap](https://github.com/ervand7/My_best_summary_about_python/blob/master/summary/web_scraping/HTML/2020/logic.png?raw=true)

### Ограничения в программе.
1. Во временном файле 'repository_of_candidates_ids' во время занесения данных в БД должно быть не более 9 (включительно) id кандидатов. В противном случае мы получим исключение KeyError.

2. Для каждой сессии используется уникальный id ВКонтакте. То есть, если вы захотите воспользоваться программой больше одного раза, вам нужно будет вставить в файле 'input_data' в колонку 'your_id' новый уникальный id ВКонтакте. Это установленное требование спроектированной мною базы данных. В противном случае вам ваш IDE выведет обработку исключения sqlalchemy.exc.IntegrityError: 'Такой ID уже был. Введите новый, уникальный.'

3. Программа выдает пользователю только тех кандидатов, у которых:
    * открытый аккаунт;
    * в наличии не менее 3 фотографий категории 'profile';
    * максимальный рейтинг во ВКонтакте.

4. При повторном поиске по уже ранее заданным в текущей сессии параметрам бот не будет выводить пользователю кандидатов, которых пользователь ранее уже видел. Вместо этого бот спросит у пользователя, показывать ли еще новых кандидатов по этим параметрам. Если бот получит положительный ответ, то он выведет пользователю новых кандидатов.

5. При длительном использовании программы библиотека vk_api, на основе которой работает наш бот, выдаст исключение "vk_api.exceptions.ApiError: [9] Flood control: too much messages sent to user".

6. При слабом интернете, либо, если после начала работы вы оставили программу на долгое время в бездействии, библиотека vk_api выдаст исключение HTTPConnectionError.

7. Необходимо следовать строгому синтаксису запросов, предлагаемых ботом для общения с ним. В противном случае бот выдает текст: "Дружище, попади правильно по клавиатуре :-(".

8. Время ответа бота на пользовательские запросы составляет несколько секунд. Это, в первую очередь, зависит от скорости работы интернета. В тех случаях, когда боту нужно длительное время, он предупреждает об этом.

9. Добавлять людей в черный список своего аккаунта и удалять оттуда этих людей пользователь может до того, как в первый раз кого-либо занесет в список понравившихся.

10. Пользователь может в любое время работы программы добавлять кандидатов в список понравившихся и удалять их из него. Все это до того момента, как пользователь наберет слово 'готово', нажмет Enter, и программа завершится.
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


 
