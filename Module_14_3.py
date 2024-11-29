from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *

connection = sqlite3.connect('base.db')
cursor = connection.cursor()
#initiate_db()


api ='...'  #ввести API
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
button4 = KeyboardButton(text='Регистрация')
kb.add(button1)
kb.add(button2)
kb.add(button3)
kb.add(button4)
kb.resize_keyboard


inline_kb = InlineKeyboardMarkup()
inline_button1 = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
inline_button2 = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
inline_kb.add(inline_button1)
inline_kb.add(inline_button2)


to_buy = InlineKeyboardMarkup()
inline_buy1 = InlineKeyboardButton('Витамин 1', callback_data="product_buying")
inline_buy2 = InlineKeyboardButton('Витамин 2', callback_data="product_buying")
inline_buy3 = InlineKeyboardButton('Витамин 3', callback_data="product_buying")
inline_buy4 = InlineKeyboardButton('Витамин 4', callback_data="product_buying")
to_buy.add(inline_buy1, inline_buy2, inline_buy3, inline_buy4)


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text) == False:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email = message.text)
    await RegistrationState.age.set()
    await message.answer('Введите свой возраст:')

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age = message.text)
    user_data = await state.get_data()
    add_user(user_data["username"], user_data["email"], user_data["age"])
    await message.answer('Регистрация прошла успешно', reply_markup=kb)
    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    new_list = get_all_products()
    for i in range(0,4):
        await message.answer(f'Название: {new_list[i][1]} | Описание: {new_list[i][2]}| Цена: {new_list[i][3]}')
        with open(f'{i}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=to_buy)

@dp.callback_query_handler(text="product_buying")
async def end_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer("Этот бот поможет Вам узнать, как расчитать свою ежедневную норму каллорий,"
                         "или даже сделать это за Вас.")


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer("Выберите опцию", reply_markup=inline_kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer("Формула расчёта ля женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")


@dp.message_handler(commands=['start'])
async def start_message(message):
   await message.answer('Привет! Я бот, помогающий твоему здоровью. Начнём?', reply_markup=kb)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def et_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()
    calories = 10 * int(data['third']) + 6.25 * int(data['second']) - 5 * int(data['first']) - 161
    await message.answer(f"Ваша ежедневная норма каллорий составляет: {calories}")
    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
