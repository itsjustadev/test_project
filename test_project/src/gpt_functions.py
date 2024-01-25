import openai
import logging

logging.basicConfig(level=logging.INFO)


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


def get_date_from_gpt(message: str):
    chat_gpt_response = ''
    prompt = '''Если пользователь указал в сообщении что-то похожее на дату, то выведи ее в формате JSON, иначе выведи пустой JSON Например:
{
date_user: “7 ноября”
}'''
    try:
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'system', 'content': prompt},
                      {'role': 'user', 'content': message}]
        )
        chat_gpt_response = completion.choices[0].message.content
    except Exception as e:
        logging.error("An error occurred:", str(e), exc_info=True)
    return chat_gpt_response


def get_context_from_gpt(array_with_history):
    chat_gpt_response = ''
    try:
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=array_with_history
        )
        chat_gpt_response = completion.choices[0].message.content
    except Exception as e:
        logging.error("An error occurred:", str(e), exc_info=True)
    return chat_gpt_response
