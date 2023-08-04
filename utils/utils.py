from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Нажать для полного перезапуска!'),
        BotCommand(command='/rules',
                   description='Правила игры.'),
        BotCommand(command='/finish',
                   description='Закончить игру.')]
    await bot.set_my_commands(main_menu_commands)


def translate_letter_to_number(letter: str) -> int:
    dictionary = {'A': 0,
                  'B': 1,
                  'C': 2,
                  'D': 3,
                  'E': 4,
                  'F': 5,
                  'G': 6,
                  'H': 7,
                  'I': 8,
                  'J': 9}

    return dictionary[letter]