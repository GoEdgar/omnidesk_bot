import aiohttp
from base64 import b64encode
from exceptions import *
import json
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


    async def _post_request(self, url, json):
        async with self.session.post(url, json=json) as r:
            json = await r.json()
            error = json.get('error')
            if not error:
                return json
            else:
                if error == 'case_not_found':
                    raise TicketNotFound(error)
                else:
                    raise RuntimeError(json)

        
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
