import psycopg2


class DB():
    def __init__(self):
        self.db_conn = psycopg2.connect('postgres://wqbllaucfcdslr:82f7c6eba7f7817f806d5392cbc0872cfd6cf1d74753dc2711f5992de787342b@ec2-54-228-243-29.eu-west-1.compute.amazonaws.com:5432/daojeeg322p7sc')
    
    def fast_query(self, query, params=()):
        cursor = self.cursor()
        try:
            cursor.execute(query, params)
            print('done')
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
