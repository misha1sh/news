<h1 align="center">Vue Baremetrics Calendar</h1>

Данный проект сделан для хакатона **MORE.Tech VTB**

## Команда разработчиков:

   [Шестаков Михаил](https://github.com/misha1sh)
  
   [Леднев Тимофей](https://github.com/tlmon)
  
   [Пашенцев Егор](https://github.com/eapashentsev)
  
   [Ковалева Вероника](https://github.com/lverafail)
  
   Лысенко Всеволод
  
---
## How to launch

В корне проекта находится два файла:

- **parser.sh**
 
- **run.sh**
 
parser.sh при запуске обновляет данные статей в папке data
run.sh запускает Flask-сервер на порте 8080
После его запуска можно пользоваться методами REST API, описанными в документации
Данные файлы установят нужные зависимости для Python
Обновление данных статей может занимать от 10 до 30 минут, поэтому в папке дата есть уже актуальные статьи

sudo bash ./parser.sh
sudo bash ./run.sh

## How 

