# import pymysql
from model.mDm3Info import mDm3Pic
from server.dm3service import dm3service
import path 
import sys
src_folder = path.Path(__file__).abspath()
sys.path.append(src_folder.parent.parent)
import tools.dataUtil as tool

# host = "10.242.128.7"
# user = "root"
# pwd = "Edifier1984"
# port = 3306


# def connectMySql():
#    db = pymysql.connect(host=host,user=user,password=pwd,port=port,database="datacreeper")
#    qp = db.cursor()

#    sql = "select * from dm3_info"

#    qp.execute(sql)
    
#    data = qp.fetchall() 
#    for d in data:
#       print("d1:",d[1])
#     #   print(d)
#    qp.close()

# test Data
def testservice():
   dm3 = dm3service()
   dm3.getInfoList()

def testInsertPicList():

   _dm3service = dm3service()
   picBlob = tool.convertToBinaryData("/Users/jackypc/Documents/AllProjects/Python/autoPortage/img/dongtu.gif")

   dm3Pic = mDm3Pic(infoId=6,picUrl="http://pic.rmb.bdstatic.com/bjh/down/e2114870927bbe8b5895d9c698fa1249.gif",ext="gif",
                 fileName="test.jpeg",titleName="幸福到昏倒",picBlob= picBlob)

   _dm3service.insertPicList([dm3Pic])

if __name__ == "__main__":
#    connectMySql()
   # for p in sys.path:
   #    print("path -- ",p)
   # print(src_folder.parent.parent)  
    testInsertPicList()
   # testservice()
   
