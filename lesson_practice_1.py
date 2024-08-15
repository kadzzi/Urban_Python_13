import asyncio
import time


async def notification():
    time.sleep(10)
    print('До доставки осталось 10 минут')


async def main():
    task = asyncio.create_task(notification())
    print('Собираемся в поездку')
    print('Едим')


asyncio.run(main())
