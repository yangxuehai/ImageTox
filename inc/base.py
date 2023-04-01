#coding=utf-8
# 专用基础库
# 2019.10.20 By Yasur

import os, requests, re, random, pymysql, traceback, time, datetime,qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance,ExifTags
import zipfile
from flask import Flask, render_template, url_for, request, redirect
import numpy as np
import math, jieba
from inc.config import *
import ast


# 输出文件
# oFileName：文件名称
# outStr：输出字符串
# oMode：读写模式(w,r,a)
def OutFile(oFileName, outStr, oMode):
    FileObj2 = open(oFileName, oMode)
    FileObj2.write(outStr)
    FileObj2.close()

def OutFileUTF8(oFileName, outStr, oMode):
    FileObj2 = open(oFileName, oMode,encoding='utf-8')
    FileObj2.write(outStr)
    FileObj2.close()

#获取文件返回内容
def GetFile(FileName):
    with open(FileName,"r") as f:
        return f.read()

#获取字典文件返回字典变量
def GetDictFile(FileName):
    with open(FileName,"r",encoding='utf-8') as f:
        return ast.literal_eval(f.read())

# 输出结果调试
# OutPrintText:输出文本内容分
# PrintMode:输出模式，0为不换行;1换行
def OutResult(OutPrintText, PrintMode):
    if PrintMode == 1:
        print(OutPrintText)
    else:
        print(OutPrintText, end='')


# 打印输出进度记录并写入日志文件
# strPrint:输出字符串
# pMode:输出模式；0为不换行;1换行
def PrintLog(strFile, strPrint, pMode):
    OutResult(strPrint, pMode)
    if pMode == 1:
        OutFile(strFile, strPrint + "\n", "a")
    else:
        OutFile(strFile, strPrint, "a")


# 输出目录
def Prt(Str, mode):
    if mode == 1:
        print(Str, end='')
    else:
        print(Str)


# 检查并创建目录
def mDir(cDir):
    if not os.path.exists(cDir):
        os.makedirs(cDir, exist_ok=True)


# 获取5u代理IP
# http://api.ip.data5u.com/dynamic/get.html?order=46b3e00f6ae52a289b66320818ae5bd2&sep=3
def getIp():
    apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=46b3e00f6ae52a289b66320818ae5bd2&sep=3"
    # 开始自动获取IP
    ipList = requests.get(apiUrl).content.decode()
    # 按照\n分割获取到的IP
    ipStr = ipList.split('\n')
    return ipStr[0]


# 读取文件并List化,以行为单位list
def FileUrlList(FileName):
    FileObj = open(FileName)
    TempList = FileObj.read().split("\n")
    FileObj.close()
    return TempList


# 读取文件并List化,以逗号为单位list
def FileList(FileName):
    FileObj = open(FileName)
    TempList = FileObj.read().split(",")
    FileObj.close()
    return TempList


# 分词并输出都好风格的字符串，去重
def FenCi(fcStr):
    seg_list = jieba.lcut(fcStr, cut_all=False, HMM=True)
    seg_list = list(set(seg_list))
    return ",".join(seg_list)


# FixNameFile
def FixNameFile(InFile, OutFileList):
    fList = FileUrlList(InFile)
    xListStr = ""
    for ifList in fList:
        xListStr += FixProdName(ifList) + "\n"
    OutFile(OutFileList, xListStr, "w")
    return len(fList)


# 字符串List化
def StrList(cStr, cSplit):
    return cStr.split(cSplit)


# 字符串逗号替换
def comRep(cStr, cSplit):
    cStr = cStr.replace("，", ",").replace("、", ",").strip()
    return cStr.replace(",", cSplit)


# 提取字符串中的数字
def GetDigital(cStr):
    return re.sub("\D", "", cStr)


# 提取字符串中的字母
def GetAlpha(cStr):
    oStr = ''.join(re.split(r'[^A-Za-z ]', cStr))
    return oStr.strip()


# 去除字符串中的数字及符号，以空格替代
def RemoveX(cStr):
    remove_chars = '[’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    oStr = re.sub(remove_chars, ' ', cStr)
    return RemoveBlank(oStr)


# 不区分大小写替换:字符串，要替换的内容，目标内容
def ReplaceX(ReStr, ReWord, DestWord):
    pattern = re.compile(ReWord, re.IGNORECASE)
    return pattern.sub(DestWord, ReStr)


