# 剪贴板
import pyperclip
from PIL import ImageGrab,Image
import requests,os
# 获取剪切板内容
# im =ImageGrab.grab()
# url = "http://s1.sinaimg.cn/large/001Db1PVzy7qxVQWMjs06"
fn = "img/	别人的17岁.gif"

print(os.path.realpath(fn))
# img = Image

size = os.path.getsize(fn)
print("size:",size)

# clipboard_content = pyperclip.paste()

# 输出剪切板内容
# print(clipboard_content)

# if if __name__ == '__main__':