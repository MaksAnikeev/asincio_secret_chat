import asyncio

async def get_chat_stream():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5000)
    n = 0
    while n < 10:
        data = await reader.readline()
        print(data.decode(), end="")
        n += 1
    writer.close()
    await writer.wait_closed()

asyncio.run(get_chat_stream())
