import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal,QThread
from PyQt6 import uic
from DataHandler.dm3DataHandler import dm3DataHandler 

from AIWorking.zhihuAuto import zhihuPublish

# import os
import path
src_folder = path.Path(__file__).abspath()
sys.path.append(src_folder.parent.parent)
from server.dm3service import dm3service
from datacreep.dm3Creep import creep3dm

from UI.imgDialog import imgDialog
import datetime


class mainWin(QMainWindow):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi("UI/UI_main.ui", self)      
        self.bn_run.clicked.connect(self.event_bn_creep)
        self.bn_dialog.clicked.connect(self.event_bn_dialog)
        self.bn_publish.clicked.connect(self.event_publish)
        self.bn_selectAll.clicked.connect(self.event_bn_selecteAll)

        # b = QPushButton()
        self.bn_publish.setDisabled(True)

        # l=  QLineEdit()
        deftext = "大嘴吹-{0}".format(datetime.datetime.now().strftime("%Y%m%d"))
        self.txt_title.setText(deftext)

        self.dm3Service = dm3service()
        self.dm3Handler = dm3DataHandler(self.tPicInfo)
        self.imgDialog = imgDialog()

    #全选
    def event_bn_selecteAll(self):
        self.dm3Handler.selectAllRow()


    #发布
    def event_publish(self):
      
        pd = self.dm3Handler.getPublishData(self.rb_isRandom.isChecked())
    
        pd.title = self.txt_title.text()
        for data in pd.list:
            print("titleName:{0},imgUrl:{1}".format(data.titleName,data.picUrl))       
    
        # 到知乎
        zhihuPublish(pd)
        pass
    
    #抓爬数据
    def event_bn_creep(self):

        self.tPicInfo.clearContents()
        url = self.cb_url.currentText()

        if(str.strip(url) == ""):
            QMessageBox.warning(self,"Stop","没有设置Url")
            return
      
        # 获取到URL，开始抓爬数据
        creep = creep3dm()
        creep.setWin(self)
        creep.start(url,1,2)

        # 获取到抓爬数据
        # 加载到内存，并展示
        self.dm3Handler.loadData(creep.data)
        try:
            # print("dataList Count:",len(self.dm3Handler.data))
            self.tm = threadMonitor(self.dm3Handler)
            self.tm.signalworker.connect(self.tm_connect)
            self.tm.start()     
        except Exception as e:
            print("Thread Error:",repr(e))

    def tm_connect(self):
        # self.bn_publish.setDisabled(False)
        self.event_publish()


    def event_bn_dialog(self):        
        self.imgDialog.setMinimumSize(600,500)
        self.imgDialog.exec()
        pass

    def showMessageFromOut(self,msg):
        QMessageBox.information(self,"Info",msg)

        
class threadMonitor(QThread):

    signalworker = pyqtSignal()

    def __init__(self,handler:dm3DataHandler) -> None:
        super().__init__()
      
        self.handler = handler

    def run(self):
        runStatus= 0
        while(runStatus == 0):
            # print("Thread Monitor dataList Count:",len(self.handler.data))
            # print("Thread downNum:",self.handler.imgDownNum)
            if(self.handler.imgDownNum == len(self.handler.data)):
                runStatus = 1 # 全部下载完毕到
                break
            QThread.sleep(2)

        if(runStatus == 1):
            self.signalworker.emit()
        
        self.quit()



if __name__ == '__main__':
    # # 创建一个app，应用
    app = QApplication(sys.argv)
    w = mainWin()
    w.show()
    sys.exit(app.exec())
