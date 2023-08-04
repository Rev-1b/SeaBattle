import asyncio

from config_data.config import Config, load_config
from aiogram import Bot, Dispatcher
from handlers_package import user_handlers
from keyboards_package.set_menu import set_main_menu


async def main():
    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(set_main_menu)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
