import psycopg2


class DB():
    def __init__(self):
        self.db_conn = psycopg2.connect('postgres://mqiofrybtfrpqa:8d2a45cfac3bb1591cc0de19d11f3e50e7cb6cc365cd609757e45c0907648503@ec2-54-228-243-238.eu-west-1.compute.amazonaws.com:5432/d8f5hg48n0uh9e')
    
    def fast_query(self, query, params=()):
        cursor = self.cursor()
        try:
            cursor.execute(query, params)
        except Exception as a:
            raise a
        finally:
            self.commit()

    
    def cursor(self):
        return self.db_conn.cursor()
    
    def select(self, query, params=()):
        cursor = self.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        self.commit()
        return data
    
    def commit(self):
        return self.db_conn.commit()
    
    def fetchall(self):
        return self.db_conn.fetchall()
