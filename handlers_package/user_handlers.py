from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon_ru import LEXICON_RU
from keyboards_package.keyboard_utils import (start_keyboard, placement_keyboard, main_letter_keyboard,
                                              main_number_keyboard, side_keyboard, reselect_coordinates_keyboard,
                                              empty_keyboard)

from utils.seabattle import (show_game_pole, place_ships, modify_game_pole, verify_shot_coordinates,
                             translate_letter_to_number, shoot, give_random_coords, is_game_finished)
from states.states import users, user_registration
from time import sleep

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    if users.get(message.from_user.id) is None:
        user_registration(message.from_user.id)
        await message.answer(text=LEXICON_RU['/start'], reply_markup=start_keyboard)
    else:
        await message.answer(text=LEXICON_RU['start_error'])  # Условий недостаточно! Добавить проверку на статус игры!!


@router.message(Command(commands=['rules']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/rules'])


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


@router.callback_query(Text(text='start_button_pressed'))
async def process_start_button(callback: CallbackQuery):
    user_registration(callback.from_user.id)
    game_pole = users[callback.from_user.id].user_game_pole
    str_game_pole = show_game_pole(game_pole, is_player=True)
    await callback.message.edit_text(text=str_game_pole,
                                     reply_markup=placement_keyboard)


@router.callback_query(Text(text='auto_placement_button_pressed'))
async def process_auto_placement_button(callback: CallbackQuery):
    user_ship_list = users[callback.from_user.id].user_ship_list
    place_ships(user_ship_list)

    bot_ship_list = users[callback.from_user.id].bot_ship_list
    place_ships(bot_ship_list)

    user_game_pole = users[callback.from_user.id].user_game_pole
    bot_game_pole = users[callback.from_user.id].bot_game_pole

    modify_game_pole(user_game_pole, user_ship_list)
    modify_game_pole(bot_game_pole, bot_ship_list)

    str_user_game_pole = show_game_pole(user_game_pole, is_player=True)
    await callback.message.edit_text(text=str_user_game_pole,
                                     reply_markup=side_keyboard)


@router.callback_query(Text(text='change_to_player_pole_button_pressed'))
async def process_change_to_player_button(callback: CallbackQuery):
    user_game_pole = users[callback.from_user.id].user_game_pole
    str_user_game_pole = show_game_pole(user_game_pole, is_player=True)

    await callback.message.edit_text(text=str_user_game_pole,
                                     reply_markup=side_keyboard)


@router.callback_query(Text(text=('change_to_bot_pole_button_pressed', 'reselect_button_pressed')))
async def process_bot_pole_button_pressed(callback: CallbackQuery):
    bot_game_pole = users[callback.from_user.id].bot_game_pole

    str_bot_game_pole = show_game_pole(bot_game_pole)
    str_bot_game_pole = str_bot_game_pole + '\n\nВыберите координаты выстрела:'

    keyboard = main_number_keyboard if users[callback.from_user.id].shot_coordinates else main_letter_keyboard

    await callback.message.edit_text(text=str_bot_game_pole,
                                     reply_markup=keyboard)


@router.callback_query(Text(endswith='_symb_pressed'))
async def process_any_symbol_pressed(callback: CallbackQuery):
    first_coordinate = translate_letter_to_number(callback.data.split('_')[0])
    users[callback.from_user.id].shot_coordinates.append(first_coordinate)

    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=main_number_keyboard)


@router.callback_query(Text(endswith='_numb_pressed'))
async def process_any_number_pressed(callback: CallbackQuery):
    users[callback.from_user.id].shot_coordinates.append(int(callback.data.split('_')[0]) - 1)

    user_game_pole = users[callback.from_user.id].user_game_pole
    user_ship_list = users[callback.from_user.id].user_ship_list
    user_shot_coordinates = users[callback.from_user.id].shot_coordinates

    bot_game_pole = users[callback.from_user.id].bot_game_pole
    bot_ship_list = users[callback.from_user.id].bot_ship_list
    print(show_game_pole(bot_game_pole, True))

    if verify_shot_coordinates(bot_game_pole, user_shot_coordinates):
        await callback.answer(text=LEXICON_RU['wrong_coordinates_selected'], show_alert=True)

        users[callback.from_user.id].shot_coordinates = []

        await callback.message.edit_text(text=callback.message.text,
                                         reply_markup=reselect_coordinates_keyboard)
    else:
        is_hit = shoot(bot_game_pole, bot_ship_list, user_shot_coordinates)

        if is_hit:
            users[callback.from_user.id].shot_coordinates = []
            str_bot_game_pole = show_game_pole(bot_game_pole)

            if is_game_finished(bot_ship_list):
                await callback.message.edit_text(text=LEXICON_RU['player_win'],
                                                 reply_markup=start_keyboard)
            else:
                await callback.message.edit_text(text=str_bot_game_pole,
                                                 reply_markup=main_letter_keyboard)
        else:
            users[callback.from_user.id].shot_coordinates = []
            str_bot_game_pole = show_game_pole(bot_game_pole, is_player=False)
            await callback.message.edit_text(text=str_bot_game_pole,
                                             reply_markup=callback.message.reply_markup)
            sleep(0.5)

            str_player_game_pole = show_game_pole(user_game_pole, is_player=True)
            await callback.message.edit_text(text=str_player_game_pole,
                                             reply_markup=empty_keyboard)

            sleep(0.5)

            bot_shot_coords = give_random_coords(user_game_pole)
            is_bot_hit = shoot(user_game_pole, user_ship_list, bot_shot_coords)

            while is_bot_hit:
                str_player_game_pole = show_game_pole(user_game_pole, is_player=True)
                await callback.message.edit_text(text=str_player_game_pole)

                bot_shot_coords = give_random_coords(user_game_pole)
                is_bot_hit = shoot(user_game_pole, user_ship_list, bot_shot_coords)

                sleep(0.5)

            str_player_game_pole = show_game_pole(user_game_pole, is_player=True)
            await callback.message.edit_text(text=str_player_game_pole,
                                             reply_markup=side_keyboard)


@router.message()
async def process_unexpected_input(message: Message):
    await message.answer(text=LEXICON_RU['wrong_input'])














