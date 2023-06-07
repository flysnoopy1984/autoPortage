import sys,path,os
src_folder = path.Path(__file__).abspath()
sys.path.append(src_folder.parent.parent)

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
import time,_thread
import tools.webTools as mytool
import subprocess
import model.pojo as pojo
from model.BindData.bdDm3Info import bdDm3Info
# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome    --remote-debugging-port=9222  --user-data-dir="/Users/jackypc/Documents/AllProjects/Python/chromeData"

class zhihuAuto:
    
    # targetUrl = "https://zhuanlan.zhihu.com/"
    # service = Service(executable_path="/Users/jackypc/Documents/自媒体/各种工具/自开发/DataCreep/SeleniumTest/driver/chromedriver")
    
    def initFromMyChrome(self):
        self.options = Options()
        self.options.add_argument('-ignore-certificate-errors')
        self.options.add_argument('-ignore -ssl-errors')

        self.options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
       
    def initNormalPorcess(self):
        self.options = Options()
        self.options.add_argument(argument="--disable-web-security")
        self.options.add_argument(argument="--remote-allow-origins=*")
        self.options.add_argument(argument="--disable-site-isolation-trials")

        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")

        self.options.add_argument("--disable-blink-features=AutomationControlled")

        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) awesomeScripts/1.0.0 Chrome/104.0.5112.102 Electron/20.1.1 Safari/537.36"
        self.options.add_argument('--user-agent='+ua)
        self.options.add_argument("--disable-infobars")
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])

        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{'source':'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'})

    def __init__(self):
        try:
            # self.options = Options()
            self.initFromMyChrome()
            
            self.targetUrl =  "https://zhuanlan.zhihu.com/"
            self.service = Service(executable_path="/Users/jackypc/Documents/自媒体/各种工具/自开发/DataCreep/SeleniumTest/driver/chromedriver") 

            self.driver = webdriver.Chrome(service=self.service,options=self.options)   
            self.driver.maximize_window()
            self.driver.implicitly_wait(3)

        except Exception as e:
            print("zhihuAuto Init Error",repr(e))

    def runWeb(self,data:pojo.publishData):
        try:
            
            mytool.modifyWebDriver(self.driver)
            self.driver.get(self.targetUrl)
   
            # 点击编写文章    
            self.data = data      
            self.__startWrite()        
            time.sleep(60*60)

        except BaseException as e:
           print("运行出现异常:"+repr(e))
            # print("运行出现异常:"+e.mess)

        finally:
            self.driver.quit()


    def __startWrite(self):

        self.driver.find_element(By.XPATH,"//div[@class='ColumnPageHeader-Button']/button").click()
    
        #切换 Tab
        curWin = self.driver.window_handles[1]
        self.driver.switch_to.window(curWin)

        # xs = "//*[@id=\"root\"]/div/main/div/div[2]/div[2]/div[2]/div[3]/div[5]/div/button[2]"
        # btn = self.driver.find_element(By.XPATH,xs)
        # print("btn:",btn.is_enabled())

        #title
        xs = "//*[@id=\"root\"]/div/main/div/div[2]/div[2]/div[1]/label/textarea"
        self.driver.find_element(By.XPATH,xs).send_keys(self.data.title)
        time.sleep(1)
        for index, val in enumerate(self.data.list):
            if(val.imgSize<10):

                #写标题               
                xs = "//*[@id=\"root\"]/div/main/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div/div/div/div/div[{0}]".format(index+1)
                w = self.driver.find_element(By.XPATH,xs)
                w.send_keys(val.titleName.strip())
                w.send_keys(Keys.ENTER)
                time.sleep(1)

                #点击图片按钮
                xs = "//*[@id=\"root\"]/div/main/div/div[2]/div[1]/div/div/div/div[1]/div[4]/div/button"
                self.driver.find_element(By.XPATH,xs).click()
                time.sleep(1)

                # imgPath = "/Users/jackypc/Documents/自媒体/项目/项目-搞笑/图文/20180809150910.gif"
                imgPath = os.path.realpath(val.fileName)
                xs = "/html/body/div[5]/div/div/div/div[2]/div/div/div/div[2]/div/div/input"
                self.driver.find_element(By.XPATH,xs).send_keys(imgPath)

                xs = "/html/body/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[3]/button"
                btnAddImg = self.driver.find_element(By.XPATH,xs)
                # while(btnAddImg.is_enabled() == False):
                #     pass
                # print("btnAddImg.text:",btnAddImg.text)
                    # print("button status :",btnEnable)
                time.sleep(4)
                btnAddImg.click()
                

       
           
def startChrome():
    cmd = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--remote-debugging-port=9222',"--user-data-dir=/Users/jackypc/Documents/AllProjects/Python/chromeData"]
    subprocess.call(cmd)


def zhihuPublish(data):
   
    _thread.start_new_thread(startChrome,())

    zh =zhihuAuto()
    time.sleep(5)

    zh.runWeb(data)
   

if __name__ == '__main__':

    data = pojo.publishData()
    data.title ="test"

    list= []
    model = bdDm3Info()
    model.titleName = "	别人的17岁"
    model.fileName = "img/	别人的17岁.gif"
    model.picUrl = "http://pic.rmb.bdstatic.com/bjh/down/a92ec6e086a6348245e9afeb357a4b31.gif"
    model.imgSize = 5
    list.append(model)

    model = bdDm3Info()
    model.titleName = "我不信除非你放大给我看"
    model.fileName = "img/我不信除非你放大给我看.gif"
    model.imgSize = 5  
    model.picUrl = "http://pic.rmb.bdstatic.com/bjh/down/a92ec6e086a6348245e9afeb357a4b31.gif"
    list.append(model)

    model = bdDm3Info()
    model.titleName = "我不信除非你放大给我看"
    model.fileName = "img/我不信除非你放大给我看.gif"
    model.imgSize = 5  
    model.picUrl = "http://pic.rmb.bdstatic.com/bjh/down/a92ec6e086a6348245e9afeb357a4b31.gif"
    list.append(model)

    data.list = list

    zhihuPublish(data)

    # _thread.start_new_thread(startChrome,())

    # time.sleep(5)

    # zh =zhihuAuto()
    
    # zh.runWeb()
       