import psycopg2

class Databases():
    """ 데이터 베이스 접속을 위한 클래스 """
    def __init__(self):
        self._db = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="8121438n", port=5433)
        self._cursor = self._db.cursor()
    
    def __del__(self):
        self._db.close()
        self._cursor.close()

    def execute(self, query, args={}):
        self._cursor.execute(query, args)
        row = self._cursor.fetchall()
        return row

    def commit(self):
        self._cursor.commit()


class CRUD(Databases):
    """ 
    데이터 베이스 CRUD를 위한 클래스

    엡데이트나 삭제는 DB프로그램을 활용하는 편이 나을것 같아 제외
    Database Class를 상속받아 사용

    : insertDB : 데이터 -> DB로 입력
    : readDB : DB데이터 읽기
    """
    def insertDB(self, schema, table, column, data):
        sql = f"INSERT INTO {schema}.{table}({column}) VALUES ({data});"
        print(sql)
        try:
            self._cursor.execute(sql)
            self._db.commit()
        except Exception as e:
            print("insert DB error", e)

    def readDB(self, schema, table, column):
        sql = f"SELECT {column} from {schema}.{table}"
        try:
            self._cursor.execute(sql)
            result = self._cursor.fetchall()
        except Exception as e:
            result = ("read DB error", e)
        return result