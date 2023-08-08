from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery

from lexicon.lexicon_ru import LEXICON_RU
from keyboards_package.keyboard_utils import (start_keyboard, choose_pole_type_keyboard, next_keyboard_option,
                                              placement_keyboard, main_letter_keyboard, main_number_keyboard,
                                              side_keyboard, reselect_coordinates_keyboard)

from utils.seabattle import (show_game_pole, place_ships, modify_game_pole, is_cell_already_open, shoot)
from utils.bot_ai import bot_ai
from utils.classes import Coordinates
from utils.utils import translate_letter_to_number
from utils.checkers import is_game_finished

from states.states import users, user_registration, User
from time import sleep


router: Router = Router()


def define_user(handler):
    async def wrapper(message_back: CallbackQuery | Message):
        user = users[message_back.from_user.id]
        await handler(message_back, user)
    return wrapper


@router.message(CommandStart())
async def process_start_command(message: Message):
    if users.get(message.from_user.id) is None:
        user_registration(message.from_user.id)
        await message.answer(text=LEXICON_RU['/start'], reply_markup=choose_pole_type_keyboard)
    else:
        await message.answer(text=LEXICON_RU['start_error'])


@router.callback_query(Text(text=['start_choose_process_button_pressed', 'next_button_pressed']))
@define_user
async def process_choose_pole_type_button_pressed(callback: CallbackQuery, user: User):
    message_text = LEXICON_RU['chose_pole_type_head_line']
    empty_game_pole = user.user_game_pole

    user.game_pole_type += 1
    if user.game_pole_type > len(LEXICON_RU['info_line_types']):
        user.game_pole_type = 1

    variation = f'\nВариант {user.game_pole_type}:\n'
    game_pole_example = show_game_pole(game_pole=empty_game_pole,
                                       top_line=LEXICON_RU['info_line_types'][user.game_pole_type])

    message_text += f'{variation}{game_pole_example}'

    await callback.message.edit_text(text=message_text,
                                     reply_markup=next_keyboard_option)


@router.message(Command(commands=['finish']))
@define_user
async def process_finish_command(message: Message, user: User):
    if user.in_game:
        user.in_game = False
        await message.answer(text=LEXICON_RU['game_finishing'],
                             reply_markup=start_keyboard)
    else:
        await message.answer(text=LEXICON_RU['game_finish_error'])


@router.message(Command(commands=['rules']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/rules'])


@router.callback_query(Text(text='start_button_pressed'))
async def process_start_button(callback: CallbackQuery):
    user_registration(callback.from_user.id)
    user = users[callback.from_user.id]
    user.in_game = True
    game_pole = user.user_game_pole
    str_game_pole = show_game_pole(game_pole=game_pole,
                                   top_line=LEXICON_RU['info_line_types'][
                                       user.game_pole_type],
                                   is_player=True)

    await callback.message.edit_text(text=str_game_pole,
                                     reply_markup=placement_keyboard)


@router.callback_query(Text(text='auto_placement_button_pressed'))
@define_user
async def process_auto_placement_button(callback: CallbackQuery, user: User):
    place_ships(user.user_ship_list)
    place_ships(user.bot_ship_list)

    modify_game_pole(user.user_game_pole, user.user_ship_list)
    modify_game_pole(user.bot_game_pole, user.bot_ship_list)

    str_user_game_pole = show_game_pole(game_pole=user.user_game_pole,
                                        top_line=LEXICON_RU['info_line_types'][
                                            user.game_pole_type],
                                        is_player=True)

    await callback.message.edit_text(text=str_user_game_pole,
                                     reply_markup=side_keyboard)


@router.callback_query(Text(text='change_to_player_pole_button_pressed'))
@define_user
async def process_change_to_player_button(callback: CallbackQuery, user: User):
    str_user_game_pole = show_game_pole(game_pole=user.user_game_pole,
                                        top_line=LEXICON_RU['info_line_types'][
                                            user.game_pole_type],
                                        is_player=True)

    await callback.message.edit_text(text=str_user_game_pole,
                                     reply_markup=side_keyboard)


@router.callback_query(Text(text=('change_to_bot_pole_button_pressed', 'reselect_button_pressed')))
@define_user
async def process_bot_pole_button_pressed(callback: CallbackQuery, user: User):
    str_bot_game_pole = show_game_pole(game_pole=user.bot_game_pole,
                                       top_line=LEXICON_RU['info_line_types'][
                                            user.game_pole_type])

    str_bot_game_pole = str_bot_game_pole + '\n\nВыберите координаты выстрела:\n\n '

    keyboard = main_letter_keyboard if not user.shot_coordinates else main_number_keyboard

    await callback.message.edit_text(text=str_bot_game_pole,
                                     reply_markup=keyboard)


@router.callback_query(Text(endswith='_symb_pressed'))
@define_user
async def process_any_symbol_pressed(callback: CallbackQuery, user: User):
    first_coordinate = translate_letter_to_number(callback.data.split('_')[0])
    user.shot_coordinates.x = first_coordinate

    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=main_number_keyboard)


@router.callback_query(Text(endswith='_numb_pressed'))
@define_user
async def process_any_number_pressed(callback: CallbackQuery, user: User):
    user.shot_coordinates.y = int(callback.data.split('_')[0]) - 1

    if is_cell_already_open(user.bot_game_pole, user.shot_coordinates):
        await callback.answer(text=LEXICON_RU['wrong_coordinates_selected'], show_alert=True)

        user.shot_coordinates = Coordinates()

        await callback.message.edit_text(text=callback.message.text,
                                         reply_markup=reselect_coordinates_keyboard)
    else:
        shoot_output = shoot(game_pole=user.bot_game_pole,
                             ship_list=user.bot_ship_list,
                             coordinates=user.shot_coordinates)
        if shoot_output.is_hit:
            user.shot_coordinates = Coordinates()
            str_bot_game_pole = show_game_pole(game_pole=user.bot_game_pole,
                                               top_line=LEXICON_RU['info_line_types'][
                                                   user.game_pole_type])
            if is_game_finished(user.bot_ship_list):
                user.in_game = False
                await callback.message.edit_text(text=LEXICON_RU['player_win'],
                                                 reply_markup=start_keyboard)
            else:
                await callback.message.edit_text(text=str_bot_game_pole,
                                                 reply_markup=main_letter_keyboard)
        else:
            user.shot_coordinates = Coordinates()
            str_bot_game_pole = show_game_pole(game_pole=user.bot_game_pole,
                                               top_line=LEXICON_RU['info_line_types'][
                                                   user.game_pole_type],
                                               is_player=False)

            await callback.message.edit_text(text=str_bot_game_pole,
                                             reply_markup=callback.message.reply_markup)
            sleep(1)

            str_player_game_pole = show_game_pole(game_pole=user.user_game_pole,
                                                  top_line=LEXICON_RU['info_line_types'][
                                                      user.game_pole_type],
                                                  is_player=True)
            await callback.message.edit_text(text=str_player_game_pole)

            bot_strike_list = bot_ai(user=user)

            str_game_pole = ''
            sleep(2.5)

            for str_game_pole in bot_strike_list:
                await callback.message.edit_text(text=str_game_pole)

                sleep(2.5)

            if is_game_finished(user.user_ship_list):
                user.in_game = False
                await callback.message.edit_text(text=LEXICON_RU['bot_win'],
                                                 reply_markup=start_keyboard)
            else:
                await callback.message.edit_text(text=str_game_pole,
                                                 reply_markup=side_keyboard)


@router.message()
async def process_unexpected_input(message: Message):
    await message.answer(text=LEXICON_RU['wrong_input'])
