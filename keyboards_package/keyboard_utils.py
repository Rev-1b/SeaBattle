from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

# -------------------------------First keyboard creation----------------------------------------------------------------
_start_button = InlineKeyboardButton(text=LEXICON_RU['start_button_text'],
                                     callback_data='start_button_pressed')
start_keyboard = InlineKeyboardMarkup(inline_keyboard=[[_start_button]])

# ---------------------------------Choose Pole Type keyboard creation --------------------------------------------------

_start_choose_process_button = InlineKeyboardButton(text=LEXICON_RU['chose_pole_type_notification'],
                                                    callback_data='start_choose_process_button_pressed')

choose_pole_type_keyboard = InlineKeyboardMarkup(inline_keyboard=[[_start_choose_process_button]])

# -----------------------------------Next pole type keyboard creation---------------------------------------------------

_next_button = InlineKeyboardButton(text=LEXICON_RU['next_button_text'],
                                    callback_data='next_button_pressed')

next_keyboard_option = InlineKeyboardMarkup(inline_keyboard=[[_next_button], [_start_button]])

# -----------------------------Placement keyboard creation--------------------------------------------------------------
_auto_placement_button = InlineKeyboardButton(text=LEXICON_RU['placement_button_text'],
                                              callback_data='auto_placement_button_pressed')

placement_keyboard = InlineKeyboardMarkup(inline_keyboard=[[_auto_placement_button]])

# ----------------------------Main keyboard creation(letters/numbers)---------------------------------------------------
_change_to_player_pole_button = InlineKeyboardButton(text=LEXICON_RU['change_to_player_button_text'],
                                                     callback_data='change_to_player_pole_button_pressed')

_letter_buttons = [InlineKeyboardButton(text=symb, callback_data=f'{symb}_symb_pressed') for symb in 'ABCDEFGHIJ']

main_letter_keyboard = InlineKeyboardBuilder()
main_letter_keyboard.add(_change_to_player_pole_button)
main_letter_keyboard = main_letter_keyboard.row(*_letter_buttons, width=5).as_markup()

number_buttons = [InlineKeyboardButton(text=num, callback_data=f'{num}_numb_pressed') for num in range(1, 11)]

main_number_keyboard = InlineKeyboardBuilder()
main_number_keyboard.add(_change_to_player_pole_button)
main_number_keyboard = main_number_keyboard.row(*number_buttons, width=5).as_markup()

# --------------------------------Side keyboard creation----------------------------------------------------------------
_change_to_bot_pole_button = InlineKeyboardButton(text=LEXICON_RU['change_to_bot_button_text'],
                                                  callback_data='change_to_bot_pole_button_pressed')

side_keyboard = InlineKeyboardMarkup(inline_keyboard=[[_change_to_bot_pole_button]])

# -----------------------------Reselect coordinates keyboard creation---------------------------------------------------

_reselect_coordinates_button = InlineKeyboardButton(text=LEXICON_RU['reselect_coordinates_button'],
                                                    callback_data='reselect_button_pressed')

reselect_coordinates_keyboard = InlineKeyboardMarkup(inline_keyboard=[[_reselect_coordinates_button]])

# --------------------------------------------Empty keyboard------------------------------------------------------------

empty_keyboard = InlineKeyboardMarkup(inline_keyboard=[[]])



