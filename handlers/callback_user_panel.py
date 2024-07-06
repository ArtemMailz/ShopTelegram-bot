from aiogram import Router, F, Bot
from aiogram.types import callback_query, CallbackQuery, LabeledPrice, Message, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.orm import AsyncORMfunctin
import keybords.inline_key as inline_key
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from typing import Optional

router_user_panel = Router()

class CreateNewCallbackDataChapter(CallbackData, prefix = 'chapter'):
    number_position: int
    
class CreateNewCallbackDataPosition(CallbackData, prefix = 'position_ordering'):
    number_ordering_position: int

@router_user_panel.callback_query(F.data == 'my_order') #выдаем заказы пользователя, если они есть конечно
async def my_order(callback: CallbackQuery):
        result = await AsyncORMfunctin.select_sum_order(int(callback.from_user.id))
        if result == 0:
            await callback.message.answer('Ваша корзина пуста, вы еще не делали некаких заказов💕')
        else:
            await AsyncORMfunctin.select_order_to_user()
            await callback.message.answer('ююю')
            
@router_user_panel.callback_query(F.data == 'catalog_chapters') #даем  выбрать раздел товара
async def my_order(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберити категорию каталога которая вам необходима', reply_markup = inline_key.user_panel)
    
@router_user_panel.callback_query(F.data == 'chapter_1_catalog') #показываем первый раздел
async def my_order(callback: CallbackQuery):
    await callback.message.delete()
    result_id = await AsyncORMfunctin.select_id_position('chapter_1')
    result = await AsyncORMfunctin.select_name_position('chapter_1')
    await callback.message.answer('Каталог микрозелени', reply_markup = inline_key.create_keybord_catalog(result, result_id, CreateNewCallbackDataChapter))
    
@router_user_panel.callback_query(F.data == 'chapter_2_catalog') #показываем второй раздел
async def my_order(callback: CallbackQuery):
    await callback.message.delete()
    result_id = await AsyncORMfunctin.select_id_position('chapter_2')
    result = await AsyncORMfunctin.select_name_position('chapter_2')
    await callback.message.answer('Каталог микрозелени', reply_markup = inline_key.create_keybord_catalog(result, result_id, CreateNewCallbackDataChapter))
    
@router_user_panel.callback_query(F.data == 'chapter_3_catalog') #показываем третий раздел
async def my_order(callback: CallbackQuery):
    await callback.message.delete()
    result_id = await AsyncORMfunctin.select_id_position('chapter_3')
    result = await AsyncORMfunctin.select_name_position('chapter_3')
    await callback.message.answer('Каталог микрозелени', reply_markup = inline_key.create_keybord_catalog(result, result_id, CreateNewCallbackDataChapter))

@router_user_panel.callback_query(F.data == 'chapter_4_catalog') #показывем чётвертый раздел
async def my_order(callback: CallbackQuery):
    await callback.message.delete()
    result_id = await AsyncORMfunctin.select_id_position('chapter_4')
    result = await AsyncORMfunctin.select_name_position('chapter_4')
    await callback.message.answer('Каталог микрозелени', reply_markup = inline_key.create_keybord_catalog(result, result_id, CreateNewCallbackDataChapter))

@router_user_panel.callback_query(F.data == 'return_chapter_catalog') #откатываем к выбору раздела
async def my_order(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберити категорию каталога которая вам необходима', reply_markup = inline_key.user_panel)
    
@router_user_panel.callback_query(F.data == 'return_user_menu') #откатываем к основному меню
async def my_order(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('💕Привет, в этом боте ты можешь заказать что-то', reply_markup = inline_key.menu_type)
    
@router_user_panel.callback_query(CreateNewCallbackDataChapter.filter()) #составляем описание товара
async def create_new_callback_data(callback: CallbackQuery, callback_data: CreateNewCallbackDataChapter, bot = Bot):
    await callback.message.delete()
    result = await AsyncORMfunctin.select_full_ifo_position(callback_data.number_position)
    await callback.message.answer(f'Название товара: {result[0]}\n\nОписание: {result[1]}\nмасса продукта в порции: {result[2]}г\n\nЦена: {result[3]}р', reply_markup = inline_key.create_keybord_position(callback_data.number_position, CreateNewCallbackDataPosition))
    
@router_user_panel.callback_query(F.data == 'return_position_catalog') #Возвращаемся к выбору товара
async def my_order(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберити категорию каталога которая вам необходима', reply_markup = inline_key.user_panel)
    
@router_user_panel.callback_query(CreateNewCallbackDataPosition.filter()) #составляем описание товара
async def create_new_callback_data(callback: CallbackQuery, 
                                   callback_data: CreateNewCallbackDataPosition, bot = Bot):
    await callback.message.delete()
    result = await AsyncORMfunctin.select_full_ifo_position(callback_data.number_ordering_position)
    PRICE = LabeledPrice(label = result[0], amount = result[3]*100)
    
    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await callback.message.answer("Тестовый платеж!!!")

    await bot.send_invoice(callback.message.chat.id,
                           title = result[0],
                           description = result[1],
                           provider_token = PAYMENTS_TOKEN,
                           currency = "RUB",
                           photo_url = "https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                           photo_width = 416,
                           photo_height = 234,
                           photo_size = 416,
                           is_flexible = False,
                           prices = [PRICE],
                           start_parameter = "one-month-subscription",
                           payload = "test-invoice-payload")
    
@router_user_panel.message(F.successful_payment)
async def successful_payment(message: Message, callback_data: CreateNewCallbackDataPosition, bot = Bot):
    print("SUCCESSFUL PAYMENT:")
    await AsyncORMfunctin.insert_new_ordering(message.from_user.id, callback_data.number_ordering_position)
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
    f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно, ваш товар будет отправлен в ближайшее время", reply_markup = inline_key.return_user_panel)