# 从列表中随机选择一项
def Sel(cSel):
    selStr = "".join(random.sample(cSel, 1))
    return selStr


# 从以竖线隔开的字符串中随机选择一项
def SelX(cSel):
    cSelList = cSel.split("|")
    selStr = "".join(random.sample(cSelList, 1))
    return selStr


# 生成时间日期字符串
def GetDateStr():
    return datetime.datetime.now().strftime('%d%H%M%S')


# 生成时间日期字符串
def GetDateDir(cType):
    if cType == 1:
        return datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        return datetime.datetime.now().strftime('%Y%m%d')


# 删除列表重复项
def deleteDuplicatedElementFromList(listA):
    # return list(set(listA))
    return sorted(set(listA), key=listA.index)


# 删除列表重复项 不改变顺序
def DelDuplicateList(inList):
    xList = []
    for i in inList:
        if i not in xList:
            xList.append(i)
    return xList


# 去除字符串中连续多个空格，只留一个
def RemoveBlank(inStr):
    return ' '.join(inStr.split())


# 处理空值，如果为空则返回空字符串，参数cStr为输入值，cType为输出类型：0为数值型，1为字符串
def BlankValue(cStr, cType):
    if cStr == "":
        if cType == 0:
            return "0"
        else:
            return ""
    else:
        return cStr


# 给以逗号隔开的每个字符串加个字符
def StrAddValue(inStr, addStr):
    inStrList = [i + addStr for i in inStr.split(",")]
    return ",".join(inStrList)


# 处理属性取值，取第一项
def getFirstValue(cStr):
    cxList = cStr.split(",")
    xValue = ""
    for xj in cxList:
        if not xj == "":
            if ord(xj[0]) < 200:
                xValue = xj
                return xValue
    return xValue


# 获取目录列表
def GetDirList(inDir):
    return [name for name in os.listdir(inDir) if os.path.isdir(os.path.join(inDir, name))]


# 获取文件列表
def GetFileList(inDir):
    # return [f for f in os.listdir(inDir) if os.path.isfile(os.path.join(inDir, f))]
    p = []
    for f in os.listdir(inDir):
        if not f.startswith('.'):
            p.append(f)
    return p


# 获取指定目录下的所有指定后缀的文件名
def GetFileSufList(path, suffix):
    input_template_All = []
    f_list = os.listdir(path)  # 返回文件名
    for i in f_list:
        if os.path.splitext(i)[1].lower() == suffix:
            input_template_All.append(i)
    return input_template_All


# 产生随机字符串，#len:长度,Prefix:前缀
def RandomStr(len, prefix):
    BaseStr = "ABCDEFGHRJKLMNOPQRSTUVWXYZabcdefghrjklmnopqrstuvwxyz1234567890"
    outStr = random.sample(BaseStr, len)
    return prefix + "".join(outStr)


# 产生随机字符串，#len:长度,Prefix:前缀
def RandomStrLower(len, prefix):
    BaseStr = "abcdefghrjklmnopqrstuvwxyz1234567890"
    outStr = random.sample(BaseStr, len)
    return prefix + "".join(outStr)

# 获取文件扩展名，mode：1为输出小写字符，其它为不变更。
def GetExtName(FileName, mode):
    if mode == 1:
        return FileName.split(".")[-1].lower()
    else:
        return FileName.split(".")[-1]


# 获取不带路径及扩展名的纯文件名
def GetPureName(FileName):
    return FileName.split("/")[-1].replace("." + GetExtName(FileName, 0), "")


# 获取不带路径的纯文件名
def GetFullName(FileName):
    return FileName.split("/")[-1]


# 获取目录及文件列表,inDir输入目录，outFile输出文件csv格式,最多支持两级目录。
def GetDirFileList(inDir, OutName):
    fNum = 0
    DirListStr = ""
    MainDirList = GetDirList(inDir)
    MainDirList.sort()
    for xMain in MainDirList:
        SubDir = inDir + xMain + "/"
        SubDirList = GetDirList(SubDir)
        print(xMain)
        if len(SubDirList) > 0:
            for xSub in SubDirList:
                FirDir = SubDir + xSub + "/"
                aFileList = GetFileList(FirDir)
                for xFile in aFileList:
                    DirListStr += xMain + "," + xSub + "," + xFile + "\n"
                    fNum += 1
        else:
            aFileList = GetFileList(SubDir)
            for xFile in aFileList:
                DirListStr += xMain + ", ," + xFile + "\n"
                fNum += 1
    OutFile(OutName, DirListStr, "a")
    return fNum


