from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,DateTime,BINARY
import datetime 

Base = declarative_base()


class mDm3Info(Base):
    __tablename__ = "dm3_info"

    def ____getattribute__(self,attr):
        print("attr:",attr)

    def __init__(self,saveDirName,creepUrl):
        self.saveDirName = saveDirName
        self.creepUrl = creepUrl
        

    id = Column(Integer,primary_key=True,autoincrement="auto")
    saveDirName = Column(String(50),nullable=False)
    creepUrl = Column(String(255),nullable=False)
    createDateTime = Column(DateTime,default=datetime.datetime.now)
    updateDateTime = Column(DateTime,default=datetime.datetime.now)


class mDm3Pic(Base):

    __tablename__="dm3_pic"

    def __init__(self):
        pass

    

    def initData(self,infoId,picUrl,ext,fileName,titleName,picBlob):
        self.infoId = infoId
        self.picUrl = picUrl
        self.ext = ext
        self.fileName = fileName
        self.titleName  = titleName
        self.picBlob = picBlob


    id = Column(Integer,primary_key=True,autoincrement="auto")
    infoId = Column(Integer)
    picUrl = Column(String(500),nullable=False)
    ext = Column(String(10))
    fileName = Column(String(100))
    titleName = Column(String(100))
    createDateTime = Column(DateTime,default=datetime.datetime.now)
    updateDateTime = Column(DateTime,default=datetime.datetime.now)
    picBlob = Column(BINARY)
    pass