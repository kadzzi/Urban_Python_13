import asyncio


SPEED_FACTOR = 0.5
ATHLETES = {
    'Pasha': 3,
    'Denis': 4,
    'Apollon': 5
}
BALLS_COUNT = 5


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнование.')
    for ball in range(BALLS_COUNT):
        await asyncio.sleep(SPEED_FACTOR * power)
        print(f'Силач {name} поднял {ball + 1} шар')
    print(f'Силач {name} закончил соревнование.')


async def start_tournament():
    tasks = []
    for name, power in ATHLETES.items():
        tasks.append(asyncio.create_task(start_strongman(name, power)))
    for task in tasks:
        await task

asyncio.run(start_tournament())
