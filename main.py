import random

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command
from config import token

API_TOKEN = token

bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()
ATTEMPTS = 5


users = {}


def give_random_num() -> int:
    return random.randint(1, 100)


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message) -> None:
    await message.answer('Играем в игру "угадай число". Чтобы ознакомиться с правилами, введи "/help\n'
                         'Чтобы начать, напиши ченить положительно-утвертидельное в чат\n'
                         'чтобы отказаться, как-нибудь обозначь отказ')
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': 0,
                                       'attempts': 0,
                                       'total_games': 0,
                                       'wins': 0}

    print(message.from_user.username)


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message) -> None:
    await message.answer(f'Правила просты: я загадаю число, а у тебя будет {ATTEMPTS} попыток его угадать.\n'
                         ' При неправильном ответе, я буду давать подсказки')


@dp.message(Command(commands=['finish']))
async def process_finish_command(message: Message) -> None:
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        users[message.from_user.id]['total_games'] += 1
        users[message.from_user.id]['attempts'] = -1
        await message.answer('Игра успешно завершена')
    else:
        await message.answer('Ты еще не в игре, завершать просто нечего. Это что, был тест фенкционала?')


@dp.message(Command(commands=['stats']))
async def process_stat_command(message: Message) -> None:
    if users[message.from_user.id]['total_games']:
        await message.answer(f"Всего игр сыграно: {users[message.from_user.id]['total_games']}\n"
                             f"Всего побед: {users[message.from_user.id]['total_wins']}")
    else:
        await message.answer('Откуда взяться статистике, если ты еще не играл?')


@dp.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра',
                       'Играть', 'Хочу играть'], ignore_case=True))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(f'Игра началась, число загадано, у тебя {ATTEMPTS} попыток')
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = give_random_num()
        users[message.from_user.id]['attempts'] = ATTEMPTS
    else:
        await message.answer(f'Мы не в игре, что значит это твое "{message.text}"?')


@dp.message(Text(text=['Нет', 'Не', 'Не хочу', 'Не буду'], ignore_case=True))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто '
                             'напишите об этом')
    else:
        await message.answer('Мы в игре, присылай число. Если хочешь выйти из игры, пиши "/finish"')


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer('Прямое попадание в загаданное число. Сыгрваем еще?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer('Число меньше')
            users[message.from_user.id]['attempts'] -= 1
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            await message.answer('Число больше')
            users[message.from_user.id]['attempts'] -= 1

        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(f'Попытки кончились '
                                 f'ТЫ проиграл :(\n\nМое число '
                                 f'было {users[message.from_user.id]["secret_number"]}\n\n'
                                 f'Сыграем еще?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


@dp.message()
async def process_other_text_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Мы сейчас играем. '
                             'Пришли мне число')
    else:
        await message.answer('Я довольно ограниченный бот, давай '
                             'просто сыграем в игру?')


if __name__ == '__main__':
    dp.run_polling(bot)
