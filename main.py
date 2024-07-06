import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers.callback_user_panel import router_user_panel
from handlers.command_handler import router_handlers
from handlers.callback_admin_panel import router_admin_panel

load_dotenv('.env')
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router_user_panel)
    dp.include_router(router_handlers)
    dp.include_routers(router_admin_panel)
    await bot.delete_webhook(drop_pending_updates = True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен')