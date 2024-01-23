import tables
from dotenv import load_dotenv
import openai
import os
import logging
from aiogram import Bot, Dispatcher, executor, types
import time

load_dotenv()
TOKEN_FOR_BOT = str(os.getenv('TOKEN_FOR_BOT'))
openai.api_key = str(os.getenv('TOKEN_FOR_CHAT_GPT'))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN_FOR_BOT)
dp = Dispatcher(bot)


def get_message_from_gpt(message: str):
    chat_gpt_response = ''
    try:
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': message}]
        )
        chat_gpt_response = completion.choices[0].message.content
    except Exception as e:
        logging.error("An error occurred:", str(e), exc_info=True)
    return chat_gpt_response


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, этот бот позволяет напрямую общаться с нейросетью chat gpt, просто напишите ваше сообщение")


@dp.message_handler()
async def echo_message(message: types.Message):
    try:
        start_time = time.time()
        user = message.from_user
        first_name = user.first_name
        last_name = user.last_name
        username = user.username
        tables.add_user(message.chat.id, username, first_name, last_name)
        gpt_answer = get_message_from_gpt(message.text)
        end_time = time.time()
        execution_time = round((end_time - start_time), 2)
        tables.add_history(message.text, str(gpt_answer), execution_time)
        await message.answer(gpt_answer)
    except Exception as e:
        logging.error("An error occurred:", str(e), exc_info=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
