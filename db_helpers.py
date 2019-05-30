import psycopg2
from db_class import DB



db = DB()

def is_new_user(user_id):
    try:
        db.fast_query('insert into users(user_id) values(%s)', (user_id,))
    except:
        return False
    else:
        return True

def set_last_msg_id(user_id, msg_id):
    db.fast_query('update users set last_msg_id=%s where user_id=%s', (msg_id, user_id))

def get_last_msg_id(user_id):
    data = db.select('select last_msg_id from users where user_id=%s', (user_id,))
    if data:
        return data[0][0]
    else:
        None
def get_user_case(user_id):
    data = db.select('select case_id, omnidesk_id from users where user_id=%s', (user_id,))
    if data[0]:
        return data[0]
    else:
        None
    
def set_user_case(user_id, case_id, omnidesk_id):
    db.fast_query('update users set case_id=%s, omnidesk_id=%s where user_id=%s', (case_id, omnidesk_id, user_id))

if __name__ == '__main__':
    pass
    #db.fast_query('drop table users')
    #db.fast_query('create table users (user_id integer unique, case_id integer, omnidesk_id integer, last_msg_id integer)')
    #db.fast_query('update users set cookie=%s', ('''{"_user": "2bb1975c341efd8209a38d37f64fa7d53556f073654d965da5d62d19b9286ac83a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_user%22%3Bi%3A1%3Bs%3A50%3A%22%5B62935%2C%22ef9840cb989abefa405bbf9d8c9ae77c%22%2C2592000%5D%22%3B%7D"}''',))
    #print(is_new_user(1))
