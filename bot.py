import os
import ssl
import asyncio
import configparser
from exceptions import *
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
        await bot.send_message(msg.chat.id, f'Вас приветствует бот поддержки брендов 2х2 '
                                            'Оставьте свой вопрос и мы Вам обязательно '
                                            'ответим.')
    else:
        await bot.send_message(msg.chat.id,
                               f'Оставьте свой вопрос и мы Вам обязательно ответим.')


@dp.message_handler()
async def message(msg):
    case_id = await api.send_message(msg)
    if case_id:
        print('создаю тикет')
        await msg.reply(f'✅ Тикет номер *{case_id}* создан!')
    else:
        reply_msg = await msg.reply('✅ *Доставлено*')
        await asyncio.sleep(10)
        await reply_msg.delete()


async def omnidesk_msg_handler(data):
    user_id = int(data['object[custom_user_id]'][0])
    print(user_id)
    text = data['object[content]'][0]
    await bot.send_message(int(user_id), text)


routes = web.RouteTableDef()


@routes.get('/')
async def hello(request):
    print(request)
    return web.Response(text='<Omnidesk bot> by @spooti')


@routes.post('/omnidesk_message')
async def change_status(request):
    if 'urlencode' in request.content_type:
        data = urlencoded_to_dict(await request.text())
        await omnidesk_msg_handler(data)
    return web.Response()


async def on_startup(_):
    wh_url = 'https://omideskbot.herokuapp.com/tg'
    webhook = await bot.get_webhook_info()
    if webhook.url != wh_url:
        await bot.delete_webhook()
        await bot.set_webhook(f'https://omideskbot.herokuapp.com/tg')


app = get_new_configured_app(dp, '/tg')

app.add_routes(routes)

app.on_startup.append(on_startup)
web.run_app(app, port=os.environ['PORT'])
