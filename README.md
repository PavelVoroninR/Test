Тестовое задание включает в себя
1. Планы тестирования, анализ результатов небольшого тестирования, выводы ( analysis.ipynb )
2. Dockerfile - файл для создания образа, содержащего FTP сервер. Перед началом сборки необходимо перейти в
    корневой каталог проекта. Команда для сборки:
    ```bash
    docker build -t local/vsftplt:v0.3 .
    ```
3. После сборки можно запустить контейнер в интерактивном режиме:
    ```bash
    docker run --rm -it -p 9098:9098 local/vsftplt:v0.3 sh
    ```
    зайти в контейнер и запустить скрипт:
    ```bash
    sh /root/generator_scripts/fix.sh
    ```
    для исправления паролей у пользователей.
4. Запустить сервер и мониторинг командой:
    ```bash
    nohup vsftpd > /dev/null 2>&1& && nohup python3 /root/monitoring_script/monitor_script.py > /dev/null 2>&1&
    ```
5. Испытать на прочность один из самых устойчивых FTP серверов =)

Список артефактов:
- /input/*.csv - файлы данных для анализа
- /Jmeter_Test/FTP Request.jmx - тестовый план в формате Apache Jmeter
- analysis.ipynb файл блокнота Jupiter
- Dockerfile - файл для создания контейнера (билдскрипт)
- file_gen.py - генератор файлов с двоичным содержимым
- fix.sh - скрипт, который чинит пароли
- gen_users.sh - скрипт для генерации пользователей и файлов
- monitor_script.py - скрипт для создания разнообразных зондов в разных тредах. Класс ShellProbe описан в коде, и ниже имеется несколько примеров его использования.
- README.md - файл с описанием репозитория
- user_list.txt - файл со списком пользователей
