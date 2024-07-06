from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from database.orm import AsyncORMfunctin
from keybords import inline_key
from database.model import ChapterEnum
from aiogram.filters.callback_data import CallbackData

router_admin_panel = Router()

class StatePassword(StatesGroup):
    password = State()
    
class StatePosition(StatesGroup):
    name_pos = State()
    decription_pos = State()
    mass_pos = State()
    chapter_pos = State()
    praice_pos = State()
    
class StateNewAdmin(StatesGroup):
    id_new_admin = State()
    password_new_admin = State()
    name_new_user = State()
    
class StateUpdatePosition(StatesGroup):
    id_position = State()
    
    new_name_position = State()
    new_description_position = State()
    new_mass_position = State()
    new_praice_position = State()
    
class CreateNewCallbackData(CallbackData, prefix = 'position'):
    number_position: int
    
class CreateNewCallbackDataAdmin(CallbackData, prefix = 'admin'):
    number_admin: int
    
class CreateNewCallbackDataUpdate(CallbackData, prefix = 'update'):
    number_update_position: int

@router_admin_panel.callback_query(F.data == 'open_admin_panel') #открываем админ панель
async def open_admin_panel(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Введите пароль👇🏻')
    await state.set_state(StatePassword.password)
    
@router_admin_panel.callback_query(F.data == 'open_admin_panel_new') #открываем админ панель
async def open_admin_panel_new(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Админ панель открыта', reply_markup = inline_key.admin_panel)
    
@router_admin_panel.message(StatePassword.password) #принимаем и проверяем пароль
async def admin_password(message: Message, state: FSMContext):
    await state.update_data(password = message.text)
    passwords = await state.get_data()
    tru_password = await AsyncORMfunctin.select_password_user(message.from_user.id)
    await state.clear()
    if int(passwords['password']) == tru_password:
        # await message.answer('Загружаем базу данных...')
        # time.sleep(2)
        # await message.answer('Разгоняем митинги Навального...')
        # time.sleep(2)
        # await message.answer('Подметаем мавзолей...')
        # time.sleep(2)
        await message.answer('Админ панель открыта', reply_markup = inline_key.admin_panel)
    if int(passwords['password']) != tru_password:
        await state.set_state(StatePassword.password)
        await message.answer('Пароль неверный, попробуйте еще раз🐙')
        
@router_admin_panel.callback_query(F.data == 'close_admin_panel') #закрываем админ панель
async def close_admin_panel(callback: CallbackQuery):
    await callback.message.delete()
    
@router_admin_panel.callback_query(F.data == 'add_position') #добавляем новую позицию в прайс
async def add_position(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(StatePosition.name_pos)
    await callback.message.answer('Ведите название нового продукта')
    
@router_admin_panel.message(StatePosition.name_pos) #принимаем имя позиции
async def add_position_name(message: Message, state: FSMContext):
    await state.update_data(name_pos = message.text)
    rev = await state.get_data()
    await message.answer('Отлично, теперь введите описание для продукта')
    await state.set_state(StatePosition.decription_pos)
    
@router_admin_panel.message(StatePosition.decription_pos) #принимаем описание
async def add_position_description(message: Message, state: FSMContext):
    await state.update_data(decription_pos = message.text)
    await state.get_data()
    await message.answer('Принято, теперь введите массу продукта в одной порции')
    await state.set_state(StatePosition.mass_pos)
    
@router_admin_panel.message(StatePosition.mass_pos) #принимаем массу
async def add_position_mass(message: Message, state: FSMContext):
    await state.update_data(mass_pos = message.text)
    await state.get_data()
    await message.answer('Масса записана, теперь введите раздел продукта:\n\n\
Микрозелень\nПроростки\nЦветы\nБеби-лист\n\nВводите слова как они написаны, без пробелов')
    await state.set_state(StatePosition.chapter_pos)
    
@router_admin_panel.message(StatePosition.chapter_pos) #принимаем раздел
async def add_position_chapter(message: Message, state: FSMContext):
    await state.update_data(chapter_pos = message.text)
    await state.get_data()
    await message.answer('Отлично, теперь введи цену за порцию продукта')
    await state.set_state(StatePosition.praice_pos)
    
@router_admin_panel.message(StatePosition.praice_pos) #принимаем цену
async def add_position_praice(message: Message, state: FSMContext):
    await state.update_data(praice_pos = message.text)
    result = await state.get_data()
    await message.answer('Загружаем новый продукт в базу данных...')
    if result['chapter_pos'] == 'Микрозелень':
        await AsyncORMfunctin.insert_new_position(result['name_pos'], result['decription_pos'], int(result['mass_pos']), ChapterEnum.chapter_1, int(result['praice_pos']))
    if result['chapter_pos'] == 'Проростки':
        await AsyncORMfunctin.insert_new_position(result['name_pos'], result['decription_pos'], int(result['mass_pos']), ChapterEnum.chapter_2, int(result['praice_pos']))
    if result['chapter_pos'] == 'Цветы':
        await AsyncORMfunctin.insert_new_position(result['name_pos'], result['decription_pos'], int(result['mass_pos']), ChapterEnum.chapter_3, int(result['praice_pos']))
    if result['chapter_pos'] == 'Беби-лист':
        await AsyncORMfunctin.insert_new_position(result['name_pos'], result['decription_pos'], int(result['mass_pos']), ChapterEnum.chapter_4, int(result['praice_pos']))
    await state.clear()
    await message.answer('Продукт добавлен в базу👍🏿')
    await message.answer('Выполнить еще какую-то операцию ?', reply_markup = inline_key.admin_panel_new)
    
@router_admin_panel.callback_query(F.data == 'delet_position') #предлагаем типы товаров
async def delet_position(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберите необходимый тип товара', reply_markup = inline_key.position_panel)
    
@router_admin_panel.callback_query(F.data == 'microgreen') #список позиций микрозелени
async def answer_position_microgreen(callback: CallbackQuery):
    await callback.message.delete()
    result_id = await AsyncORMfunctin.select_id_position('chapter_1')
    result = await AsyncORMfunctin.select_name_position('chapter_1')
    await callback.message.answer('список позиций', reply_markup = inline_key.create_keybord(result, result_id, CreateNewCallbackData))
    
@router_admin_panel.callback_query(F.data == 'prorostki') #список позиций проростков
async def answer_position_prorostki(callback: CallbackQuery): 
    await callback.message.delete()
    result_id = await AsyncORMfunctin.select_id_position('chapter_2')
    result = await AsyncORMfunctin.select_name_position('chapter_2')
    await callback.message.answer('список позиций', reply_markup = inline_key.create_keybord(result, result_id, CreateNewCallbackData))
    
@router_admin_panel.callback_query(F.data == 'flover') #список позиций цветов
async def answer_position_flover(callback: CallbackQuery): 
    await callback.message.delete()
    result_id = await AsyncORMfunctin.select_id_position('chapter_3')
    result = await AsyncORMfunctin.select_name_position('chapter_3')
    await callback.message.answer('список позиций', reply_markup = inline_key.create_keybord(result, result_id, CreateNewCallbackData))
    
@router_admin_panel.callback_query(F.data == 'bubilist') #список позиций беби-листа
async def answer_position_dudilist(callback: CallbackQuery): 
    await callback.message.delete()
    result_id = await AsyncORMfunctin.select_id_position('chapter_4')
    result = await AsyncORMfunctin.select_name_position('chapter_4')
    await callback.message.answer('список позиций', reply_markup = inline_key.create_keybord(result, result_id, CreateNewCallbackData))
    
@router_admin_panel.callback_query(CreateNewCallbackData.filter()) #удаление позиции
async def create_new_callback_data(callback: CallbackQuery, callback_data: CreateNewCallbackData):
    await callback.message.delete()
    await AsyncORMfunctin.delete_position({callback_data.number_position})
    await callback.message.answer(f'id удаленной позиции: {callback_data.number_position}\n\nУспешно удаленна 🍒🍒🍒')
    await callback.message.answer('Выполнить еще какую-то операцию ?', reply_markup = inline_key.admin_panel_new)

@router_admin_panel.callback_query(F.data == 'update_position') #категории товаров для изменения
async def update_position(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберите категорию товара', reply_markup = inline_key.position_update_panel)

@router_admin_panel.callback_query(F.data == 'microgreen_update') #список позиций микрозелени
async def update_position_mecrogreen(callback: CallbackQuery):
    await callback.message.delete()
    result_id = await AsyncORMfunctin.select_id_position('chapter_1')
    result = await AsyncORMfunctin.select_name_position('chapter_1')
    await callback.message.answer('список позиций', reply_markup = inline_key.create_keybord_update(result, result_id, CreateNewCallbackDataUpdate))
    
@router_admin_panel.callback_query(F.data == 'prorostki_update') #список позиций проростков
async def update_position_prorostki(callback: CallbackQuery):
    await callback.message.delete()
    result_id = await AsyncORMfunctin.select_id_position('chapter_2')
    result = await AsyncORMfunctin.select_name_position('chapter_2')
    await callback.message.answer('список позиций', reply_markup = inline_key.create_keybord_update(result, result_id, CreateNewCallbackDataUpdate))
    
@router_admin_panel.callback_query(F.data == 'flover_update') #список позиций цветов
async def update_position_flover(callback: CallbackQuery):
    await callback.message.delete()
    result_id = await AsyncORMfunctin.select_id_position('chapter_3')
    result = await AsyncORMfunctin.select_name_position('chapter_3')
    await callback.message.answer('список позиций', reply_markup = inline_key.create_keybord_update(result, result_id, CreateNewCallbackDataUpdate))
    
@router_admin_panel.callback_query(F.data == 'bubilist_update') #список позиций беби-листа
async def update_position_bubilist(callback: CallbackQuery):
    await callback.message.delete()
    result_id = await AsyncORMfunctin.select_id_position('chapter_4')
    result = await AsyncORMfunctin.select_name_position('chapter_4')
    await callback.message.answer('список позиций', reply_markup = inline_key.create_keybord_update(result, result_id, CreateNewCallbackDataUpdate))
    
@router_admin_panel.callback_query(CreateNewCallbackDataUpdate.filter())
async def create_new_callback_update(callback: CallbackQuery, callback_data: CreateNewCallbackDataUpdate):
    await callback.message.delete()
    await callback.message.answer(f'id выбранной позиции: {callback_data.number_update_position}\n\nЧто необходимо в ней изменить?', reply_markup = inline_key.update_panel)
    
@router_admin_panel.callback_query(F.data == 'name_update') #изменяем имя позиции
async def update_name_position(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateUpdatePosition.id_position)
    await callback.message.answer('Хоршо, введите id позиции')
    
@router_admin_panel.message(StateUpdatePosition.id_position) #принимаем id
async def update_name_position_id(message: Message, state: FSMContext):
    await state.update_data(id_position = message.text)
    await state.get_data()
    await message.answer('теперь введите новое имя')
    await state.set_state(StateUpdatePosition.new_name_position)
    
@router_admin_panel.message(StateUpdatePosition.new_name_position) #принимаем новое имя
async def update_name_position_new_name(message: Message, state: FSMContext):
    await state.update_data(new_name_position = message.text)
    result = await state.get_data()
    await AsyncORMfunctin.update_name_position(result['id_position'], result['new_name_position'])
    await message.answer('Имя позиции успешно измененно')
    await message.answer('Выполнить еще какую-то операцию ?', reply_markup = inline_key.admin_panel_new)
    await state.clear()
    
@router_admin_panel.callback_query(F.data == 'description_update') #изменяем описание
async def update_description_position(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateUpdatePosition.id_position)
    await callback.message.answer('Хоршо, введите id позиции')
    
@router_admin_panel.message(StateUpdatePosition.id_position) #принимаем id
async def update_description_position_id(message: Message, state: FSMContext):
    await state.update_data(id_position = message.text)
    await message.answer('теперь введите новое описание товара')
    await state.set_state(StateUpdatePosition.new_description_position)
    
@router_admin_panel.message(StateUpdatePosition.new_description_position) #принимаем новое описание
async def update_description_position_new_description(message: Message, state: FSMContext):
    await state.update_data(new_description_position = message.text)
    result = await state.get_data()
    await AsyncORMfunctin.update_description_position(result['id_position'], result['new_description_position'])
    await state.clear()
    await message.answer('Описание позиции успешно измененно')
    await message.answer('Выполнить еще какую-то операцию ?', reply_markup = inline_key.admin_panel_new)
    
@router_admin_panel.callback_query(F.data == 'mass_update') #изменяем массу
async def update_mass_position(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateUpdatePosition.id_position)
    await callback.message.answer('Хоршо, введите id позиции')
    
@router_admin_panel.message(StateUpdatePosition.id_position) #принимаем id
async def update_mass_position_id(message: Message, state: FSMContext):
    await state.update_data(id_position = message.text)
    await state.get_data()
    await message.answer('теперь введите новую массу')
    await state.set_state(StateUpdatePosition.new_mass_position)
    
@router_admin_panel.message(StateUpdatePosition.new_mass_position) #принимаем новую массу
async def update_mass_position_new_mass(message: Message, state: FSMContext):
    await state.update_data(new_mass_position = message.text)
    result = await state.get_data()
    await AsyncORMfunctin.update_mass_position(result['id_position'], result['new_mass_position'])
    await state.clear()
    await message.answer('Масса позиции успешно измененно')
    await message.answer('Выполнить еще какую-то операцию ?', reply_markup = inline_key.admin_panel_new)
    
@router_admin_panel.callback_query(F.data == 'praice_update') #изменяем цену
async def update_praice_position(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateUpdatePosition.id_position)
    await callback.message.answer('Хоршо, введите id позиции')
    
@router_admin_panel.message(StateUpdatePosition.id_position) #принимаем id
async def update_praice_position_id(message: Message, state: FSMContext):
    await state.update_data(id_position = message.text)
    await state.get_data()
    await message.answer('Теперь введите новую цену')
    await state.set_state(StateUpdatePosition.new_praice_position)
    
@router_admin_panel.message(StateUpdatePosition.new_praice_position) #принимаем новую цену
async def update_praice_position_new_praice(message: Message, state: FSMContext):
    await state.update_data(new_praice_position = message.text)
    result = await state.get_data()
    await AsyncORMfunctin.update_praice_position(result['id_position'], result['new_praice_position'])
    await message.answer('Цена позиции успешно измененно')
    await message.answer('Выполнить еще какую-то операцию ?', reply_markup = inline_key.admin_panel_new)
    await state.clear()
    
@router_admin_panel.callback_query(F.data == 'add_admin') #добавляем нового админа
async def add_admins(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Для добавления нового админа введите его id\n\n\
Предварительно он должен быть зарегестрирован в боте')
    await state.set_state(StateNewAdmin.id_new_admin)
    
@router_admin_panel.message(StateNewAdmin.id_new_admin) #принимаем id нового админа
async def add_admins_id(message: Message, state: FSMContext):
    await state.update_data(id_new_admin = message.text)
    await message.answer('Good, теперь введите пароль для нового админа, он должен состоять только из чисел, не более 9 цифр')
    await state.set_state(StateNewAdmin.password_new_admin)
    
@router_admin_panel.message(StateNewAdmin.password_new_admin) #принимаем пароль для нового админа
async def add_admins_password(message: Message, state: FSMContext):
    await state.update_data(password_new_admin = message.text)
    await message.answer('Теперь придумайте прикольно имя для нового админа)')
    await state.set_state(StateNewAdmin.name_new_user)
    
@router_admin_panel.message(StateNewAdmin.name_new_user) #принимаем имя для админа
async def add_admins_name(message: Message, state: FSMContext):
    await state.update_data(name_new_user = message.text)
    result = await state.get_data()
    await state.clear()
    await AsyncORMfunctin.insert_new_admin(int(result['id_new_admin']), int(result['password_new_admin']), result['name_new_user'])
    await message.answer('Новый админ успешно добавлен', reply_markup = inline_key.admin_panel_new)
    await message.answer('Выполнить еще какую-то операцию ?', reply_markup = inline_key.admin_panel_new)
    
@router_admin_panel.callback_query(F.data == 'delet_admins') #список кнопок для удаления
async def delet_admins(callback: CallbackQuery):
    await callback.message.delete()
    result_id = await AsyncORMfunctin.select_admins_id()
    result_name = await AsyncORMfunctin.select_admins_name()
    await callback.message.answer('Выберите какого админа необходимо удалить', reply_markup = inline_key.create_keybord_admin(result_name, result_id, CreateNewCallbackDataAdmin))
    
@router_admin_panel.callback_query(CreateNewCallbackDataAdmin.filter()) #удаление админа
async def create_new_callback_data_admin(callback: CallbackQuery, callback_data: CreateNewCallbackDataAdmin):
    await callback.message.delete()
    await AsyncORMfunctin.delet_admins(callback_data.number_admin)
    await callback.message.answer(f'id удаленного админа: {callback_data.number_admin}\n\nУспешно удален 🍒🍒🍒')
    await callback.message.answer('Выполнить еще какую-то операцию ?', reply_markup = inline_key.admin_panel_new)