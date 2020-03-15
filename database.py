import sqlalchemy as db

class Database():

    def __init__(self):
        self.engine = db.create_engine('postgresql://postgres:8121438n@nosangho.asuscomm.com:5432/stock')

    def return_engine(self):
        return self.engine


        # print("DB Instance created")
"""
    def saveData(self):
        try:
            self.connection.execute(
                "insert into basic.test(yyyymmdd, sCode, sName, per, roe, bps, profit, debt, pbr) values('{date}', '{code}', '{sname}', {per}, {roe}, {bps}, {profit}, {debt}, {pbr})".format(date=self.yyyymmdd, code=self.sCode, sname=self.sName, per=self.per, roe=self.roe, bps=self.bps, profit=self.profit, debt=self.debt, pbr=self.pbr)
            )
            print("{} finish".format(self.sName))
        except TypeError:
            pass

    def loadData(self, query):
        query_result = self.connection.excute(query)
        df = query_result

        return df"""