# 根据描述切分时分秒，如果小时为0，只输出分秒
def SecSplit(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    oStr = "%02d:%02d:%02d" % (h, m, s)
    if oStr[0:2] == "00": oStr = oStr[3:]
    return oStr


# 切分文件大小格式
def FileSizeSplit(fz):
    oStr = round(float(fz) / 1024 / 1024, 2)
    if oStr < 1:
        return fz + "k"
    else:
        return str(oStr) + "M"


# 判断传入字符串是否包含中文
# :param word: 待判断字符串
# :return: True:包含中文  False:不包含中文
def IncludeZH(inStr):
    for ch in inStr:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


# 创建压缩文件,输入参数为原始文件名(带路径)、输出目录名，文件名标题
def MakeZip(FileName, OutDir, FileTitle):
    ZipFileName = FileTitle + RandomStr(12, "-") + ".zip"
    with zipfile.ZipFile(OutDir + ZipFileName, 'w', zipfile.ZIP_DEFLATED) as zFile:
        zFile.write(FileName, arcname=GetFullName(FileName))
    return ZipFileName


# 创建压缩文件夹,输入参数为原始文件名(带路径)、输出目录名，文件名标题
def MakeDirZip(FileDir, OutDir, FileTitle):
    FileNums = 0
    ZipFileName = FileTitle + RandomStr(12, "_") + ".zip"
    with zipfile.ZipFile(OutDir + ZipFileName, 'w') as zFile:
        for DirPath, DirNames, FileNames in os.walk(FileDir):
            fPath = DirPath.replace(FileDir, '')
            fPath = fPath and fPath + os.sep or ''
            for FileName in FileNames:
                zFile.write(os.path.join(DirPath, FileName), fPath + FileName)
                FileNums += 1
    return ZipFileName, FileNums, FileNames


# 获取文本内网址,输入参数为字符串，返回URL列表
def GetHtmlUrl(string):
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
    return re.findall(pattern, string)


# 获取字符串中的中文
def GetChinese(txt):
    pattern = re.compile("[\u4e00-\u9fa5]")
    return "".join(pattern.findall(txt))


# 图片拼接.ColNums:每行几张图片,PicLimit：图片限制，超出多少后不进行处理,inDir：输入目录,OutFile：输出文件名为jpeg
def PicSplice(ColNums, PicLimit, inDir, OutFile):
    OutColumn = ColNums  # 小图列数
    Margin = 20  # 边距,大图底部也是此
    Spacing = 20  # 小图间距
    ImageWidth = 1000  # 图片总宽
    ImgHeight = 560  # 主图高度
    ImageBorderColor = "#DDDDDD"
    sImageBorderColor = "#EEEEEE"
    ImageBackground = "#xxx"
    IsWatermark = 1  # 是否打水印
    WatermarkFile = "/Users/yangxuehai/DataCenter/5EORG/Base/Watermark.png"

    ImgFileOrg = []
    ImgFileAll = GetFileSufList(inDir, ".jpg")
    ImgFileAll.sort()
    for ix in ImgFileAll:
        if ix.find("-0.jpg") == -1:
            ImgFileOrg.append(ix)

    FileNums = len(ImgFileOrg)

    if FileNums == 0: return 0
    if not PicLimit == 0 and FileNums > PicLimit: FileNums = PicLimit

    HWratio = ImgHeight / ImageWidth

    # 水印
    if IsWatermark == 1:
        WMImage = Image.open(WatermarkFile)
        WMWidth, WMHeight = WMImage.size
        BWMZoom = 4
        BWMImage = WMImage.resize((int(WMWidth / BWMZoom), int(WMHeight / BWMZoom)), Image.ANTIALIAS)

    # 计算小图尺寸
    fixBW = ImageWidth - Margin * 2  # 除去边距后的大图高宽
    fixBH = int(fixBW * HWratio)
    SW = int((fixBW - (OutColumn - 1) * Spacing) / OutColumn)
    SH = int(SW * HWratio)
    SRow = math.ceil(FileNums / OutColumn)

    ImageHeight = Margin * 2 + SRow * SH + (SRow - 1) * Spacing
    OutImages = Image.new('RGB', (ImageWidth, ImageHeight), (255, 255, 255))
    OutImages = ImageOps.expand(OutImages, border=1, fill=ImageBorderColor)

    cTime = 0
    for xFile in ImgFileOrg:
        sImage = Image.open(inDir + xFile)
        fixsImage = sImage.resize((SW, SH), Image.ANTIALIAS)
        fixsImage = ImageOps.expand(fixsImage, border=1, fill=ImageBorderColor)
        if IsWatermark == 1: fixsImage.paste(BWMImage, (30, 30), BWMImage)
        sImgX = Margin + (cTime % OutColumn) * (SW + Spacing)
        sImgY = Margin + (int(cTime / OutColumn)) * (SH + Spacing)
        OutImages.paste(fixsImage, (sImgX, sImgY))
        if not PicLimit == 0 and PicLimit == cTime: break
        cTime += 1
    OutImages.save(OutFile, 'jpeg', quality=80)

    return cTime


# 1:HEX2RGB;2:RGB2HEX
def RGBHEX(RGB, Type):
    if Type == 1:
        if not RGB[0] == "#": RGB = "#" + RGB
        if len(RGB) == 4: RGB = RGB + RGB.replace("#", "")
        return tuple(int(RGB[i:i + 2], 16) for i in (1, 3, 5))
    else:
        HEX = 1


# ColorType,ColorEnhance,cText,inImage,FontType,FontSize,FontColor,FontSpace,LineSpace,Background,Contrast,Brightness,PicPercent
# cText:Picture Character;ColorType:1-BlackWhite,2-Colorful;ColorEnhance:Saturation,Brightness,Contrast,Sharpness;
# QRcode 如果为空，不处理。传入参数为二维码内容
def MakeCharPicture(ColorType, ColorEnhance, ColorRevert,cText, inImage, FontType, FontSize, FontColor, FontSpace, LineSpace, Background, ProcessedFileName,QRcode):
    tStart = datetime.datetime.now()
    OrgImage = Image.open(inImage)
    try:  #处理手机等设备图片旋转问题
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation': break
        exif = dict(OrgImage._getexif().items())
        if exif[orientation] == 3:
            OrgImage = OrgImage.rotate(180, expand=True)
        elif exif[orientation] == 6:
            OrgImage = OrgImage.rotate(270, expand=True)
        elif exif[orientation] == 8:
            OrgImage = OrgImage.rotate(90, expand=True)
    except:
        pass

    ImgWidth, ImgHeight = OrgImage.size
    OrgImage = OrgImage.convert("RGBA")
    TextImages = Image.new('RGBA', (ImgWidth, ImgHeight), 0)
    nOrgImage = np.array(OrgImage)

    # Character Background,calculate character space,Process LineSpace&FontSpace,By to by.
    oDraw = ImageDraw.Draw(TextImages)
    Fonts = ImageFont.truetype(FontType, FontSize)
    twSpace = []
    tHeight = oDraw.textsize(cText, Fonts)[1]
    for i in cText:
        twSpace.append(oDraw.textsize(i, Fonts)[0])
    tPosX, tPosY, LineWidth, LineHeight = 0, 0, 0, 0
    while True:
        for idx, t in enumerate(cText):
            oDraw.text((tPosX, tPosY), t, FontColor, Fonts)
            LineWidth += twSpace[idx] + FontSpace
            tPosX, tPosY = (LineWidth, LineHeight)
            if LineWidth > ImgWidth:
                LineHeight += tHeight + LineSpace
                tPosX, LineWidth = 0, 0
                tPosY = LineHeight
        if LineHeight > ImgHeight:
            break

    nTextImages = np.array(TextImages)
    nTextImages = 255 - nTextImages  # Transparent inversion
    TextImages = Image.fromarray(nTextImages)
    R, G, B, A = TextImages.split()
    OrgImage.paste(TextImages, (0, 0), mask=A)

    # Process Images Effects
    if ColorType == 1:
        OrgImage = OrgImage.convert("L")  # GrayImages
    else:
        OrgImage = OrgImage.convert("RGB")  # GrayImages

    if ColorRevert == 1: OrgImage = ImageOps.invert(OrgImage)

    if not ColorEnhance[0] == 1: OrgImage = ImageEnhance.Color(OrgImage).enhance(ColorEnhance[0])
    if not ColorEnhance[1] == 1: OrgImage = ImageEnhance.Brightness(OrgImage).enhance(ColorEnhance[1])
    if not ColorEnhance[2] == 1: OrgImage = ImageEnhance.Contrast(OrgImage).enhance(ColorEnhance[2])
    if not ColorEnhance[3] == 1: OrgImage = ImageEnhance.Sharpness(OrgImage).enhance(ColorEnhance[3])

    if not QRcode=="":
        QRimg = MakeQRcode(QRcode,QRCODE_BG,(ImgWidth, ImgHeight))
        QRWidth,QRHeight=QRimg.size
        OrgImage.paste(QRimg, (ImgWidth-QRWidth, ImgHeight-QRHeight))
    UsedTime = str((datetime.datetime.now() - tStart).seconds)
    OrgImage.save(ProcessedFileName)
    return UsedTime, ProcessedFileName

#生成二维码
#inStr:字符串,bgImage：背景图片地址,MainImgSize：主图尺寸，为0则不改变大小
def MakeQRcode(inStr,bgImage,MainImgSize):
    ScaleRatio=10
    qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_Q,box_size=5,border=0)
    qr.add_data(inStr)
    qr.make(fit=True)
    img = qr.make_image()
    QRcodeBg = Image.open(bgImage)
    BgWidth,BgHeight=QRcodeBg.size
    img = img.resize((165, 165), Image.ANTIALIAS)
    QRcodeBg.paste(img, (0, 0))
    if not MainImgSize==0:
        MainWidth,MainHeight=MainImgSize
        if MainWidth<BgWidth*ScaleRatio:
            QRcodeBg=QRcodeBg.resize((round(MainWidth/ScaleRatio),round(MainWidth*1.05/ScaleRatio)),Image.ANTIALIAS)
    return QRcodeBg

