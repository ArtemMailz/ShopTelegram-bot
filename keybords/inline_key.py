from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

menu_type = InlineKeyboardMarkup(inline_keyboard =
  [
    [InlineKeyboardButton(text = 'Наш канал⭐', url = 'https://')],
    [InlineKeyboardButton(text = 'Мои заказы🛒', callback_data = 'my_order')],
    [InlineKeyboardButton(text = 'Каталог✏️', callback_data = 'catalog_chapters')],
    [InlineKeyboardButton(text = 'Обратиться в тех. поддержку✅', callback_data = 'texpod')]
  ])

help_type = InlineKeyboardMarkup(inline_keyboard = 
  [
    [InlineKeyboardButton(text = 'Как сделать заказ📝', callback_data = 'callback_1')],
    [InlineKeyboardButton(text = 'Что можно заказать🧩', callback_data = 'callback_2')],
    [InlineKeyboardButton(text = 'Как доставляем📬', callback_data = 'callback_3')],
    [InlineKeyboardButton(text = 'Сотрудничество✒️', callback_data = 'callback_4')]
  ])

admin_type = InlineKeyboardMarkup(inline_keyboard =
  [
    [InlineKeyboardButton(text = 'Да✅', callback_data = 'open_admin_panel')],
    [InlineKeyboardButton(text = 'Нет❌', callback_data = 'close_admin_panel')]
  ])

admin_panel = InlineKeyboardMarkup(inline_keyboard = [
  [InlineKeyboardButton(text = 'Добавить позицию', callback_data = 'add_position')],
  [InlineKeyboardButton(text = 'Удалить позицию', callback_data = 'delet_position')],
  [InlineKeyboardButton(text = 'Изменить позицию', callback_data = 'update_position')],
  [InlineKeyboardButton(text = 'Добавить админа', callback_data = 'add_admin')],
  [InlineKeyboardButton(text = 'Удалить админа', callback_data = 'delet_admins')],
  [InlineKeyboardButton(text = 'Закрыть админ панель❌', callback_data = 'close_admin_panel')]
  ])

position_panel = InlineKeyboardMarkup(inline_keyboard=  [
  [InlineKeyboardButton(text = 'Микрозелень', callback_data = 'microgreen'),
  InlineKeyboardButton(text = 'Проростки', callback_data = 'prorostki')],
  [InlineKeyboardButton(text = 'Сьедобные цветы', callback_data = 'flover')],
  [InlineKeyboardButton(text = 'беби - лист', callback_data = 'bubilist')]
])

position_update_panel = InlineKeyboardMarkup(inline_keyboard=  [
  [InlineKeyboardButton(text = 'Микрозелень', callback_data = 'microgreen_update'),
  InlineKeyboardButton(text = 'Проростки', callback_data = 'prorostki_update')],
  [InlineKeyboardButton(text = 'Сьедобные цветы', callback_data = 'flover_update')],
  [InlineKeyboardButton(text = 'беби - лист', callback_data = 'bubilist_update')]
])

user_panel = InlineKeyboardMarkup(inline_keyboard = [
  [InlineKeyboardButton(text = 'Микрозелень', callback_data = 'chapter_1_catalog'),
  InlineKeyboardButton(text = 'Проростки', callback_data = 'chapter_2_catalog')],
  [InlineKeyboardButton(text = 'Сьедобные цветы', callback_data = 'chapter_3_catalog'),
  InlineKeyboardButton(text = 'Беби-лист', callback_data = 'chapter_4_catalog')],
  [InlineKeyboardButton(text = 'Вернуться в меню', callback_data = 'return_user_menu')]
])

admin_panel_new = InlineKeyboardMarkup(inline_keyboard =
  [
    [InlineKeyboardButton(text = 'Да✅', callback_data = 'open_admin_panel_new')],
    [InlineKeyboardButton(text = 'Нет❌', callback_data = 'close_admin_panel')]
  ])

update_panel = InlineKeyboardMarkup(inline_keyboard = [
  [InlineKeyboardButton(text = 'Изменить название', callback_data = 'name_update')],
  [InlineKeyboardButton(text = 'Изменить описание', callback_data = 'description_update')],
  [InlineKeyboardButton(text = 'Изменить массу', callback_data = 'mass_update')],
  [InlineKeyboardButton(text = 'Изменить цену', callback_data = 'praice_update')]
])

return_user_panel = InlineKeyboardMarkup(inline_keyboard = [
  [InlineKeyboardButton(text = 'Вернуться в меню', callback_data = 'return_user_menu')]
  ])

def create_keybord(result, result_id, create_class):
  bulder = InlineKeyboardBuilder()
  for index in range(0, len(result)):
    bulder.button(text = str(result[index]), callback_data = create_class(number_position = result_id[index]))
  bulder.adjust(2)
  return bulder.as_markup() 

def create_keybord_admin(result, result_id, create_class):
  bulder = InlineKeyboardBuilder()
  for index in range(0, len(result)):
    bulder.button(text = str(result[index]), callback_data = create_class(number_admin = result_id[index]))
  bulder.adjust(2)
  return bulder.as_markup()

def create_keybord_update(result, result_id, create_class):
  bulder = InlineKeyboardBuilder()
  for index in range(0, len(result)):
    bulder.button(text = str(result[index]), callback_data = create_class(number_update_position = result_id[index]))
  bulder.adjust(2)
  return bulder.as_markup()

def create_keybord_catalog(result, result_id, create_class):
  bulder = InlineKeyboardBuilder()
  for index in range(0, len(result)):
    bulder.button(text = str(result[index]), callback_data = create_class(number_position = result_id[index]))
  bulder.adjust(2)
  bulder.button(text = 'Вернуться', callback_data = 'return_chapter_catalog')
  return bulder.as_markup()

def create_keybord_position(result_id, create_class):
  bulder = InlineKeyboardBuilder()
  bulder.button(text = 'Заказать', callback_data = create_class(number_ordering_position = result_id))
  bulder.button(text = 'Вернуться в каталог', callback_data = 'return_position_catalog')
  bulder.adjust(1)
  return bulder.as_markup()
