from api_helpers import ApiOmnidesk
import db_helpers as db

email = 'chistiytoillett@gmail.com'
token = '0bba95c6b13981b336f71e123'
channel = 'cch159'

api = ApiOmnidesk(email, token, channel)

class ApiManager:
    
    async def send_message(self, msg):
        case_id, omnidesk_id = db.get_user_case(msg.chat.id)
        if case_id:
            await api.send_message(msg.chat.id, case_id, omnidesk_id, msg.text)
        else:
            username = self.get_user_identifier(msg)
            case_id, omnidesk_id = await api.create_case(msg.chat.id, username, msg.text)
            db.set_user_case(msg.chat.id, case_id, omnidesk_id)
            return case_id
    
    async def send_file(self, msg, file, case_created=False):
        case_id, omnidesk_id = db.get_user_case(msg.chat.id)
        if case_id:
            await api.send_file(msg.chat.id, case_id, omnidesk_id, file)
            if case_created:
                return case_id
        else:
            username = self.get_user_identifier(msg)
            case_id, omnidesk_id = await api.create_case(msg.chat.id, username, 'Здравствуйте')
            db.set_user_case(msg.chat.id, case_id, omnidesk_id)
            await self.send_file(msg, file, case_created=True)
           
            
    def get_user_identifier(self, msg):
        if hasattr(msg.chat, 'username'):
            return '@' + msg.chat.username
        else:
            return msg.chat.first_name