# 读取语言文件并返回字典类型
def GetLang(LangType):
    if LangType in LANGUAGE_CONFIG.keys():
        return GetDictFile(LANGUAGE_DIR+LangType+".lang")
    else:
        return GetDictFile(LANGUAGE_DIR+DEFAULT_LANG+".lang")

# 转换饱和度等值
def EnhanceValue(inValue):
    return round((int(inValue) + 100) / 100, 2)


# 上传文件格式检查
def AllowFile(filename):
    return '.' in filename and \
           filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 根据字体值前缀2位获得字体文件名称及路径
def GetFontFile(fontValue):
    outStr = ""
    for i in LANGUAGE_CONFIG.keys():
        if fontValue[:2] == str(LANGUAGE_CONFIG[i]["Flag"]):
            outStr = i + "/" + fontValue.split("-")[0]
            break
    if outStr == "":
        outStr = DEFAULT_LANG + "/" + DEFAULT_FONT

    if "-" in fontValue:
        if fontValue.split("-")[1] == "2":
            outStr += ".otf"
        else:
            outStr += ".ttf"
    return outStr


# 获取默认字体文件值或文件，cType=0为值，1为文件
def GetDefaultFont(lang, cType):
    outStr = ""
    if lang in LANGUAGE_CONFIG.keys():
        outStr = LANGUAGE_CONFIG[lang]["Font_List"].split(";")[0].split(":")[1]
    else:
        outStr = DEFAULT_FONT
        lang = DEFAULT_LANG

    if cType == 0:
        return outStr
    else:
        return lang + "/" + outStr + DEFAULT_FONT_TYPE


