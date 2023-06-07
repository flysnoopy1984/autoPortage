
from sqlalchemy.orm import sessionmaker
from model.mDm3Info import mDm3Info,mDm3Pic
from server.creepDao import creepDao

# import path 
# import sys
# src_folder = path.Path(__file__).abspath()
# print(src_folder.parent.parent + "/tools")
# sys.path.append(src_folder.parent.parent + "/tools")
# import tools.dataUtil as tool


class dm3service:
    def __init__(self):
        pass
    def getDbSession(self):
        try:
            # 创建会话
            db = creepDao()
            obj_session = sessionmaker(db.getDb())
            db_session = obj_session()
            return db_session
        except Exception as e:
            print("getDbSession",repr(e))


    def getInfoList(self):
       
        try:
        # 创建会话
            db_session = self.getDbSession()
            all_list = db_session.query(mDm3Info).all()
            for obj in all_list:
                print(obj.id,obj.creepUrl,obj.saveDirName)        
        finally:
               db_session.close()
        
    def insertPicList(self,picList):
         try:
            db_session = self.getDbSession()
            db_session.add_all(picList)
            db_session.commit()
         except Exception as e:
            print(repr(e))
            # db_session.execute
         finally:
            db_session.close()
    
    def getPicList(self):
        try:
            db_session = self.getDbSession()
            all_list = db_session.query(mDm3Pic).all()
            return all_list
        except Exception as e:
            print(repr(e))
        finally:
            db_session.close()
    
