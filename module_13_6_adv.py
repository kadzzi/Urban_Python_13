from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(resize_keyboard=True)
calc_button = KeyboardButton(text="Рассчитать")
info_button = KeyboardButton(text="Информация")
kb.row(calc_button, info_button)

inl_kb = InlineKeyboardMarkup()
inl_calc_button = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
inl_form_button = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
inl_kb.row(inl_calc_button, inl_form_button)

gender_kb = InlineKeyboardMarkup()
male_button = InlineKeyboardButton(text="Муж.", callback_data="male")
female_button = InlineKeyboardButton(text="Жен.", callback_data="female")
gender_kb.row(male_button, female_button)


class UserState(StatesGroup):
    gender = State()
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=kb)


@dp.message_handler(text=["Информация"])
async def get_info(message):
    await message.answer("Производится расчет оптимального числа калорий по формуле Миффлина-Сан Жеора")


@dp.message_handler(text=["Рассчитать"])
async def main_menu(message):
    await message.answer("Выбери опцию:", reply_markup=inl_kb)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("Муж.: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n"
                              + "Жен.: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_gender(call):
    await call.message.answer("Ваш пол:", reply_markup=gender_kb)
    await call.answer()
    await UserState.gender.set()


@dp.callback_query_handler(state=UserState.gender, text='male')
async def set_age_male(call, state):
    await state.update_data(gender='male')
    await call.message.answer("Введите свой возраст (полных лет):")
    await UserState.age.set()


@dp.callback_query_handler(state=UserState.gender, text='female')
async def set_age_female(call, state):
    await state.update_data(gender='female')
    await call.message.answer("Введите свой возраст (полных лет):")
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
    if data['gender'] == 'male':
        result = raw_calories + 5
        await message.answer(f"Оптимальное количество калорий: {result}")
    elif data['gender'] == 'female':
        result = raw_calories - 161
        await message.answer(f"Оптимальное количество калорий: {result}")

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
