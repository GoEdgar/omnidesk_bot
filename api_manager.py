from api_helpers import ApiOmnidesk
import db_helpers as db
from exceptions import *

email = 'chistiytoillett@gmail.com'
token = '0bba95c6b13981b336f71e123'
channel = 'cch159'

api = ApiOmnidesk(email, token, channel)


class ApiManager:

    async def send_message(self, msg):
        case_id, omnidesk_id = db.get_user_case(msg.chat.id)
        if case_id:
            try:
                await api.send_message(msg.chat.id, case_id, omnidesk_id, msg.text)
            except TicketNotFound:
                db.del_user_case(msg.chat.id)
                return self._create_case(msg)
        else:
            return await self._create_case(msg)

    async def _create_case(self, msg):
        username = self.get_user_identifier(msg)
        case_id, omnidesk_id = await api.create_case(msg.chat.id, username, msg.text)
        db.set_user_case(msg.chat.id, case_id, omnidesk_id)
        return case_id

    def get_user_identifier(self, msg):
        if msg.chat.username:
            return '@' + msg.chat.username
        else:
            return msg.chat.first_name
