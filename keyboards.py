from pyrogram.types import KeyboardButton, InlineKeyboardButton
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from pyrogram import emoji

btn_info = KeyboardButton(f'{emoji.INFORMATION} info')
btn_games = KeyboardButton(f'{emoji.VIDEO_GAME} Games')
btn_profile = KeyboardButton(f'{emoji.PERSON} Profile')
btn_time = KeyboardButton(f'{emoji.ONE_O_CLOCK} time')
btn_image = KeyboardButton(f'{emoji.FRAMED_PICTURE} generate image')

kb_main = ReplyKeyboardMarkup(
    keyboard=[
        [btn_info, btn_games, btn_time, btn_profile, btn_image]
    ],
    resize_keyboard=True
)

btn_rps = KeyboardButton(f'{emoji.PLAY_BUTTON} rock-paper-scissors')
btn_quest = KeyboardButton(f'{emoji.CITYSCAPE_AT_DUSK} quest')
btn_back = KeyboardButton(f'{emoji.BACK_ARROW} back')

kb_games = ReplyKeyboardMarkup(
    keyboard=[
        [btn_rps],
        [btn_quest, btn_back]
    ],
    resize_keyboard=True
)

btn_rock = KeyboardButton(f'{emoji.ROCK} rock')
btn_paper = KeyboardButton(f'{emoji.NEWSPAPER} paper')
btn_scissors = KeyboardButton(f'{emoji.SCISSORS} scissors')

kb_rps = ReplyKeyboardMarkup(
    keyboard=[
        [btn_rock, btn_paper, btn_scissors],
        [btn_back]
    ],
    resize_keyboard=True
)

inline_kb_start_quest = InlineKeyboardMarkup([
    [InlineKeyboardButton('start a quest?', callback_data='start_quest')]
])

inline_kb_1 = InlineKeyboardMarkup([
    [InlineKeyboardButton('jump off the cliff', callback_data='cliff')],
    [InlineKeyboardButton('grab an icicle', callback_data='icicle')]
])

inline_kb_fallen = InlineKeyboardMarkup([
    [InlineKeyboardButton('go explore', callback_data='explore')],
    [InlineKeyboardButton('try to climb out', callback_data='climbend')]
])

inline_kb_explore = InlineKeyboardMarkup([
    [InlineKeyboardButton('fight back', callback_data='fightflowey')],
    [InlineKeyboardButton('try to run', callback_data='floweydeath')]
])

inline_kb_toriel = InlineKeyboardMarkup([
    [InlineKeyboardButton('stay with toriel', callback_data='happy')],
    [InlineKeyboardButton('escape the house', callback_data='dungeondeath')]
])

inline_kb_glacier = InlineKeyboardMarkup([
    [InlineKeyboardButton('go deeper', callback_data='village')],
    [InlineKeyboardButton('try to climb out using the icicle', callback_data='icicleclimbend')]
])

inline_kb_village = InlineKeyboardMarkup([
    [InlineKeyboardButton('start a new life', callback_data='newlife')],
    [InlineKeyboardButton('run away from the village', callback_data='robberdeath')]
])