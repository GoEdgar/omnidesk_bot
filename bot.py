import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import configparser
from aiohttp import web
from urllib.parse import parse_qs as urlencoded_to_dict



config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config['tokens']['bot']

from db_helpers import *
from api_manager import ApiManager, db

InlineKeyboard = types.inline_keyboard.InlineKeyboardMarkup
InlineButton = types.inline_keyboard.InlineKeyboardButton
RemoveKeyboard = types.ReplyKeyboardRemove
ReplyKeyboard = types.ReplyKeyboardMarkup
ReplyButton = types.KeyboardButton

bot = Bot(TOKEN, parse_mode='Markdown')

dp = Dispatcher(bot)
api = ApiManager()



# def menu_btn(msg):
#     btn = ReplyKeyboard(resize_keyboard=True)
#     if db.user_ticket_count(msg.chat.id):
#         btn.insert('Написать сообщение')
#     else:
#         btn.insert('Открыть тикет')
#     return {'btn': btn}



def start_filter(msg):
    return msg.chat.type == 'private' and msg.text == '/start'


@dp.message_handler(start_filter)
async def main(msg):
    if is_new_user(msg.chat.id):
        await bot.send_message(msg.chat.id, f'Привет, *{msg.chat.first_name}*!')
    else:
        await bot.send_message(msg.chat.id, f'Оставь сообщение - мы обязательно ответим')


@dp.message_handler()
async def message(msg: types.Message):
    case_id = await api.send_message(msg)
    if case_id:
        await msg.reply(f'Тикет номер *{case_id}* создан!')
    else:
        reply_msg = await msg.reply('Доставлено')
        await asyncio.sleep(10)
        await reply_msg.delete()


async def omnidesk_msg_handler(data):
    user_id = int(data['object[custom_user_id]'][0])
    print(user_id)
    text = data['object[content]'][0]
    await bot.send_message(int(user_id), text)

routes = web.RouteTableDef()


@routes.post('/omnidesk_message')
async def change_status(request):
    if 'urlencode' in request.content_type:
        data = urlencoded_to_dict(await request.text())
        await omnidesk_msg_handler(data)
    return web.Response()

app = web.Application()
app.add_routes(routes)

loop = asyncio.get_event_loop()
loop.create_task(web._run_app(app, port=80))
executor.start_polling(dp, loop=loop)