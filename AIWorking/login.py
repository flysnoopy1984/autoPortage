from selenium import webdriver
from selenium.webdriver.common.by import By 
from PIL import Image
from io import BytesIO
import requests
import numpy as np

import cv2
import time

AccountName = "13482710060"
AccountPwd = "edifier1984"
def zhihuLogin(driver:webdriver.Chrome):
 

    list = driver.find_elements(By.CLASS_NAME,"SignFlow-tab")
    list[1].click()

    xp = "/html/body/div[4]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[1]/div/form/div[2]/div/label/input"
    driver.find_element(By.XPATH,xp).send_keys(AccountName)

    xp = "/html/body/div[4]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[1]/div/form/div[3]/div/label/input"
    driver.find_element(By.XPATH,xp).send_keys(AccountPwd)

    time.sleep(1)

    xp = "/html/body/div[4]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[1]/div/form/button"
    driver.find_element(By.XPATH,xp).click()

    time.sleep(1)

   
    # 获取图片
    target_link = driver.find_element(By.CLASS_NAME, "yidun_bg-img").get_attribute('src')
    move_link = driver.find_element(By.CLASS_NAME, "yidun_jigsaw").get_attribute('src')

    target_img = Image.open(BytesIO(requests.get(target_link).content))
    move_img = Image.open(BytesIO(requests.get(move_link).content))
    target_img.save("img/target.jpg")
    move_img.save("img/template.png")

    distance = get_distance("img/target.jpg","img/template.png")
    distance = distance/480 * 345 + 12
    print("距离：%d",distance)


def handle_img(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)  # 转灰度图
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # 高斯模糊
    imgCanny = cv2.Canny(imgBlur, 60, 60)  # Canny算子边缘检测
    return imgCanny

def add_alpha_channel(img):

    r_channel, g_channel, b_channel = cv2.split(img)  # 剥离jpg图像通道
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255  # 创建Alpha通道
    img_new = cv2.merge((r_channel, g_channel, b_channel, alpha_channel))  # 融合通道
    return img_new

def get_distance(img_target_path,img_move_path):
    orig_target = cv2.imread(img_target_path,cv2.IMREAD_UNCHANGED)
    orig_move = cv2.imread(img_move_path)
    # 判断jpg图像是否已经为4通道
    if orig_target.shape[2] == 3:
        orig_target = add_alpha_channel(orig_target)

    after_target = handle_img(orig_target)
    after_move = handle_img(orig_move)

    res_TM_CCOEFF_NORMED = cv2.matchTemplate(after_target, after_move, cv2.TM_CCOEFF_NORMED)

    value = cv2.minMaxLoc(res_TM_CCOEFF_NORMED)
    value = value[3][0]  # 获取到移动距离
    return value







    


    