# 获取默认字体列表
def GetFontList(lang):
    outList = []
    if not lang in LANGUAGE_CONFIG.keys() or lang == DEFAULT_LANG:
        return LANGUAGE_CONFIG[DEFAULT_LANG]["Font_List"].split(";")
    else:
        return (LANGUAGE_CONFIG[DEFAULT_LANG]["Font_List"] + ";" + LANGUAGE_CONFIG[lang]["Font_List"]).split(";")


# 指定目录字体生成字体列表
def MakeFontList(inDir, langNums):
    OutList = ""
    xNums = 1
    DirList = GetFileList(inDir)
    DirList.sort()
    for i in DirList:
        if GetExtName(i, 1) in "ttf,otf":
            f = langNums + str(xNums).zfill(2)
            xNums += 1
            if GetExtName(i, 1) == "ttf":
                OutList += ";" + GetPureName(i.strip()) + ":" + f + "-1"
            else:
                OutList += ";" + GetPureName(i.strip()) + ":" + f + "-2"

            os.rename(inDir + i, inDir + f + "." + GetExtName(i, 1))
        else:
            os.remove(inDir + i)
    return OutList[1:]

#存储数据
def SaveData(inData):
    #MainData
    OutFile(DATA_MAIN,inData,"a")
    #CountData


