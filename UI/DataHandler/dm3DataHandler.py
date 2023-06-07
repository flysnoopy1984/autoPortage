import sys
import typing
from PyQt6.QtCore import QObject
import path
src_folder = path.Path(__file__).abspath()
sys.path.append(src_folder.parent.parent.parent)
from PyQt6.QtWidgets import *
from PyQt6 import QtGui,QtCore
from model.BindData.bdDm3Info import bdDm3Info
from model.pojo import publishData
# from PyQt6. import  *
import requests
from PyQt6.QtCore import * 
from PyQt6.QtGui import *
# import os
import random


class dm3DataHandler():

    def __init__(self,table:QTableWidget):
        
        self.t = table
        self.t.verticalHeader().setDefaultSectionSize(100)

        # self.t.cellClicked.connect(self.event_cellClick)

        self.t.setStyleSheet("selection-background-color: rgba(156, 203, 233, 50);")
        
        self.t.itemSelectionChanged.connect(self.tableRowSelected)


        self.pool = QThreadPool.globalInstance()
        self.pool.setMaxThreadCount(16)
    
    
        self.signal = signalImgDown()
        self.signal.download.connect(self.event_updateImg)

        self.dataMap = {}
        self.selectedAll = False
        self.downDone = False

    #全选非全选
    def selectAllRow(self):
        
        if(self.selectedAll == False):
            self.t.selectAll()  
        else:
            self.t.clearSelection()

        self.selectedAll = ~self.selectedAll

    #当选择表格时触发
    def tableRowSelected(self):
        selItems = self.t.selectedItems()       
        self.dataMap.clear()        
        for item in selItems:
            rowIndex = item.row()
            if(self.dataMap.get(rowIndex) == None):
                d = self.t.item(rowIndex,1).data(QtCore.Qt.ItemDataRole.UserRole)
                self.dataMap[rowIndex] = d  
        pass

    #异步下载图片
    def asyncImgdown(self,data:bdDm3Info):

        run = imgDownRunnable(data,self.signal) 
        
        self.pool.start(run)
    
    #异步下载图片回掉更新UI
    def event_updateImg(self,data:bdDm3Info):   
      
        self.setImg(1,data)

    #发布数据
    def getPublishData(self,isRandom=True):
        result = publishData()
      
        dataList =list(self.dataMap.values())
        if(isRandom == True):         
            random.shuffle(dataList)
        result.setData("",dataList)
        return result
 
    #加载爬虫后的数据
    def loadData(self,list):        
        self.data = list
        self.imgDownNum = 0
    
        for d in list:      
           curRow = self.t.rowCount()  
           self.t.setRowCount(curRow+1)
           self.rowIndex = curRow
           d.rowIndex = curRow

           self.asyncImgdown(d)

            #数据列
           self.setItem(1,d,QtCore.Qt.ItemDataRole.UserRole)
           #显示title
           self.setItem(2,d.titleName,QtCore.Qt.ItemDataRole.DisplayRole)
        
        self.selectAllRow()
           
                 
    def setCheckBox(self,colIndex):
        cbItem = QCheckBox()
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(cbItem)
        self.t.setCellWidget(self.rowIndex,colIndex,container)
    

    def setImg(self,colIndex,picObj:bdDm3Info):
        lb_img =  QLabel()
        lb_img.setScaledContents(True)
        if(picObj.ext == "gif"):
            path = self.downImage(picObj)
            gif = QtGui.QMovie(path)
            lb_img.setMovie(gif)
            gif.start()                 
        else:
            self.downImage(picObj)
            img = QtGui.QPixmap()
            img.loadFromData(picObj.picBlob,picObj.ext)
            lb_img.setPixmap(img)

        self.t.setCellWidget(picObj.rowIndex,colIndex,lb_img)   

    def downImage(self,picObj:bdDm3Info):
        savepath ="img/"+picObj.titleName+"."+picObj.ext

        with open(savepath,"wb") as f:
            fb =  bytearray(picObj.picBlob)
            f.write(fb)
            
        picObj.fileName = savepath
        self.imgDownNum = self.imgDownNum+1
        if(self.imgDownNum == len(self.data)):
            self.downDone = True
            pass
        return savepath         


    def setItem(self,colIndex,value,role):        
      
        item = QTableWidgetItem()
       
        item.setData(role,value)
        
        self.t.setItem(self.rowIndex,colIndex,item)

    # def startMonitorThread():
    #     thread = QThread()
    #     work = monitorWorker()
    #     work.moveToThread(thread)
        
    #     thread.start()
    # def event_cellClick(self,row,col):

    #     print("row:",row,"col:",col)
    #     pass



class signalImgDown(QObject):
     
     download= pyqtSignal(bdDm3Info)

class imgDownRunnable(QRunnable):

    def __init__(self,creepObj:bdDm3Info,signal:signalImgDown):
        super().__init__()
        self.creepObj = creepObj
        self.signal = signal
        pass

    def run(self) -> None:
    #   print("start down img",self.creepObj.picUrl)

        self.creepObj.picBlob = requests.get(self.creepObj.picUrl).content 
        self.creepObj.imgSize = len(self.creepObj.picBlob)/1024/1024
            
        self.signal.download.emit(self.creepObj)







       

