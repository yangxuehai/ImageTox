# coding:utf-8
# Create by YASUR 2020-3-15
# YANGXUEHAI@GMAIL.COM
# Base Config File
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__)).replace("/inc", "")

MAIN_DOMAIN = "imageTox.com"
DOMAIN_URL = "https://imageTox.com/"
APP_URL = "/character-picture/"
MAIN_MAIL = "imageTox@gmail.com"
STATIC_DIR = "/static"
HOST=1 if APP_ROOT.find("www") > -1 else 0
STATIC_DOMAIN = "https://img.imagetox.com" if HOST==1 else STATIC_DIR

UPLOAD_BASE="/storage/character/uploaded/"
UPLOAD_PIC_URL = STATIC_DOMAIN + UPLOAD_BASE
UPLOAD_PIC_DIR = APP_ROOT + STATIC_DIR + UPLOAD_BASE
UPLOAD_SAMPLE_PIC_URL = UPLOAD_PIC_URL + "sample/"

PROCESSED_BASE="/storage/character/processed/"
PROCESSED_PIC_URL = STATIC_DOMAIN + PROCESSED_BASE
PROCESSED_PIC_DIR = APP_ROOT + STATIC_DIR + PROCESSED_BASE
PROCESSED_SAMPLE_PIC_URL = PROCESSED_PIC_URL + "sample/"
PROCESSED_DEFAULT_TYPE=".jpg"

FONT_DIR = APP_ROOT + "/assets/fonts/"
LANGUAGE_DIR = APP_ROOT + "/inc/language/"
DATA_DIR = "/data/"
DATA_MAIN = APP_ROOT + DATA_DIR + "main.itd"
DATA_COUNT = APP_ROOT + DATA_DIR + "count.itd"

QRCODE_BG=APP_ROOT + STATIC_DIR+"/image/base/QRcodeBg.png"

ALLOWED_EXTENSIONS = 'png,jpg,jpeg'.split(",")
MAX_FILE_LENGTH = 10 * 1024 * 1024  # 10M

INIT_VALUE = {
    "iCharacter": "",
    "iFont": "",
    "iFontSize": 12,
    "iPhotoStyle": 1,
    "iEnhance": 0,
    "iWordSpace": 1,
    "iLineSpace": 1,
    "iSaturation": 0,
    "iBrightness": 0,
    "iContrast": 0,
    "iSharpness": 0,
    "iTest": "",
    "iOrgFileName": "",
    "iLongTextCircle": 1,
    "uPic":"",
}

