import pymysql
from sqlalchemy import create_engine

class creepDao:
    def __init__(self) -> None:
        self.host = "10.242.128.7"
        self.user = "root"
        self.pwd = "Edifier1984"
        self.port = 3306
        self.database = "datacreeper"
    
    def connect_sql(self):
        # 使用pymysql获取连接对象
        connect = pymysql.connect(host=self.host,user=self.user,password=self.pwd,port=self.port,database=self.database)
        return connect

    def getDb(self):
        db = create_engine('mysql+pymysql://',creator=self.connect_sql)
        return db