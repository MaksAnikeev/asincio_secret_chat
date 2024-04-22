import argparse
import asyncio
import json
from pathvalidate import replace_symbol

from environs import Env
import logging


logger = logging.getLogger(__name__)


async def register(reader, writer, nick_name):
    writer.write(f'\n{nick_name}\n'.encode())
    await writer.drain()
    messages = []
    for _ in range(3):
        data = await reader.readline()
        logger.debug(data)
        messages.append(data.decode())
    registration_message = json.loads(messages[2])
    nickname = registration_message["nickname"]
    token = registration_message["account_hash"]
    return nickname, token


async def authorise(reader, writer, token):
    writer.write(f'{token}\n'.encode())
    messages = []
    for _ in range(2):
        data = await reader.readline()
        logger.debug(data)
        messages.append(data.decode())
    return bool(json.loads(messages[1]))


async def submit_message(writer, message):
    writer.write(f'{message}\n\n'.encode())
    await writer.drain()


async def add_message_to_chat(host, port, message, nick_name=None, token=None):
    reader, writer = await asyncio.open_connection(host, port)
    try:
        if token:
            is_autorizated = await authorise(reader, writer, token)
            if is_autorizated:
                await submit_message(writer, message)
            else:
                print('Вы ввели неправильный токен, попробуйте еще раз или зарегестрируйтесь заново')
                print('Для новой регистрации токен должен быть пустым')
        else:
            nickname, token = await register(reader, writer, nick_name)
            print('Ваш ник в чате: ', nickname)
            print('Ваш токен для следующего захода в чат под этим ником: ', token)
            print(f"Запишите ваш token в .env TOKEN='{token}', \n"
                  " или используйте его при каждом следующем запуске скрипта \n"
                  f"--token {token}")

    finally:
        writer.close()
        await writer.wait_closed()


if __name__ == "__main__":
    env = Env()
    env.read_env()

    logging.basicConfig(
        format="%(levelname)s:sender: %(message)s",
        level=logging.DEBUG
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        type=str,
                        help='адрес сайта',
                        default=env('HOST', 'minechat.dvmn.org'))
    parser.add_argument('--port_writer',
                        type=int,
                        help='порт',
                        default=env('PORT_WRITER', 5050))
    parser.add_argument('message',
                        type=str,
                        help='сообщение для отправки в чат')
    parser.add_argument('--token',
                        type=str,
                        help='ваш токен от предыдущей регистрации',
                        default=env('TOKEN', None))
    args = parser.parse_args()

    message = args.message.replace('\\n', '')

    if not args.token:
        nick_name = input('Введите ваше имя для новой регистрации: ')
        nick_name = replace_symbol(nick_name)
        asyncio.run(add_message_to_chat(host=args.host,
                                        port=args.port_writer,
                                        message=message,
                                        nick_name=nick_name))
    else:
        asyncio.run(add_message_to_chat(host=args.host,
                                        port=args.port_writer,
                                        message=message,
                                        token=args.token))
