from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Не нажимать!'),
        BotCommand(command='/rules',
                   description='Правила игры.'),
        BotCommand(command='/finish',
                   description='Закончить игру.')]
    await bot.set_my_commands(main_menu_commands)
