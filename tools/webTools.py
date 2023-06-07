from selenium import webdriver

def modifyWebDriver(driver:webdriver.Chrome):
     # 读取js文件内容
    with open('tools/stealth.min.js','r',encoding='utf-8') as fp:
        content = fp.read()
    # 处理selenium中webdriver特征值
    driver.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {
            'source':content
        }
    )