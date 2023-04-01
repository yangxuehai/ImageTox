# coding:utf-8
# Create by YASUR 2020-3-15
# YANGXUEHAI@GMAIL.COM
import os, datetime, random, string, math, ast, sys, time, traceback
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps, ExifTags
from flask import Flask, render_template, url_for, request, redirect
import numpy as np
from inc.config import *
from inc.base import *

app = Flask(__name__)
app.config.from_object('inc.config')
SYS_LANG_LIST = LANGUAGE_CONFIG.keys()


@app.route("/")
def index():
    return redirect(url_for('CharacterPicture', cLang=GetRedirectLang("", SYS_LANG_LIST)))



@app.route("/<path:cLang>/character-picture/", methods=['GET', 'POST'])
@app.route("/<path:cLang>/character-picture/<FromWhere>", methods=['GET', 'POST'])
def CharacterPicture(cLang=None, FromWhere=None):
    t1 = datetime.datetime.now()
    RedirectLang = GetRedirectLang(cLang, SYS_LANG_LIST)
    LocalLangStr=""
    if  cLang == None or cLang not in SYS_LANG_LIST:
        return redirect(url_for('CharacterPicture', cLang=RedirectLang))
    if not cLang == RedirectLang:
        LangDict = GetDictFile(LANGUAGE_DIR + RedirectLang + ".lang")
        LocalLangStr=LangDict["LocalLangNotice"]+""
    FormValue = {}
    ErrorInfo = ""
    OrgImage = ""
    FullOutImage=""
    HrefLang = ['<link rel="alternate" hreflang="' + i + '" href="' + DOMAIN_URL + i + APP_URL + '"/>' for i in SYS_LANG_LIST]
    UrlList = (DOMAIN_URL + cLang + APP_URL, "/" + cLang + APP_URL, HrefLang,LocalLangStr)
    Forms = request.form
    iSubmit = Forms.get("iSubmit", "noSubmit")
    LANGUAGE_TEXT = GetLang(cLang)
    FontList = GetFontList(cLang)
    LangList = GetLangList(cLang)
    if iSubmit == "noSubmit":
        FormValue = INIT_VALUE
        FormValue["iCharacter"] = LANGUAGE_TEXT["DefaultCharater"]
        FormValue["iFont"] = GetDefaultFont(cLang, 0)
        if FromWhere == None:
            OutImage = PROCESSED_SAMPLE_PIC_URL + cLang + PROCESSED_DEFAULT_TYPE
            OrgImage = UPLOAD_SAMPLE_PIC_URL + cLang + PROCESSED_DEFAULT_TYPE
        else:
            uFrom = FromWhere[2:]
            uFile = RandomCrypto(uFrom, "", "", 1)
            if uFile:
                ShareImage = uFile[0] + "/" + uFile[1]
                OutImage = PROCESSED_PIC_URL + ShareImage + PROCESSED_DEFAULT_TYPE
                OrgImage = UPLOAD_PIC_URL + ShareImage + "." + uFile[2]
            else:
                OutImage = PROCESSED_SAMPLE_PIC_URL + cLang + PROCESSED_DEFAULT_TYPE
                OrgImage = UPLOAD_SAMPLE_PIC_URL + cLang + PROCESSED_DEFAULT_TYPE
        FullOutImage = OutImage
    else:
        FormValue["iCharacter"] = Forms.get("iCharacter", LANGUAGE_TEXT["DefaultCharater"])
        FormValue["iFont"] = Forms.get("iFont", GetDefaultFont(cLang, 0))
        FormValue["iFontSize"] = int(Forms.get("iFontSize", "12"))
        FormValue["iPhotoStyle"] = int(Forms.get("iPhotoStyle", "1"))
        FormValue["iEnhance"] = int(Forms.get("iEnhance", 0))
        FormValue["iWordSpace"] = int(Forms.get("iWordSpace", "3"))
        FormValue["iLineSpace"] = int(Forms.get("iLineSpace", "5"))
        FormValue["iSaturation"] = Forms.get("iSaturation", "0")
        FormValue["iBrightness"] = Forms.get("iBrightness", "0")
        FormValue["iContrast"] = Forms.get("iContrast", "0")
        FormValue["iSharpness"] = Forms.get("iSharpness", "0")
        FormValue["iTest"] = Forms.get("iTest", "")
        FormValue["iOrgFileName"] = Forms.get("iOrgFileName", "")
        FormValue["iLongTextCircle"] = Forms.get("iLongTextCircle", "1")
        FormValue["uPic"] = Forms.get("uPic", "")

        ColorEnhance = (EnhanceValue(FormValue["iSaturation"]), EnhanceValue(FormValue["iBrightness"]), EnhanceValue(FormValue["iContrast"]), EnhanceValue(FormValue["iSharpness"]))
        OutImage = PROCESSED_SAMPLE_PIC_URL + cLang + ".jpg"

        oImage = request.files["iFile"]
        if oImage:
            if AllowFile(oImage.filename):
                if len(oImage.read()) <= MAX_FILE_LENGTH:
                    ExtName = GetExtName(oImage.filename, 1)
                    uFile = RandomCrypto("", ExtName, "1", 0)
                    PicSubDir = uFile[0] + "/"
                    mDir(UPLOAD_PIC_DIR + PicSubDir)
                    mDir(PROCESSED_PIC_DIR + PicSubDir)
                    xFileName = uFile[1]
                    FormValue["uPic"] = "u:" + uFile[2]
                    UploadFileName = UPLOAD_PIC_DIR + PicSubDir + xFileName + "." + ExtName
                    ProcessedFileName = PROCESSED_PIC_DIR + PicSubDir + xFileName + PROCESSED_DEFAULT_TYPE
                    oImage.seek(0)  # When Object be readed,must let pointer to 0
                    oImage.save(UploadFileName)
                    FontType = FONT_DIR + GetFontFile(FormValue["iFont"])
                    Background = "#ffffff"
                    FontColor = "#000"
                    QrCodeStr = DOMAIN_URL + cLang + APP_URL + FormValue["uPic"]
                    UsedTime = MakeCharPicture(FormValue["iPhotoStyle"], ColorEnhance, FormValue["iEnhance"], FormValue["iCharacter"], UploadFileName, FontType, FormValue["iFontSize"], FontColor, FormValue["iWordSpace"], FormValue["iLineSpace"], Background, ProcessedFileName, QrCodeStr)
                    OutImage = STATIC_DIR + PROCESSED_BASE + PicSubDir + xFileName + PROCESSED_DEFAULT_TYPE
                    OrgImage = STATIC_DIR + UPLOAD_BASE + PicSubDir + xFileName + "." + ExtName
                    FullOutImage = PROCESSED_PIC_URL + PicSubDir + xFileName + PROCESSED_DEFAULT_TYPE
                    FormValue["iTest"] = PicSubDir + xFileName + "." + ExtName
                    FormValue["iOrgFileName"] = oImage.filename
                else:
                    ErrorInfo = LANGUAGE_TEXT["UploadFileSize"] + FileSizeSplit(str(MAX_FILE_LENGTH))
            else:
                ErrorInfo = LANGUAGE_TEXT["UploadFileType"] + ",".join(ALLOWED_EXTENSIONS)
        else:
            if not FormValue["iTest"] == "":
                if os.path.exists(UPLOAD_PIC_DIR + FormValue["iTest"]):
                    UploadFileName = UPLOAD_PIC_DIR + FormValue["iTest"]
                    ProcessedFile = FormValue["iTest"].replace("." + GetExtName(FormValue["iTest"], 1), PROCESSED_DEFAULT_TYPE)
                    ProcessedFileName = PROCESSED_PIC_DIR + ProcessedFile
                    FontType = FONT_DIR + GetFontFile(FormValue["iFont"])
                    Background = "#ffffff"
                    FontColor = "#000"
                    QrCodeStr = DOMAIN_URL + cLang + APP_URL + FormValue["uPic"]
                    print(QrCodeStr)
                    UsedTime = MakeCharPicture(FormValue["iPhotoStyle"], ColorEnhance, FormValue["iEnhance"], FormValue["iCharacter"], UploadFileName, FontType, FormValue["iFontSize"], FontColor, FormValue["iWordSpace"], FormValue["iLineSpace"], Background, ProcessedFileName, QrCodeStr)
                    OutImage = STATIC_DIR + PROCESSED_BASE + ProcessedFile + "?" + RandomStrLower(6, "")
                    FullOutImage = PROCESSED_PIC_URL + ProcessedFile
                    OrgImage = STATIC_DIR + PROCESSED_BASE + FormValue["iTest"]
                    FormValue["iTest"] = FormValue["iTest"]
                    FormValue["uPic"] = FormValue["uPic"]
                else:
                    ErrorInfo = LANGUAGE_TEXT["UploadFileEmpty"]
            else:
                ErrorInfo = LANGUAGE_TEXT["UploadFileEmpty"]

    Usedtime = str((datetime.datetime.now() - t1).microseconds) + "ms"
    return render_template('CharacterPicture.html', OutImage=OutImage, FormValue=FormValue, LANGUAGE_TEXT=LANGUAGE_TEXT, FontList=FontList, ErrorInfo=ErrorInfo, LangList=LangList, iLanguage=cLang, UrlList=UrlList, StaticDomain=STATIC_DOMAIN, OrgImage=OrgImage, DomainUrl=DOMAIN_URL, AppUrl=APP_URL,FullOutImage=FullOutImage)


@app.errorhandler(404)
def page_not_found(e):
    # return CharacterPicture("")
    return redirect(url_for('CharacterPicture', cLang=GetRedirectLang("", SYS_LANG_LIST)))


@app.route("/testlang")
def testlang():
    supported_languages = LANGUAGE_CONFIG.keys()
    x2 = request.accept_languages[0][0].split("-")[1]
    lang = (request.accept_languages.best_match(supported_languages), request.accept_languages, x2, GetRedirectLang("", SYS_LANG_LIST))
    return render_template('testlang.html', Showinfo=lang)


if __name__ == "__main__":
    if HOST == 0:
        app.run(host='0.0.0.0', debug=True, port=81)
    else:
        app.run(host='0.0.0.0', port=80)
