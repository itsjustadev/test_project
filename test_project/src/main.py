import tables
from dotenv import load_dotenv
import openai
import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import time
from gpt_functions import *

load_dotenv()
TOKEN_FOR_BOT = str(os.getenv('TOKEN_FOR_BOT'))
openai.api_key = str(os.getenv('TOKEN_FOR_CHAT_GPT'))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN_FOR_BOT)
dp = Dispatcher(bot, storage=MemoryStorage())
history = {}


class MyStates(StatesGroup):
    date = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if not history.get(message.chat.id):
        history[message.chat.id] = []
    await message.reply("Привет, этот бот позволяет напрямую общаться с нейросетью chat gpt, просто напишите ваше сообщение или отправьте /date чтобы достать дату из последующего сообщения")


@dp.message_handler(commands=['date'])
async def prepare_date(message: types.Message):
    await message.reply("Отправьте сообщение содержащее дату и получите json в ответ")
    await MyStates.date.set()


@dp.message_handler(state=MyStates.date)
async def complete_date(message: types.Message, state: FSMContext):
    gpt_answer = get_date_from_gpt(message.text)
    await message.reply(gpt_answer)
    print(gpt_answer)
    await state.finish()


@dp.message_handler()
async def echo_message(message: types.Message):
    try:
        user_history = history.get(message.chat.id)
        if not user_history or len(user_history) > 18:
            history[message.chat.id] = []
        history[message.chat.id].append(
            {'role': 'user', 'content': message.text})
        start_time = time.time()
        user = message.from_user
        first_name = user.first_name
        last_name = user.last_name
        username = user.username
        tables.add_user(message.chat.id, username, first_name, last_name)
        if not history.get(message.chat.id):
            gpt_answer = get_message_from_gpt(message.text)
        else:
            gpt_answer = get_context_from_gpt(history[message.chat.id])
        end_time = time.time()
        execution_time = round((end_time - start_time), 2)
        tables.add_history(message.text, str(gpt_answer), execution_time)
        history[message.chat.id].append(
            {'role': 'assistant', 'content': str(gpt_answer)})
        await message.answer(gpt_answer)
    except Exception as e:
        logging.error("An error occurred:", str(e), exc_info=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
