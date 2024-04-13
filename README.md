# Скрипт для записи сообщений из чата в файл

## Пример работы скрипта:

```
[13.04.2024 12:21] Установлено соединение

[13.04.2024 12:21] Eva: Бога нет, поэтому я не могу верить в него. Как и в Санта-Клауса.
[13.04.2024 12:21] Vlad: Тебе нравится имя Коко?
[13.04.2024 12:21] Eva: Да, у меня есть друг, которого зовут Этан.
[13.04.2024 12:21] Vlad: Какая у нее фамилия?
[13.04.2024 12:21] Eva: Ты имеешь в виду, какая у него фамилия?
[13.04.2024 12:21] Vlad: Какая фамилия у Карен?
[13.04.2024 12:21] Eva: Я не знаю Карен.
[13.04.2024 12:21] Соединение разорвано
```


## Запуск:

### 1. Копируем содержимое проекта себе в рабочую директорию
```
git clone https://github.com/MaksAnikeev/asincio_secret_chat.git
```
- listen-minechat.py - этот скрипт, который запускает сохранение сообщений из выбранного чата

### 2. Устанавливаем библиотеки:
```
pip install -r requirements.txt
```

### 3. Для хранения переменных окружения создаем файл .env:
```
touch .env
```
Записываем в .env адрес чата, с которого будем брать сообщения, порт и папку/файл,
в которой будет сохранятся переписка:
```pycon
HOST='minechat.dvmn.org'
PORT=5000
HISTORY_FILE="chat.txt"
```
Можно не создавать файл `.env`, а указать переменные окружения при запуске скрипта в командной строке
```pycon
python listen-minechat.py -host minechat.dvmn.org -port 5000 -history_file chat.txt
```
### 4. Запуск

Запускаем файл `listen-minechat.py` с указанием переменных окружения, или без них, тогда будут выставлены
переменные окружения по умолчанию (указаны выше):
```pycon
python listen-minechat.py
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).