DEFAULT_LANG = "en"
DEFAULT_FONT = "1000"
DEFAULT_FONT_TYPE = ".ttf"
LANGUAGE_CONFIG = {
    "en": {
        "Flag": 10,
        "Font_List": "Arial:1000-1;04B_08 Pixel:1001-1;Amaranth:1002-2;Avant Guard:1004-1;Black Night:1005-1;Blecklet:1006-1;Greekbeartinye:1007-1;HelveticaInserat:1008-2;Impact:1009-2;Made Canvas:1010-2;Sans Serif:1011-1;Superhet:1012-1;Tahoma:1013-1;Verdana:1014-1;Zinc Boomerang:1015-1",
        "Language_Name": "English",
        "Sample_Range": 1,
    },
    "zh": {
        "Flag": 11,
        "Font_List": "经典宋体简:1100-1;微软雅黑:1101-1;方正清刻本悦宋简:1102-1;田氏颜体:1103-1;经典仿宋简:1104-1;经典仿宋繁:1105-1;经典圆体简:1106-1;经典圆体繁:1107-1;方正启体简体:1108-1;经典宋体繁:1109-1;经典楷体简:1110-1;经典楷体繁:1111-1;经典粗黑简:1112-1;经典粗黑繁:1113-1;经典繁古印:1114-1;经典繁方篆:1115-1;经典繁行书:1116-1;经典繁角篆:1117-1;经典细隶书简:1118-1;经典细隶书繁:1119-1;经典美黑简:1120-1;经典美黑繁:1121-1;经典行书简:1122-1;经典行楷简:1123-1;经典行楷繁:1124-1",
        "Language_Name": "中文简体",
        "Sample_Range": 1,
    },
    "tw": {
        "Flag": 12,
        "Font_List": "Test:1000-1",
        "Language_Name": "中文繁體",
        "Sample_Range": 1,
    },
    "kr": {
        "Flag": 13,
        "Font_List": "Test:1000-1",
        "Language_Name": "한국어",
        "Sample_Range": 1,
    },
    "jp": {
        "Flag": 14,
        "Font_List": "Test:1000-1",
        "Language_Name": "にほんご",
        "Sample_Range": 1,
    },
    "de": {
        "Flag": 15,
        "Font_List": "Test:1000-1",
        "Language_Name": "Deutsch",
        "Sample_Range": 1,
    },
    "fr": {
        "Flag": 16,
        "Font_List": "Test:1000-1",
        "Language_Name": "Français",
        "Sample_Range": 1,
    },
    "th": {
        "Flag": 17,
        "Font_List": "Test:1000-1",
        "Language_Name": "ไทย",
        "Sample_Range": 1,
    },
    "it": {
        "Flag": 18,
        "Font_List": "Test:1000-1",
        "Language_Name": "Italiano",
        "Sample_Range": 1,
    },
    "tr": {
        "Flag": 19,
        "Font_List": "Test:1000-1",
        "Language_Name": "Türkçe",
        "Sample_Range": 1,
    },
    "pt": {
        "Flag": 20,
        "Font_List": "Test:1000-1",
        "Language_Name": "Português",
        "Sample_Range": 1,
    },
    "ru": {
        "Flag": 21,
        "Font_List": "Test:1000-1",
        "Language_Name": "Русский",
        "Sample_Range": 1,
    },
    "es": {
        "Flag": 22,
        "Font_List": "Test:1000-1",
        "Language_Name": "Español",
        "Sample_Range": 1,
    },
    "pl": {
        "Flag": 23,
        "Font_List": "Test:1000-1",
        "Language_Name": "Polskie",
        "Sample_Range": 1,
    },
    "ar": {
        "Flag": 24,
        "Font_List": "Test:1000-1",
        "Language_Name": "عربي  ",
        "Sample_Range": 1,
    },
    "vn": {
        "Flag": 25,
        "Font_List": "Test:1000-1",
        "Language_Name": "Tiếng việt",
        "Sample_Range": 1,
    },
    "fa": {
        "Flag": 26,
        "Font_List": "Test:1000-1",
        "Language_Name": "فارسی ",
        "Sample_Range": 1,
    },
    "bn": {
        "Flag": 27,
        "Font_List": "Test:1000-1",
        "Language_Name": "বাংলা ভাষার",
        "Sample_Range": 1,
    },
    "my": {
        "Flag": 28,
        "Font_List": "Test:1000-1",
        "Language_Name": "Melayu",
        "Sample_Range": 1,
    },
    "uk": {
        "Flag": 29,
        "Font_List": "Test:1000-1",
        "Language_Name": "Українська",
        "Sample_Range": 1,
    },
    "nl": {
        "Flag": 30,
        "Font_List": "Test:1000-1",
        "Language_Name": "Nederlands",
        "Sample_Range": 1,
    },
    "in": {
        "Flag": 31,
        "Font_List": "Test:1000-1",
        "Language_Name": "हिन्दी",
        "Sample_Range": 1,
    },
    "sv": {
        "Flag": 32,
        "Font_List": "Test:1000-1",
        "Language_Name": "svenska",
        "Sample_Range": 1,
    },
    "da": {
        "Flag": 33,
        "Font_List": "Test:1000-1",
        "Language_Name": "dansk",
        "Sample_Range": 1,
    },
}
