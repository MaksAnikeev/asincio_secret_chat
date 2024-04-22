import argparse
import asyncio
import datetime

import aiofiles
from environs import Env


async def action_with_file(name, mode, text):
    async with aiofiles.open(name, mode=mode) as file:
        await file.write(text)


async def get_chat_stream(host, port, history_file):
    reader, writer = await asyncio.open_connection(host, port)
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    first_string = f'[{now}] Установлено соединение \n'
    print(first_string)
    await action_with_file(name=history_file,
                           mode="a",
                           text=first_string)
    try:
        while True:
            try:
                data = await reader.readline()
                now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
                chat_string = f'[{now}] {data.decode()}'
                print(chat_string, end="")
                await action_with_file(name=history_file,
                                       mode="a",
                                       text=chat_string)

            except asyncio.exceptions.CancelledError:
                now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
                last_string = f'[{now}] Программа остановлена пользователем \n\n'
                await action_with_file(name="chat.txt",
                                       mode="a",
                                       text=last_string)
                print(last_string)
                break
    finally:
        now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        last_string = f'[{now}] Соединение разорвано \n\n'
        await action_with_file(name="chat.txt",
                               mode="a",
                               text=last_string)

        print(last_string)
        writer.close()
        await writer.wait_closed()




if __name__ == "__main__":
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        type=str,
                        help='адрес сайта',
                        default=env('HOST', 'minechat.dvmn.org'))
    parser.add_argument('--port',
                        type=int,
                        help='порт',
                        default=env('PORT', 5000))
    parser.add_argument('--history_file',
                        type=str,
                        help='путь и название файла для'
                             ' сохранения истории сообщений из чата',
                        default=env('HISTORY_FILE', "chat.txt"))
    args = parser.parse_args()

    asyncio.run(get_chat_stream(host=args.host,
                                port=args.port,
                                history_file=args.history_file))