#存储统计合计数据
def SaveCountData(dataType):
    newtime = datetime.datetime.now()
    TodayKey=GetDateDir(2)
    with open(DATA_COUNT, "r+") as FileObj:
        CountData = ast.literal_eval(FileObj.read())
        AllData = CountData["AllData"].split(",")
        if dataType==1:
            CountData["AllData"] = str(int(AllData[0]) + 1)+","+str(int(AllData[1]) + 1)
        else:
            CountData["AllData"] = str(int(AllData[0])) + ","+str(int(AllData[1]) + 1)
        if  TodayKey in CountData.keys():
            KeyData=CountData[TodayKey].split(",")
            if dataType == 1:
                CountData[TodayKey] = str(int(KeyData[0]) + 1) + "," + str(int(KeyData[1]) + 1)
            else:
                CountData[TodayKey] = str(int(KeyData[0])) + "," + str(int(KeyData[1]) + 1)
        else:
            CountData[TodayKey] = "1,1"
        FileObj.seek(0)
        FileObj.truncate()
        FileObj.write(str(CountData))
        return (datetime.datetime.now()-newtime).microseconds

#获取语言列表
def GetLangList(cLang):
    outStr=tempStr=""
    xTemplate='<div class="col-3">\nXXtemplate</div>\n'
    for idx,iKey in enumerate(LANGUAGE_CONFIG.keys(),start=1):
        active=" active" if iKey==cLang else ""
        tempStr+=f'<a href="/{iKey}{APP_URL}" class="list-group-item list-group-item-action{active}">{LANGUAGE_CONFIG[iKey]["Language_Name"]}</a>\n'
        if idx % 6 == 0:
            outStr+=xTemplate.replace("XXtemplate",tempStr)
            tempStr=""
    return outStr

#判断输入地址语言并返回语言
def GetRedirectLang(cLang,LangList):
    RequestLanguage=request.accept_languages
    LangValue = RequestLanguage.best_match(LangList)
    if len(RequestLanguage)==0:
        SecondFlag=""
    else:
        SecondFlag=RequestLanguage[0][0].split("-")[1]
    if cLang not in LangList:
        if LangValue in LangList:
            OutLang=LangValue
        elif LangValue == None:
            if SecondFlag in LangList:
                OutLang=SecondFlag
            else:
                OutLang=DEFAULT_LANG
        else:
            OutLang = DEFAULT_LANG
    else:
        OutLang=cLang
    return OutLang

#语言库字典检查工具
def LangLibTools():
    LcKeys=LANGUAGE_CONFIG.keys()
    LcLen=len(LcKeys)
    Log = f"All {LcLen} Languages."
    Prt(Log,2)
    for idx,iKey in enumerate(LcKeys,start=1):
        FontNums=len(LANGUAGE_CONFIG[iKey]["Font_List"].split(":"))-1
        SampleNums=LANGUAGE_CONFIG[iKey]["Sample_Range"]
        iuLost=0
        iuLostList=""
        for i in range(1,SampleNums+1):
            if not os.path.exists(UPLOAD_SAMPLE_PIC_URL+iKey+"-"+str(i)+".jpg"):
                iuLost+=1
                iuLostList+=","+iKey+"-"+str(i)+".jpg"
        ipLost=0
        ipLostList=""
        for i in range(1,SampleNums+1):
            if not os.path.exists(PROCESSED_SAMPLE_PIC_URL+iKey+"-"+str(i)+".jpg"):
                ipLost+=1
                ipLostList+=","+iKey+"-"+str(i)+".jpg"
        Log = f"{idx}[{iKey}:{LANGUAGE_CONFIG[iKey]['Language_Name']}]-{FontNums} font.{SampleNums} sample,{iuLost} upload lost({iuLostList[1:]}),{ipLost} processed lost({ipLostList[1:]})"
        if os.path.exists(LANGUAGE_DIR + iKey + ".lang"):
            LangStatus = ".lang Exist"
            LangFile = GetDictFile(LANGUAGE_DIR + iKey + ".lang")
            LfKeys = LangFile.keys()
            LfLen=len(LfKeys)
            LfLostNum=0
            LfLostStr=""
            for idc,fKey in enumerate(LfKeys, start=1):
                if LangFile[fKey]=="":
                    LfLostNum+=1
                    LfLostStr+=","+fKey
            Log = f"{Log}-{LfLen} lang var.{LfLostNum} No value({LfLostStr[1:]})"
        else:
            LangStatus=".lang Not exist"
            Log = f"{Log} {LangStatus}"

        Prt(Log,2)

