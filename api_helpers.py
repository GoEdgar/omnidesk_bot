import aiohttp
from aiohttp import FormData
from base64 import b64encode
import asyncio

api_url = 'https://spooti.omnidesk.ru/api/'



def _to_base64(token):
    return b64encode(token.encode('utf-8')).decode('utf-8')


class ApiOmnidesk:
    def __init__(self, email, token, channel):
        self.channel = channel
        token_base64 = _to_base64(email + ':' + token)
        headers = {'Authorization': 'Basic ' + token_base64}
        self.session = aiohttp.ClientSession(headers=headers)
    

    async def _post_request(self, url, json=None, data=None):
        async with self.session.post(url, json=json, data=data) as r:
            if r.status == 201:
                json = await r.json()
                return json
            else:
                json = await r.json()
                print(json)
                raise RuntimeError(r.status)

        
    async def create_case(self, user_id, username, text):
        
        case = {'case': {
                    'user_custom_id': user_id,
                    'user_full_name': username,
                    'subject': '    ',
                    'content': text,
                    'channel': self.channel}}
        
        data = await self._post_request(api_url + 'cases.json', json=case)
        data = data['case']
        return data['case_id'], data['user_id']
    
    
    async def send_message(self, user_id, case_id, omnidesk_id, text):
        message = {'message': {
                    'user_id': omnidesk_id,
                    'user_custom_id': user_id,
                    'content': text}}
        
        url = api_url + f'cases/{case_id}/messages.json'
        await self._post_request(url, json=message)
    
    
    async def send_file(self, user_id, case_id, omnidesk_id, file):
        form = FormData()
        print(user_id, case_id, omnidesk_id)
        form.add_field('message[user_id]', str(omnidesk_id))
        form.add_field('message[user_custom_id]', str(user_id))
        form.add_field('message[attachments][0]', file, filename='voice.mp3')
        
        url = api_url + f'cases/{case_id}/messages.json'
        #url = 'http://localhost:8000'
        await self._post_request(url, data=form)

email = 'chistiytoillett@gmail.com'
token = '0bba95c6b13981b336f71e123'
channel = 'cch159'

api = ApiOmnidesk(email, token, channel)

loop = asyncio.get_event_loop()

loop.create_task(api.send_file(425439946, 49457537, 11522802, open(r'C:\Users\Spooti\Pictures\g.png', 'rb')))

loop.run_forever()