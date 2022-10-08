<h1 align="center">Рекомендательная система новостей</h1>

Данный проект сделан для хакатона **MORE.Tech VTB**

Данный WEB-API сервис позволяет получать тренды и инсайты, на основе опубликованных новостей в популярных бизнес источниках (РБК, CFO, Klerk.ru, Consultant)

Формировать дайджесты для клиентов банка ВТБ, в зависимости от их профиля, т.е. профессии клиента 

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
 
### parser.sh
---
parser.sh при запуске обновляет данные статей в папке ./data

### run.sh
---
run.sh запускает Flask-сервер на порте 8080

После запуска run.sh можно пользоваться методами REST API, описанными в документации ниже

---

При запуске данные файлы установят нужные зависимости для Python

--Warning!--
Обновление данных статей может занимать от 10 до 30 минут, поэтому в папке дата есть уже актуальные статьи**

sudo bash ./parser.sh
sudo bash ./run.sh

## How 
