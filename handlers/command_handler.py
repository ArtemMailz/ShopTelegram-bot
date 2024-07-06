from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from database.orm import AsyncORMfunctin
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import keybords.inline_key as inline_key

router_handlers = Router()

@router_handlers.message(Command('start'))
async def start(message: Message):
    #await AsyncORMfunctin.create_table()
    result_id = await AsyncORMfunctin.select_id_user(message.from_user.id)
    result_admin = await AsyncORMfunctin.select_admin_stare(message.from_user.id)
    if result_id == True:
        if len(result_admin) == 0:
            await message.answer('💕Привет, в этом боте ты можешь заказать что-то', reply_markup = inline_key.menu_type)
        if len(result_admin) == 1:
            await message.answer('💕Привет, в этом боте ты можешь заказать что-то', reply_markup = inline_key.menu_type)
            await message.answer('Открыть админ панель ?', reply_markup = inline_key.admin_type)
    if result_id != True:
        await AsyncORMfunctin.init_user(message.from_user.id)
        await message.answer('💕Привет, в этом боте ты можешь заказать что-то', reply_markup = inline_key.menu_type)
        
@router_handlers.message(Command('help'))
async def help(message: Message):
    await message.answer('Что-то не понятно? Давай обьясню😉', reply_markup = inline_key.help_type)
    
@router_handlers.message(Command('admin_panel'))
async def open_admin(message: Message):
    result_admin = await AsyncORMfunctin.select_admin_stare(message.from_user.id)
    if len(result_admin) == 0:
        await message.answer('Это не для тебя команда😐')
    if len(result_admin) == 1:
        await message.answer('Открыть админ панель ?', reply_markup = inline_key.admin_type)
        