#生成并同步语言库：制定语言库文件、输出目录及指定的语言列表
def MakeLanguageFile(LibFile,OutDir,LangList):
    # en_lang=zh_lang=hk_lang=kr_lang=jp_lang=de_lang=fr_lang=th_lang=it_lang=tr_lang=pt_lang=ru_lang=es_lang=pl_lang=ar_lang=vn_lang=fa_lang=bn_lang=my_lang=uk_lang=nl_lang=in_lang=sv_lang=da_lang={}
    LibList=FileUrlList(LibFile)
    TitleList=LibList[0].split(",￥,")
    for idx,xLang in enumerate(TitleList):
        if idx == 0: continue
        exec(f"{xLang}_lang={{}}")
    for idx,xLib in enumerate(LibList):
        if idx==0:continue
        xLibList=xLib.split(",￥,")
        for jdx,colValue in enumerate(xLibList):
            if jdx==0:
                KeyName = colValue
                continue
            colValue=colValue.replace('"',"")
            xStr=f"{TitleList[jdx]}_lang['{KeyName}']=\"{colValue}\""
            exec(xStr)
    for idx,xLib in enumerate(TitleList):
        if idx == 0: continue
        # if xLib+"_lang"=="th_lang": OutFile(OutDir+xLib+".lang",str(th_lang),"a")
        exec(f"OutFileUTF8(OutDir + xLib + '.lang', str({xLib}_lang), 'a')")
    return f"{idx} File Created!"

#instr，输入字符串，加密是不用;mode 0为加密，1为解密
#dirMode目录模式，1为年月日，2月年月日时，以此类推,解密时不用
def RandomCrypto(instr,fileExt,dirMode,mode):
    OutStr=""
    if mode==0:
        fileExtNum = str(ALLOWED_EXTENSIONS.index(fileExt))
        rndStr=RandomStr(14, "")
        rndStr2=rndStr[::-1]
        nTime=round(time.time())
        nTime2=str(nTime)[::-1]
        for i in range(0,len(rndStr2),2):
            if i==len(nTime2):
                OutStr += rndStr2[i:i + 2] + dirMode+fileExtNum
            else:
                OutStr+=rndStr2[i:i+2]+nTime2[i:i+2]
        OutStr=OutStr[13:]+OutStr[0:13]
        if dirMode=="1":
            DirStyle = time.strftime("%Y%m%d", time.localtime(nTime))
        elif dirMode=="2":
            DirStyle = time.strftime("%Y%m%d%H", time.localtime(nTime))
        return DirStyle,rndStr,OutStr
    else:
        if not len(instr)==26:return False
        FileStr=DirStr=""
        instr=instr[13:]+instr[0:13]
        for i in range(0,len(instr),2):
            if (i/2)%2==0:
                FileStr+=instr[i:i+2]
            else:
                DirStr+=instr[i:i+2]
        dirMode=DirStr[-2]
        FileExtNum=DirStr[-1]
        if FileExtNum.isdigit() and int(FileExtNum)<len(ALLOWED_EXTENSIONS):
            FileExt=ALLOWED_EXTENSIONS[int(FileExtNum)]
        else:
            return False
        nTime=int(DirStr[0:10][::-1])
        if dirMode=="1":
            DirStyle = time.strftime("%Y%m%d", time.localtime(nTime))
        elif dirMode=="2":
            DirStyle = time.strftime("%Y%m%d%H", time.localtime(nTime))
        else:
            return False

        return DirStyle,FileStr[::-1],FileExt
