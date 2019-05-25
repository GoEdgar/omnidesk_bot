import os
import ssl
import asyncio
import configparser
from aiohttp import web
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.webhook import WebhookRequestHandler, get_new_configured_app
from urllib.parse import parse_qs as urlencoded_to_dict

from db_helpers import *
from api_manager import ApiManager

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config['tokens']['bot']



bot = Bot(TOKEN, parse_mode='Markdown')
dp = Dispatcher(bot)

api = ApiManager()



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

@routes.get('/')
async def hello(request):
    print(request)
    return web.Response(text='Hello')


async def on_startup(_):
    webhook = await bot.get_webhook_info()
    if webhook.url:
        await bot.delete_webhook()
    await bot.set_webhook(f'https://omnideskbot.herokuapp.com/tg')

async def on_shutdown(_):
    await bot.delete_webhook()

#create_certificate()
# app = get_new_configured_app(dp, '/tg')
app = web.Application()
app.add_routes(routes)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

web.run_app(app, port=int(os.environ['PORT']))