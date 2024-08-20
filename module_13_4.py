from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


api = '7040296994:AAGNK1uv_a7nruCtHZEkQ8aUv6tmxbOgRsA'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text=['Calories'])
async def set_gender(message):
    await message.answer("Введите свой пол [м/ж]:")
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender, text=['М', 'м', 'Ж', 'ж'])
async def set_age(message, state):
    await state.update_data(gender=message.text)
    await message.answer("Введите свой возраст (полных лет):")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост (см.):")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес (кг.):")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    raw_calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age'])
    if data['gender'].lower() == 'м':
        result = raw_calories + 5
        await message.answer(f"Оптимальное количество калорий для вас: {result}")
    elif data['gender'].lower() == 'ж':
        result = raw_calories - 161
        await message.answer(f"Оптимальное количество калорий для вас: {result}")

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
