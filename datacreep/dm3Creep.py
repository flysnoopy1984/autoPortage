import path 
import sys
import typing
src_folder = path.Path(__file__).abspath()
sys.path.append(src_folder.parent.parent)
import requests
import bs4
from model.BindData.bdDm3Info import bdDm3Info 
from tools.dataUtil import dataUtil

# https://www.cnblogs.com/chenyangqit/p/16594745.html

class creep3dm:

 
    def __init__(self):
        self.data = []
 
    # @classmethod
    # def withWin(self,win):
    #     self.setWin(win)
    #     return self()


    def setWin(self,win):
        self.win = win
    
    def showMsg(self,msg):
        if(hasattr(self,"win")): self.win.showMessageFromOut(msg)
        else: print(msg)

    #URL获取内容
    def getPageHtml(self,url):
        webRes = requests.get(url)
        
        if(webRes.status_code != 404):
            webRes.encoding = 'UTF-8'
            self.soup = bs4.BeautifulSoup(webRes.text,'lxml')
            return True
        else: 
            self.showMsg("没有可用页面可操作")
            return False
      

    def analyHtml(self):
        wrapDiv = self.soup.find(name="div",class_="news_warp_center")
        pList = wrapDiv.find_all(name="p",attrs={'align':'center'})
        data = bdDm3Info()
        for p in pList:
            text = p.text
            if text == "\n\n":
                img = p.find(name="img")
                data.picUrl = img.attrs.get("src")
                data.ext = dataUtil.getExtFromUrl(data.picUrl)
                # data.picBlob = requests.get(data.picUrl).content
            else:
                data.titleName = text.replace("\r\n","").replace("\t","")
                self.data.append(data)
                data = bdDm3Info()

   
    #入口函数
    def start(self,url,pageStart=1,pageEnd=10):
        origUrl = url
        try:
            while pageStart<=pageEnd:
                if pageStart>1:
                    pos = origUrl.rfind(".")
                    if pos > -1 :
                        url = origUrl[0:pos]+"_"+str(pageStart)+".html"
                        # print("url:"+url)

                pageStart = int(pageStart)+1
                if(self.getPageHtml(url) == False): return True
                else:
                    self.analyHtml()
            return True
        
        except Exception as e:
            self.showMsg("creep get error : "+repr(e))

       
if __name__ == "__main__":
    creep = creep3dm()
    creep.start("https://www.3dmgame.com/bagua/5921.html",1,2)

    print("data:",len(creep.data),"个数据")
    for d in creep.data:
        print("imgUrl",d.picUrl," | text:",d.titleName," | ext:",d.ext)