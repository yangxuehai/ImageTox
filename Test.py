#coding=utf-8
import os,requests,re,random,pymysql,traceback,time,datetime,qrcode
from PIL import Image, ImageDraw, ImageFont,ImageOps
import zipfile
import numpy as np
import math,jieba
from  inc.base import *
from  inc.config import *
from  inc.language import *

# print(MakeFontList("/Users/yangxuehai/Documents/Program/LBTools/venv/ImageTox/assets/fonts/en/","10"))
#LangLibTools()
print(MakeLanguageFile("/Users/yangxuehai/Documents/ImageTox/Base/Language/xLanguage_0405-1.csv","/Users/yangxuehai/Downloads/langTest/",""))
def MakeDefaultImage(iDefault,inDir):
    for i in LANGUAGE_CONFIG.keys():
        os.system(f'cp {iDefault} {inDir}{i}.{GetExtName(iDefault,1)}')
    print("ok!")

# x=('WTtwv6uOzRNchY', '20200404', 'u586v51wt10TWYh65cN02Rz89O')
# print(RandomCrypto(RandomCrypto("","png","1",0)[2],"","",1))