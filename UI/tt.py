
import path 
import sys
import os

print("f:  "+__file__)

print("path:  "+path.Path(__file__).abspath())

src_folder = path.Path(__file__).abspath()

print("os:   "+os.path.dirname( os.path.abspath(__file__) ))

print("final:  "+ src_folder.parent.parent + "/tools")

CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
config_path = CURRENT_DIR.rsplit('/', 0)[0]  # 当前目录,可以通过修改分割最右边的第几个'/'来拿到第几层目录

print("os FInal:  "+config_path + "/tools")