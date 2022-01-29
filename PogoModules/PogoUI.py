# coding=UTF-8
PogoUIVer = '2020/7/10 v4.0.2'

'''
Pogo driver webdriver 控制快速模組

2020/07/10 v4.0.2 取消 Bsleep 倒數
2019/12/16 v4.0.1 加強 https 的相容性
2019/10/9 v4.0.0 與 Python3 版本合併, 直接相容 Python 2 & 3
2019/4/19 v3.3.2 bug fix
2019/4/17 v3.3.1 續 3.3.0 改版完成
2019/4/16 v3.3.0 指令結尾為 D 的 多工支援, 可指定 driver 變數
2018/3/29 v3.2.1 改變 log 的時間格式
2018/2/27 v3.2.0 linux 相容
2017/10/5 v3.1.9 增加幾個結尾是D的語法, 讓多個 def 內能加 driver 參數運作
2017/9/26 v3.1.8 Bver 語法移至 PogoPeplink.py
2017/6/29 v3.1.7 改 Default Browser 為 Chrome
2017/6/7 v3.1.6 Bwait_test 一樣問題, 加1sec 媽的...
2017/6/7 v3.1.5 Bvisit 增加 1 sec 的 delay , B310HW4 7.0.1 GA 後會有詭異的UI異常, 等1sec 可避免
2017/5/18 v3.1.4 Bver fix
2017/5/9 v3.1.3 增加 Bcap2 增強full screen cap 的能力 !! 需要 pillow 模組 !! 語法為 Bcap2(driver,'檔名')
2017/5/8 v3.1.2 增加 BKey 功能, 與直接 import webdriver 的 Keys
2017/4/20 v3.1.1 bug fix
2017/3/31 v3.1 增加 hughlight 元素功能
2016/11/8 v3.0.8 新增 Bver 版本控制功能
2016/11/3 v3.0.7 Bxxt BclickT 判斷機制再加強與修正
2016/4/20 v3.0.6 bug fix
2016/4/19 v3.0.5 BselectT 改為 BselectTO, 增加 Sxxxxx 功能在 fail 時 中止程式, 增加 Bsleep 功能
2016/4/18 v3.0.4 改寫模組式與 log 訊息
2016/4/14 v3.0.3 增加 BselectT 點選符合 2 字串條件的元素
2016/4/14 v3.0.2 增加 BclickTO 選擇選項第 ? 個
2016/4/6 v3.0.1 重新改寫 BxxxT 成模組式
2016/4/6 v3.0.0 完善 BxxxT 語法訊息
2016/4/1 v2.9.3 舊有的 Bxxx 語法判斷式補正, 正確回1 失敗回0
2016/3/31 v2.9.2 增加 BfillTT 用來填入 textarea 的欄位, 發現要和input 分開才不會混亂錯誤
2016/3/30 v2.9.1 BxxxT 功能 增加微調選項
2016/3/29 v2.8.8 BxxxT 功能 加強選擇邏輯, 由內向外選合條件的元件
2016/3/29 v2.8.7 新增 BcheckT 與 BncheckT 功能
2016/3/28 v2.8.6 新增 BfillT 與 BclickT 功能
2016/3/25 v2.8.5 Bclick 刪除 value = 特定完元判斷, 發現用不太到
2016/3/24 v2.8.4 Bclick 增加只要看特定字元, 就把全部符合條件的目標都 click 一次
2016/3/23 v2.8.3 bug fix
2016/3/10 v2.8.2 增加 Bdrop Bcheck 成功回傳 1 , 失敗回傳 0 
2016/1/18 v2.8.1 增加版本 log 配合
2016/1/15 v2.8 增加成功行畫面顯示訊息, 部分語法重新整理
v2.7.2: 語法修正
v2.7.1: 配合模組式小修改
v2.7: 增加 Bwait可以自訂重試次數, wait & click 加入成功與失敗的回傳機制
v2.6: 增加以 javascript click 的方式, 並改變原 click 失敗後自動試 javascript 方式
v2.5.3: 修正 Bvisit 失敗沒清空 temp 問題
v2.5.2: 加 find element by id
v2.5.1: 修正關 firefox 沒清空暫存問題, 與 Felement 判斷是否存在
v2.5: 增加取得元素值的機制
v2.4: 改善訊息格式為 功能 + 狀態
v2.3: 增加找字串機制
v2.2: 改善找元素方法, 增加 wait 機制
v2.1: 增加開網頁check機制 與縮短試元素的方法, fill 增加先清空的動作
v2.0: 語法修改方便直接套用 Selenium IDE 產出程式碼
v1.1: 增加 ScreenCap 功能, 補足示範的說明
v1.0: 第一個release 的版本

'''

'''
模組化用法

把 UIPogo.py 放在和你要一起執行的 python 目錄 或其他能 import 的路徑

加入這句即可
from UIPogo import *

Bopen() 要改為 driver = Bopen() , 雖不改也可, 但一些用到 driver 的語法會失效

Bcap2 增強full screen cap 的能力 !! 需要 pillow 模組 !! 語法為 Bcap2(driver,'檔名')

'''


'''
v2.9 後新功能說明

Bclick ('變數') 舊的運作方式, 如查找失敗會直接帶 BclickT
BclickT ('目標文字','目標編號')
BclickTI ('目標文字','目標後選用順位','目標編號') 針對 input 目標選用, 如打勾或圓形的選項
BclickTB ('目標文字','目標後選用順位','目標編號') 針對 按紐 目標選用

'目標編號' 用來微調所有 BxxxT 的功能, 使用時必需帶所有參數才會生效, 用來選定符合條件的第 ? 筆目標


'''

from subprocess import Popen, PIPE
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time,re,os,sys,platform
from datetime import datetime

pyver = sys.version_info[0] # Python 主版本

Webwaittime = 10 # 開網頁元素的等待時間

def Bsleep(num):
    print('\n[' + str (datetime.now()) + '] Bsleep | ' + str(num))  
    time.sleep(num)
    print('-Success')  


def ErrorCon():
    print('[' + str (datetime.now()) + '] Error: Action Fail !! STOP the program now....')
    raise SystemExit

def Bopen(): #開 Browser
    info1 = '\n[' + str (datetime.now()) + '] Bopen'
    print(info1)
    
    global driver
    #driver = webdriver.Firefox()
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    driver.implicitly_wait(Webwaittime) #找元素最長等待時間


    return driver

def Bvisit(url): # 打開 url
    info1 = '\n[' + str (datetime.now()) + '] Bvisit | ' + url
    print(info1)


    driver.get(url)
    if 'aboutNetError' in driver.page_source:
        print('-Error: ' + url)
        driver.quit()        
    else:
        print('-Wait 1 sec for Page load...')
        time.sleep(1)
        print('-Success: ' + url)    
        
def BvisitD(driver,url):
    info1 = '\n[' + str (datetime.now()) + '] Bvisit | ' + url
    print(info1)


    driver.get(url)
    if 'aboutNetError' in driver.page_source:
        print('-Error: ' + url)
        driver.quit()        
    else:
        print('-Wait 1 sec for Page load...')
        time.sleep(1)
        print('-Success: ' + url)    

def Bquit(): # 關 driver
    info1 = '\n[' + str (datetime.now()) + '] Bquit'
    print(info1)

    driver.quit()


def BquitD(driver): # 關 driver
    info1 = '\n[' + str (datetime.now()) + '] Bquit'
    print(info1)

    driver.quit()


def Felement(element): #以 CSS ->  Xpath -> name -> link_text 試 網頁元素, 存在的話回傳
    retries = Webwaittime    
    while retries:
        driver.implicitly_wait(0)        
        try:
            e1=driver.find_element_by_css_selector(element)
            print('-Success Find CSS: ' + element)
        except:            
            try:
                e1=driver.find_element_by_xpath(element)
                print('-Success Find xpath: ' + element)
            except:
                try:
                    e1=driver.find_element_by_name(element)
                    print('-Success Find name: ' + element)
                except:
                    try:
                        e1=driver.find_element_by_id(element)
                        print('-Success Find id: ' + element)
                    except:
                        try:
                            e1=driver.find_element_by_link_text(element)
                            print('-Success Find link text: ' + element)
                        except:
                            e1 = 0
                            print('-Fail Find: ' + element) 
                    
        if e1 != 0 and e1.is_displayed():
            highlight(e1)
            return e1
            break                       
        retries = retries - 1        
        time.sleep(0.5)
    driver.implicitly_wait(Webwaittime)
    return 0


def FelementD(driver,element): #以 CSS ->  Xpath -> name -> link_text 試 網頁元素, 存在的話回傳
    retries = Webwaittime    
    while retries:
        driver.implicitly_wait(0)        
        try:
            e1=driver.find_element_by_css_selector(element)
            print('-Success Find CSS: ' + element)
        except:            
            try:
                e1=driver.find_element_by_xpath(element)
                print('-Success Find xpath: ' + element)
            except:
                try:
                    e1=driver.find_element_by_name(element)
                    print('-Success Find name: ' + element)
                except:
                    try:
                        e1=driver.find_element_by_id(element)
                        print('-Success Find id: ' + element)
                    except:
                        try:
                            e1=driver.find_element_by_link_text(element)
                            print('-Success Find link text: ' + element)
                        except:
                            e1 = 0
                            print('-Fail Find: ' + element) 
                    
        if e1 != 0 and e1.is_displayed():
            highlight(e1)
            return e1
            break                       
        retries = retries - 1        
        time.sleep(0.5)
    driver.implicitly_wait(Webwaittime)
    return 0
        

        
def Bfill(element,txt): #填入元素 欄位, 第一個變數找元素 第二個變數是要填入的資料, 成功回傳 1 , 失敗回傳 0 
    return Bxxx ('Bfill', element,txt)

def BfillD(driver,element,txt): #填入元素 欄位, 第一個變數找元素 第二個變數是要填入的資料, 成功回傳 1 , 失敗回傳 0 
    return BxxxD (driver,'Bfill', element,txt)

def SBfill(element,txt):
    if Bxxx ('Bfill', element,txt) == 0:
        ErrorCon()
    else:
        return 1

def Bkey(element,txt): #填入元素 欄位, 第一個變數找元素 第二個變數是要填入的資料, 成功回傳 1 , 失敗回傳 0 
    return Bxxx ('Bkey', element,txt)

def BkeyD(driver, element,txt): #填入元素 欄位, 第一個變數找元素 第二個變數是要填入的資料, 成功回傳 1 , 失敗回傳 0 
    return BxxxD (driver,'Bkey', element,txt)

def SBkey(element,txt):
    if Bxxx ('Bkey', element,txt) == 0:
        ErrorCon()
    else:
        return 1


def Bclick(element): # Click 元素, 標準操作, 成功回傳 1 , 失敗回傳 0 
    return Bxxx ('Bclick', element)

def BclickD(driver,element): # Click 元素, 標準操作, 成功回傳 1 , 失敗回傳 0 
    return BxxxD (driver,'Bclick', element)

def SBclick(element): # Click 元素, 標準操作, 成功回傳 1 , 失敗回傳 0 
    if Bxxx ('Bclick', element) == 0:
        ErrorCon()
    else:
        return 1
    
def Bcheck(element): #勾選 元素 ,成功回傳 1 , 失敗回傳 0
    return Bxxx ('Bcheck', element)

    
def BcheckD(driver,element): #勾選 元素 ,成功回傳 1 , 失敗回傳 0
    return BxxxD (driver,'Bcheck', element)

def SBcheck(element): #勾選 元素 ,成功回傳 1 , 失敗回傳 0
    if Bxxx ('Bcheck', element) == 0:
        ErrorCon()
    else:
        return 1        

def Bncheck(element): #取消 勾選 元素,成功回傳 1 , 失敗回傳 0
    return Bxxx ('Bncheck', element)

def BncheckD(driver,element): #取消 勾選 元素,成功回傳 1 , 失敗回傳 0
    return BxxxD (driver,'Bncheck', element)

def SBncheck(element): #取消 勾選 元素,成功回傳 1 , 失敗回傳 0
    if Bxxx ('Bncheck', element) == 0:
        ErrorCon()
    else:
        return 1
    
def Bdrop(point1,point2): #拖->放 元素, 第一個變數為元素開始位置 第二個變數為元素放開位置,成功回傳 1 , 失敗回傳 0

    info1 = '\n[' + str (datetime.now()) + '] Bdrop | ' + point1 + ' | ' + point2
    print(info1)
    
    p1 = Felement(point1)
    if p1 == 0:        
        info = '--Error: "' + point1 + '" not found'
        print(info)
        return 0



    p2 = Felement(point2)
    if p1 == 0:
        info = '--Error: "' + point2 + '" not found'
        print(info)
        return 0

    else: 
        action_chains = ActionChains(driver)
        try:
            action_chains.drag_and_drop(p1, p2).perform()
            info = '--Success: ' + point1 + ' & ' + point2 + ' can drag and drop'
            print(info)
            return 1
        except:
            info = '--Error: ' + point1 + ' & ' + point2 + ' can not drag and drop'
            print(info)
            return 0

def BdropD(driver,point1,point2): #拖->放 元素, 第一個變數為元素開始位置 第二個變數為元素放開位置,成功回傳 1 , 失敗回傳 0

    info1 = '\n[' + str (datetime.now()) + '] Bdrop | ' + point1 + ' | ' + point2
    print(info1)
    
    p1 = FelementD(driver,point1)
    if p1 == 0:        
        info = '--Error: "' + point1 + '" not found'
        print(info)
        return 0



    p2 = FelementD(driver,point2)
    if p1 == 0:
        info = '--Error: "' + point2 + '" not found'
        print(info)
        return 0

    else: 
        action_chains = ActionChains(driver)
        try:
            action_chains.drag_and_drop(p1, p2).perform()
            info = '--Success: ' + point1 + ' & ' + point2 + ' can drag and drop'
            print(info)
            return 1
        except:
            info = '--Error: ' + point1 + ' & ' + point2 + ' can not drag and drop'
            print(info)
            return 0




def SBdrop(point1,point2):
    if Bdrop(point1,point2) == 0:
        ErrorCon()
    else:
        return 1
        

def Bdrop_offset(point1,px1,py1): #用 畫素XY位置 拖->放 元素, 第一個變數為元素開始位置 第二個變數為X軸變動數, 第三個變數為Y軸變動數,成功回傳 1 , 失敗回傳 0

    info1 = '\n[' + str (datetime.now()) + '] Bdrop | ' + point1 + ' | ' + str(px1) + ' | ' + str(py1)
    print(info1)
    
    p1 = Felement(point1)
    if p1 == 0:
        return 0
    else:

        action_chains = ActionChains(driver)
        try:
            action_chains.drag_and_drop_by_offset(p1, px1, py1).perform()
            info = '--Success: ' + point1 + ' can drag and drop via offset'
            print(info)
            return 1
        except Exception as e:
            print(e)
            info = '--Error: ' + point1 + ' can not drag and drop via offset'
            print(info)
            return 0


def Bdrop_offsetD(driver,point1,px1,py1): #用 畫素XY位置 拖->放 元素, 第一個變數為元素開始位置 第二個變數為X軸變動數, 第三個變數為Y軸變動數,成功回傳 1 , 失敗回傳 0

    info1 = '\n[' + str (datetime.now()) + '] Bdrop | ' + point1 + ' | ' + str(px1) + ' | ' + str(py1)
    print(info1)
    
    p1 = FelementD(driver,point1)
    if p1 == 0:
        return 0
    else:

        action_chains = ActionChains(driver)
        try:
            action_chains.drag_and_drop_by_offset(p1, px1, py1).perform()
            info = '--Success: ' + point1 + ' can drag and drop via offset'
            print(info)
            return 1
        except Exception as e:
            print(e)
            info = '--Error: ' + point1 + ' can not drag and drop via offset'
            print(info)
            return 0


def SBdrop_offset(point1,px1,py1):
    if Bdrop_offset(point1,px1,py1) ==0:
           ErrorCon()
    else:
        return 1

def Bcap(filename): #抓driver 畫面成圖檔, 變數就是檔名要加 .png
    info1 = '\n[' + str (datetime.now()) + '] Bcap | ' + filename
    print(info1)
    
    driver.save_screenshot(filename)

def Bcap2(driver, filename):
    from PIL import Image

    info1 = '\n[' + str (datetime.now()) + '] Bcap2 | ' + filename
    print(info1)

    print("Starting full page screenshot workaround ...")

    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    print(("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,viewport_width,viewport_height)))
    rectangles = []

    i = 0
    while i < total_height:
        ii = 0
        top_height = i + viewport_height

        if top_height > total_height:
            top_height = total_height

        while ii < total_width:
            top_width = ii + viewport_width

            if top_width > total_width:
                top_width = total_width

            print(("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height)))
            rectangles.append((ii, i, top_width,top_height))

            ii = ii + viewport_width

        i = i + viewport_height

    stitched_image = Image.new('RGB', (total_width, total_height))
    previous = None
    part = 0

    for rectangle in rectangles:
        if not previous is None:
            driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
            time.sleep(0.2)
            '''
            #留著以免日後又做了上面的控制Bar, 方便參考
            try:
                driver.execute_script("document.getElementById('topnav').setAttribute('style', 'position: absolute; top: 0px;');")
            except:
                print 'no topnav'
            '''
            time.sleep(0.2)
            print(("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1])))
            time.sleep(0.2)

        file_name = "part_{0}.png".format(part)
        print(("Capturing {0} ...".format(file_name)))

        driver.get_screenshot_as_file(file_name)
        screenshot = Image.open(file_name)

        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])

        print(("Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1])))
        stitched_image.paste(screenshot, offset)

        del screenshot
        os.remove(file_name)
        part = part + 1
        previous = rectangle

    stitched_image.save(filename)
    print("Finishing full page screenshot workaround...")
    return True


    
    
def Bwait(element,ctime = 3): # 等待某元素出現, 試3次, 間隔2秒, 成功回傳 1 , 失敗回傳 0
    info1 = '\n[' + str (datetime.now()) + '] Bwait | ' + element + ' | ' + str(ctime)
    print(info1)
    
    for x in range(ctime):
        e1 = Felement(element)    
        if e1 != 0:
            print('--Wait success: ' + element)
            return 1
            break
        else:
            print('--Wait Error: ' + element + ' , 2 sec more try !! ' + str(x+1) +'/3')            
            time.sleep(2)
    return 0

def BwaitD(driver,element,ctime = 3): # 等待某元素出現, 試3次, 間隔2秒, 成功回傳 1 , 失敗回傳 0
    info1 = '\n[' + str (datetime.now()) + '] Bwait | ' + element + ' | ' + str(ctime)
    print(info1)
    
    for x in range(ctime):
        e1 = FelementD(driver,element)    
        if e1 != 0:
            print('--Wait success: ' + element)
            return 1
            break
        else:
            print('--Wait Error: ' + element + ' , 2 sec more try !! ' + str(x+1) +'/3')            
            time.sleep(2)
    return 0



def SBwait(element,ctime = 3):
    if Bwait(element,ctime) == 0:
           ErrorCon()
    else:
        return 1
        
    
def Bwait_text(text,ctime = 3): # 等待某字串出現, 試3次, 間隔2秒, 成功回傳 1 , 失敗回傳 0
    info1 = '\n[' + str (datetime.now()) + '] Bwait_text | ' + text + ' | ' + str(ctime)
    print(info1)
    time.sleep(1)
    for x in range(ctime):         
        if text in driver.page_source:
            print('--Wait success: ' + text)
            return 1           
        else:
            print('--Wait Error: ' + text + ' , 2 sec more try !! ' + str(x+1) +'/3')            
            time.sleep(2)
    return 0

def Bwait_textD(driver,text,ctime = 3): # 等待某字串出現, 試3次, 間隔2秒, 成功回傳 1 , 失敗回傳 0
    info1 = '\n[' + str (datetime.now()) + '] Bwait_text | ' + text + ' | ' + str(ctime)
    print(info1)
    time.sleep(1)
    for x in range(ctime):         
        if text in driver.page_source:
            print('--Wait success: ' + text)
            return 1           
        else:
            print('--Wait Error: ' + text + ' , 2 sec more try !! ' + str(x+1) +'/3')            
            time.sleep(2)
    return 0


def SBwait_text(text,ctime = 3):
    if Bwait_text(text,ctime) == 0:
           ErrorCon()
    else:
        return 1
    
  
def Btext(text): # 找字串機制, 成功回傳 1 , 失敗回傳 0
    info1 = '\n[' + str (datetime.now()) + '] Btext | ' + text
    print(info1)
    
    if text in driver.page_source:
        print('-Success Find Text: ' + text)
        return 1
    else:
        print('-Fail Find Text: ' + text)
        return 0

  
def BtextD(driver,text): # 找字串機制, 成功回傳 1 , 失敗回傳 0
    info1 = '\n[' + str (datetime.now()) + '] Btext | ' + text
    print(info1)
    
    if text in driver.page_source:
        print('-Success Find Text: ' + text)
        return 1
    else:
        print('-Fail Find Text: ' + text)
        return 0


def SBtext(text):
    if Btext(text) == 0:
           ErrorCon()
    else:
        return 1


def Battribute(element): # 取得某元素的值, 回傳
    info1 = '\n[' + str (datetime.now()) + '] Battribute | ' + element
    print(info1)
    
    e1 = Felement(element)
    if e1 == 0:  
        info = '--Error: "' + element + '" not found'
        print(info)
        return 0

    else:
        try:        
            v1 = e1.get_attribute('value')
            info = 'Success: find value '  + v1 + ' from ' + element
            return v1
        except:
            info = 'Error: can not find value from '  +element
            return 0


def BattributeD(driver,element): # 取得某元素的值, 回傳
    info1 = '\n[' + str (datetime.now()) + '] Battribute | ' + element
    print(info1)
    
    e1 = FelementD(driver,element)
    if e1 == 0:  
        info = '--Error: "' + element + '" not found'
        print(info)
        return 0

    else:
        try:        
            v1 = e1.get_attribute('value')
            info = 'Success: find value '  + v1 + ' from ' + element
            return v1
        except:
            info = 'Error: can not find value from '  +element
            return 0

        
def PingCheck(ip): # ping ip , 成功回傳 1 , 失敗回傳 0

    if platform.system() == 'Windows':        
        runtest = Popen('ping -n 1 '+ip , stdout=PIPE)        
        chktest = re.search('= (.*)ms',runtest.stdout.read().decode('big5'))
        
        if pyver is 2: #Python 2 相容
            chktest = re.search('= (.*)ms',runtest.stdout.read())
            
    elif platform.system() == 'Linux':
        chktest = 0   

        runtest = Popen('ping -c 1 ' + ip ,shell = True).wait()
        if runtest == 0:
            chktest = 1
    
    if chktest:
        print(ip + ' ping Check Success !!')
        return 1
    else:
        print(ip + ' ping Check Fail..')
        return 0

def PingWait(ip,num = 10): # 2015/10/21 PingCheck 的延伸應用, 每3秒 ping ip, 30 秒內成功續執行, 否則中斷程式
    info1 = '\n[' + str (datetime.now()) + '] PingWait | ' + ip + ' | ' + str(num)
    print(info1)
    
    for x in range (num):            
        if PingCheck(ip):                
            break              
        print(str(x+1) +' Fail, Wait 3 sec retry...')
        time.sleep(3)
    if x == (num -1) :
        print(ip + ' ping Fail more than 30 sec!! something wrong !!')
        print('Ping Wait Error !! Test Stop Now...')
        raise SystemExit
        
    else:
        print(ip + ' Wait Success!!')   

def FelementT(element, num='1', mod='i'): # 依文字查找 元素, 變數1 '要查的文字' 變數2 查到後的第幾個元素 變數3 模式, 所有變數都要加 ''查次一層級
    if mod == 'i':
        mode = 'input'
    elif mod == 'b':
        mode = 'button'
    elif mod == 't':
        mode = 'textarea'
    elif mod == 'o':
        mode = 'option'        
    e1 = driver.find_elements_by_xpath("//*[.='" + element + "']/following::" + mode + "[" + num + "]")
    if not e1:
        print('-Fail Find Text: "' + element + '" | Number: ' + num + ' | Mode: ' + mode)
        return 0
    print('-Success Find Text: "' + element + '" | Number: ' + num + ' | Mode: ' + mode+ ' | Point: ' +  str(len(e1)))

    
    #print e1
    return e1

def FelementTD(driver,element, num='1', mod='i'): # 依文字查找 元素, 變數1 '要查的文字' 變數2 查到後的第幾個元素 變數3 模式, 所有變數都要加 ''查次一層級
    if mod == 'i':
        mode = 'input'
    elif mod == 'b':
        mode = 'button'
    elif mod == 't':
        mode = 'textarea'
    elif mod == 'o':
        mode = 'option'        
    e1 = driver.find_elements_by_xpath("//*[.='" + element + "']/following::" + mode + "[" + num + "]")
    if not e1:
        print('-Fail Find Text: "' + element + '" | Number: ' + num + ' | Mode: ' + mode)
        return 0
    print('-Success Find Text: "' + element + '" | Number: ' + num + ' | Mode: ' + mode+ ' | Point: ' +  str(len(e1)))

    
    #print e1
    return e1



def FelementT0 (element, num='1', mod='i'): # 依文字查找 元素, 變數1 '要查的文字' 變數2 查到後的第幾個元素 變數3 模式, 所有變數都要加 '' 查同一層級
    if mod == 'i':
        mode = 'input'
    elif mod == 'b':
        mode = 'button'
    elif mod == 't':
        mode = 'textarea'
    elif mod == 'o':
        mode = 'option'                
    e1 = driver.find_elements_by_xpath("//*[contains(text(),'" + element + "')]/"+ mode + "[" + num + "]" )
    if not e1:
        print('-Fail Find Text: "' + element + '" | Number: ' + num + ' | Mode: ' + mode)
        return 0
    print('-Success Find Text: "' + element + '" | Number: ' + num + ' | Mode: ' + mode+ ' | Point: ' +  str(len(e1)))
    
    #print e1
    return e1

def FelementT0D (driver,element, num='1', mod='i'): # 依文字查找 元素, 變數1 '要查的文字' 變數2 查到後的第幾個元素 變數3 模式, 所有變數都要加 '' 查同一層級
    if mod == 'i':
        mode = 'input'
    elif mod == 'b':
        mode = 'button'
    elif mod == 't':
        mode = 'textarea'
    elif mod == 'o':
        mode = 'option'                
    e1 = driver.find_elements_by_xpath("//*[contains(text(),'" + element + "')]/"+ mode + "[" + num + "]" )
    if not e1:
        print('-Fail Find Text: "' + element + '" | Number: ' + num + ' | Mode: ' + mode)
        return 0
    print('-Success Find Text: "' + element + '" | Number: ' + num + ' | Mode: ' + mode+ ' | Point: ' +  str(len(e1)))
    
    #print e1
    return e1    

def BfillT (element, txt, num='1',adj='0',adj2='A'):  
    '''
    for Input 依文字查找 元素 後填入值
    element 要查找的文字
    txt 查到後要填入的字
    num 目標序
    adj 符合目標序的第幾個元素 0 是全部
    adj2 查找level A是自動, 0是同一level , 1是次一level 

    所有變數都要加 ''
    '''
    return BxxxT ('BfillT', element, num, adj, adj2,txt)


def BfillTD (driver,element, txt, num='1',adj='0',adj2='A'):  
    '''
    for Input 依文字查找 元素 後填入值
    element 要查找的文字
    txt 查到後要填入的字
    num 目標序
    adj 符合目標序的第幾個元素 0 是全部
    adj2 查找level A是自動, 0是同一level , 1是次一level 

    所有變數都要加 ''
    '''
    return BxxxTD (driver, 'BfillT', element, num, adj, adj2,txt)

def SBfillT (element, txt, num='1',adj='0',adj2='A'):  
    if BxxxT ('BfillT', element, num, adj, adj2,txt) == 0:
           ErrorCon()
    else:
        return 1

def BfillTT (element, txt, num='1',adj='0',adj2='A'):
    '''
    for Textarea 依文字查找 元素 後填入值
    element 要查找的文字
    txt 查到後要填入的字
    num 目標序
    adj 符合目標序的第幾個元素 0 是全部
    adj2 查找level A是自動, 0是同一level , 1是次一level 

    所有變數都要加 ''
    '''    
    return BxxxT ('BfillTT', element, num, adj, adj2,txt)

def BfillTTD (driver,element, txt, num='1',adj='0',adj2='A'):
    '''
    for Textarea 依文字查找 元素 後填入值
    element 要查找的文字
    txt 查到後要填入的字
    num 目標序
    adj 符合目標序的第幾個元素 0 是全部
    adj2 查找level A是自動, 0是同一level , 1是次一level 

    所有變數都要加 ''
    '''    
    return BxxxTD (driver,'BfillTT', element, num, adj, adj2,txt)

def SBfillTT (element, txt, num='1',adj='0',adj2='A'):
    if BxxxT ('BfillTT', element, num, adj, adj2,txt) == 0:
           ErrorCon()
    else:
        return 1

def BclickT (element,adj='0'): # 依文字查找 元素 全部按下去 , element '要查的文字'  adj 查到後的第幾個元素 , 所有變數都要加 ''
    info1 = '\n[' + str (datetime.now()) + '] BclickT | ' + element + ' | adj= ' + adj
    print(info1)
    try:     
        e1 = driver.find_elements_by_xpath("(//*[contains(text(), '" + element + "')])")
        #print e1
        if not e1:            
            print('-Fail Find Text: "' + element)             
            return 0              

        print('-Success Find Text: "' + element + ' | Point: ' +  str(len(e1)))

        if adj != '0':
            x = int(adj)-1
            print('--Try element s number: ' + str(x+1))
            try:
                highlight(e1[x])
                e1[x].click()                 
                info = '--Success: "' + element + '" | Number: ' + str(x+1) + ' can click'
                print(info)
                
                return 1
                
            except:
                info = '--Error: "' + element + '" | Number: ' + str(x+1) + ' can not click'
                print(info)

                return 0
            

            
        else:
            x = 0
            y = len(e1)
            count = 0

            for i in e1:
                print('--Try element s number: ' + str(x+1))
                try:
                    highlight(e1[x])
                    e1[x].click()                 
                    info = '--Success: "' + element + '" | Number: ' + str(x+1) + ' can click'
                    print(info)
                    count += 1

                    
                except:
                    info = '--Error: "' + element + '" | Number: ' + str(x+1) + ' can not click'
                    print(info)
                        
                x +=1
                
            if count != 0:

                info = '-Success: "' + element + '" can click | Total Point: ' + str(count)
                print(info)
                return 1
            else:
                return 0

                
    
    except:
        info = '--Error: "' + element + '" can not click'        
        print(info)
        return 0

def BclickTD (driver,element,adj='0'): # 依文字查找 元素 全部按下去 , element '要查的文字'  adj 查到後的第幾個元素 , 所有變數都要加 ''
    info1 = '\n[' + str (datetime.now()) + '] BclickT | ' + element + ' | adj= ' + adj
    print(info1)
    try:     
        e1 = driver.find_elements_by_xpath("(//*[contains(text(), '" + element + "')])")
        #print e1
        if not e1:            
            print('-Fail Find Text: "' + element)             
            return 0              

        print('-Success Find Text: "' + element + ' | Point: ' +  str(len(e1)))

        if adj != '0':
            x = int(adj)-1
            print('--Try element s number: ' + str(x+1))
            try:
                highlight(e1[x])
                e1[x].click()                 
                info = '--Success: "' + element + '" | Number: ' + str(x+1) + ' can click'
                print(info)
                
                return 1
                
            except:
                info = '--Error: "' + element + '" | Number: ' + str(x+1) + ' can not click'
                print(info)

                return 0
            

            
        else:
            x = 0
            y = len(e1)
            count = 0

            for i in e1:
                print('--Try element s number: ' + str(x+1))
                try:
                    highlight(e1[x])
                    e1[x].click()                 
                    info = '--Success: "' + element + '" | Number: ' + str(x+1) + ' can click'
                    print(info)
                    count += 1

                    
                except:
                    info = '--Error: "' + element + '" | Number: ' + str(x+1) + ' can not click'
                    print(info)
                        
                x +=1
                
            if count != 0:

                info = '-Success: "' + element + '" can click | Total Point: ' + str(count)
                print(info)
                return 1
            else:
                return 0

                
    
    except:
        info = '--Error: "' + element + '" can not click'        
        print(info)
        return 0


def SBclickT (element,adj='0'):
    if BclickT (element,adj) == 0:
           ErrorCon()
    else:
        return 1        

def BclickTI (element, num='1',adj='0',adj2='A' ):
    '''
    for input 依文字查找 元素 按下去
    element 要查找的文字
    num 目標序
    adj 符合目標序的第幾個元素 0 是全部
    adj2 查找level A是自動, 0是同一level , 1是次一level 

    所有變數都要加 ''
    '''    
    return BxxxT ('BclickTI', element, num, adj, adj2)

def BclickTID (driver,element, num='1',adj='0',adj2='A' ):
    '''
    for input 依文字查找 元素 按下去
    element 要查找的文字
    num 目標序
    adj 符合目標序的第幾個元素 0 是全部
    adj2 查找level A是自動, 0是同一level , 1是次一level 

    所有變數都要加 ''
    '''    
    return BxxxTD (driver,'BclickTI', element, num, adj, adj2)

def SBclickTI (element, num='1',adj='0',adj2='A' ):
    if BxxxT ('BclickTI', element, num, adj, adj2) == 0:
           ErrorCon()
    else:
        return 1

def BclickTB (element, num='1',adj='0',adj2='A'): 
    '''
    for button 依文字查找 元素 按下去
    element 要查找的文字
    num 目標序
    adj 符合目標序的第幾個元素 0 是全部
    adj2 查找level A是自動, 0是同一level , 1是次一level 

    所有變數都要加 ''
    '''    
    return BxxxT ('BclickTB', element, num, adj, adj2)

def BclickTBD (driver, element, num='1',adj='0',adj2='A'): 
    '''
    for button 依文字查找 元素 按下去
    element 要查找的文字
    num 目標序
    adj 符合目標序的第幾個元素 0 是全部
    adj2 查找level A是自動, 0是同一level , 1是次一level 

    所有變數都要加 ''
    '''    
    return BxxxTD (driver,'BclickTB', element, num, adj, adj2)


def SBclickTB (element, num='1',adj='0',adj2='A'): 
    if BxxxT ('BclickTB', element, num, adj, adj2) == 0:
           ErrorCon()
    else:
        return 1


def BclickTO (element, num='1',adj='0',adj2='A'): 
    '''
    for button 依文字查找 元素 按下去
    element 要查找的文字
    num 目標序
    adj 符合目標序的第幾個元素 0 是全部
    adj2 查找level A是自動, 0是同一level , 1是次一level 

    所有變數都要加 ''
    '''    
    return BxxxT ('BclickTO', element, num, adj, adj2)

def BclickTOD (driver,element, num='1',adj='0',adj2='A'): 
    '''
    for button 依文字查找 元素 按下去
    element 要查找的文字
    num 目標序
    adj 符合目標序的第幾個元素 0 是全部
    adj2 查找level A是自動, 0是同一level , 1是次一level 

    所有變數都要加 ''
    '''    
    return BxxxTD (driver,'BclickTO', element, num, adj, adj2)


def SBclickTO (element, num='1',adj='0',adj2='A'): 
    if BxxxT ('BclickTO', element, num, adj, adj2) == 0:
           ErrorCon()
    else:
        return 1
    
def BcheckT (element, num='1',adj='0',adj2='A'): # 依文字查找 元素 後鈎選 , 變數1 '要查的文字'  變數2 查到後的第幾個元素 , 所有變數都要加 '' 
    '''
    for input 依文字查找 元素 勾選
    element 要查找的文字
    num 目標序
    adj 符合目標序的第幾個元素 0 是全部
    adj2 查找level A是自動, 0是同一level , 1是次一level 

    所有變數都要加 ''
    '''    
    return BxxxT ('BcheckT', element, num, adj, adj2)

    
def BcheckTD (driver,element, num='1',adj='0',adj2='A'): # 依文字查找 元素 後鈎選 , 變數1 '要查的文字'  變數2 查到後的第幾個元素 , 所有變數都要加 '' 
    '''
    for input 依文字查找 元素 勾選
    element 要查找的文字
    num 目標序
    adj 符合目標序的第幾個元素 0 是全部
    adj2 查找level A是自動, 0是同一level , 1是次一level 

    所有變數都要加 ''
    '''    
    return BxxxTD (driver,'BcheckT', element, num, adj, adj2)


def SBcheckT (element, num='1',adj='0',adj2='A'): # 依文字查找 元素 後鈎選 , 變數1 '要查的文字'  變數2 查到後的第幾個元素 , 所有變數都要加 '' 
    if BxxxT ('BcheckT', element, num, adj, adj2) == 0:
           ErrorCon()
    else:
        return 1


        
def BncheckT (element, num='1',adj='0',adj2='A'): 
    '''
    for input 依文字查找 元素 取消勾選
    element 要查找的文字
    num 目標序
    adj 符合目標序的第幾個元素 0 是全部
    adj2 查找level A是自動, 0是同一level , 1是次一level 

    所有變數都要加 ''
    '''
    return BxxxT ('BncheckT', element, num, adj, adj2)

        
def BncheckTD (driver,element, num='1',adj='0',adj2='A'): 
    '''
    for input 依文字查找 元素 取消勾選
    element 要查找的文字
    num 目標序
    adj 符合目標序的第幾個元素 0 是全部
    adj2 查找level A是自動, 0是同一level , 1是次一level 

    所有變數都要加 ''
    '''
    return BxxxTD (driver,'BncheckT', element, num, adj, adj2)

def SBncheckT (element, num='1',adj='0',adj2='A'): 
    if BxxxT ('BncheckT', element, num, adj, adj2) == 0:
           ErrorCon()
    else:
        return 1
   
def BxxxT (mode, element, num='1',adj='0',adj2='A', txt = ''):
    
    info1 = '\n[' + str (datetime.now()) + '] ' + mode + ' | ' + element + ' | ' + txt + ' | num= ' + num + ' | adj= ' + adj + ' | adj2= ' + adj2
    print(info1)

    c1c = 666
    if mode == 'BfillT':
        mod = 'i'
        msg1 = 'fill: "' + txt + '"'
        

    elif mode == 'BfillTT':
        mod = 't'
        msg1 = 'fill: "' + txt + '"'
        
       
    elif mode == 'BclickTI':
        mod = 'i'
        msg1 = 'click'
        
    elif mode == 'BclickTB':
        mod = 'b'
        msg1 = 'click'
                
    elif mode == 'BclickTO':
        mod = 'o'
        msg1 = 'click'
        
    elif mode == 'BcheckT':
        mod = 'i'
        msg1 = 'check'
        c1c = 0
        
        
    elif mode == 'BncheckT':
        mod = 'i'
        msg1 = 'disable check'
        c1c = 1
       
    else:
        info = '-Error: "' + mode + '" not support!!'
        return 0

       


    if adj2 == '0':
        e1 = FelementT0( element , num , mod)
        if e1 == 0:
            print('-Fail ' + mode + ' adj2=0')
            return 0
    elif adj2 == '1':
        e1 = FelementT( element , num , mod)
        if e1 == 0:
            print('-Fail ' + mode + ' adj2=1')
            return 0    
    else:    
        e1 = FelementT0( element , num , mod)
        if e1 == 0:
            print('-Fail ' + mode + ' Auto Mode adj2=0 , Try adj2=1 now..')
            e1 = FelementT( element , num , mod)
            if e1 == 0:
                print('-Fail ' + mode + ' Auto Mode adj2=0 and adj2=1')
                return 0


    try:
        
        if adj != '0':
            
            x = int(adj)-1
            
            print('-Try element s number: ' + str(x+1))

            highlight(e1[x])
            
            c1 = 666
            if mode == 'BcheckT' or mode == 'BncheckT':      
                try:
                    
                    c1 = e1[x].is_selected()
                except:
                    c1 = 666

            if c1 == c1c:
                
                try:
                    if mode == 'BfillT' or mode == 'BfillTT':                        
                        e1[x].clear()
                        e1[x].send_keys(txt)
                    else:
                        e1[x].click()
                    info = '-Success: "' + element + '" | Number: ' + str(x+1) + ' can ' + msg1
                    print(info)                    

                    return 1

                except:
                    info = '-Error: "' + element + '" | Number: ' + str(x+1) + ' can not ' + msg1
                    print(info)

                    return 0

        else:
            x = 0
            y = len(e1)
            count = 0
            
            for i in e1:
                print('-Try element s number: ' + str(x+1))

                highlight(e1[x])
                
                c1 = 666
                if mode == 'BcheckT' or mode == 'BncheckT':      
                    try:
                        c1 = e1[x].is_selected()
                    except:
                        c1 = 666

                if c1 == c1c:
                    try:
                        if mode == 'BfillT' or mode == 'BfillTT':
                            e1[x].clear()
                            e1[x].send_keys(txt)
                        else:
                            e1[x].click()
                        info = '-Success: "' + element + '" | Number: ' + str(x+1) + ' can ' + msg1
                        print(info)
                        count += 1

                    except:
                        info = '-Error: "' + element + '" | Number: ' + str(x+1) + ' can not ' + msg1
                        print(info)
                    x +=1
                       

            if count != 0:

                info = '-Success: "' + element + '" can ' + msg1 + ' | Total Point: ' + str(count)
                print(info)
                return 1
            else:
                return 0 

    except:        
        info = '-Error: "' + element + '" can not ' + msg1
        print(info)
        return 0

def BxxxTD (driver, mode, element, num='1',adj='0',adj2='A', txt = ''):
    
    info1 = '\n[' + str (datetime.now()) + '] ' + mode + ' | ' + element + ' | ' + txt + ' | num= ' + num + ' | adj= ' + adj + ' | adj2= ' + adj2
    print(info1)

    c1c = 666
    if mode == 'BfillT':
        mod = 'i'
        msg1 = 'fill: "' + txt + '"'
        

    elif mode == 'BfillTT':
        mod = 't'
        msg1 = 'fill: "' + txt + '"'
        
       
    elif mode == 'BclickTI':
        mod = 'i'
        msg1 = 'click'
        
    elif mode == 'BclickTB':
        mod = 'b'
        msg1 = 'click'
                
    elif mode == 'BclickTO':
        mod = 'o'
        msg1 = 'click'
        
    elif mode == 'BcheckT':
        mod = 'i'
        msg1 = 'check'
        c1c = 0
        
        
    elif mode == 'BncheckT':
        mod = 'i'
        msg1 = 'disable check'
        c1c = 1
       
    else:
        info = '-Error: "' + mode + '" not support!!'
        return 0

       


    if adj2 == '0':
        e1 = FelementT0D(driver, element , num , mod)
        if e1 == 0:
            print('-Fail ' + mode + ' adj2=0')
            return 0
    elif adj2 == '1':
        e1 = FelementTD(driver, element , num , mod)
        if e1 == 0:
            print('-Fail ' + mode + ' adj2=1')
            return 0    
    else:    
        e1 = FelementT0D(driver, element , num , mod)
        if e1 == 0:
            print('-Fail ' + mode + ' Auto Mode adj2=0 , Try adj2=1 now..')
            e1 = FelementTD(driver, element , num , mod)
            if e1 == 0:
                print('-Fail ' + mode + ' Auto Mode adj2=0 and adj2=1')
                return 0


    try:
        
        if adj != '0':
            
            x = int(adj)-1
            
            print('-Try element s number: ' + str(x+1))

            highlight(e1[x])
            
            c1 = 666
            if mode == 'BcheckT' or mode == 'BncheckT':      
                try:
                    
                    c1 = e1[x].is_selected()
                except:
                    c1 = 666

            if c1 == c1c:
                
                try:
                    if mode == 'BfillT' or mode == 'BfillTT':                        
                        e1[x].clear()
                        e1[x].send_keys(txt)
                    else:
                        e1[x].click()
                    info = '-Success: "' + element + '" | Number: ' + str(x+1) + ' can ' + msg1
                    print(info)                    

                    return 1

                except:
                    info = '-Error: "' + element + '" | Number: ' + str(x+1) + ' can not ' + msg1
                    print(info)

                    return 0

        else:
            x = 0
            y = len(e1)
            count = 0
            
            for i in e1:
                print('-Try element s number: ' + str(x+1))

                highlight(e1[x])
                
                c1 = 666
                if mode == 'BcheckT' or mode == 'BncheckT':      
                    try:
                        c1 = e1[x].is_selected()
                    except:
                        c1 = 666

                if c1 == c1c:
                    try:
                        if mode == 'BfillT' or mode == 'BfillTT':
                            e1[x].clear()
                            e1[x].send_keys(txt)
                        else:
                            e1[x].click()
                        info = '-Success: "' + element + '" | Number: ' + str(x+1) + ' can ' + msg1
                        print(info)
                        count += 1

                    except:
                        info = '-Error: "' + element + '" | Number: ' + str(x+1) + ' can not ' + msg1
                        print(info)
                    x +=1
                       

            if count != 0:

                info = '-Success: "' + element + '" can ' + msg1 + ' | Total Point: ' + str(count)
                print(info)
                return 1
            else:
                return 0 

    except:        
        info = '-Error: "' + element + '" can not ' + msg1
        print(info)
        return 0



    
def BselectTO (element1,element2): #  點選符合 2 字串條件的元素


    info1 = '\n[' + str (datetime.now()) + '] BselectT | ' + element1 + ' | ' + element2
    print(info1)


    mod = 'o'
    mode = 'BselectT'

    try:     
        e2 = driver.find_elements_by_xpath("(//*[contains(text(), '" + element2 + "')])")
        #print e2
        if not e2:            
            print('--Fail Find Text2: "' + element2)             
            return 0              

        print('--Success Find Text2: "' + element2 + ' | Point: ' +  str(len(e2)))



        for z in range (10):
            num = str(z + 1)
            print('--Try Option: ' + num)
            e1 = FelementT0( element1 , num , mod)
            if e1 == 0:
                print('--Fail ' + mode + ' Auto Mode adj2=0 , Try adj2=1 now..')
                e1 = FelementT( element1 , num , mod)
                if e1 == 0:
                    print('--Fail ' + mode + ' Auto Mode adj2=0 and adj2=1')
                    continue
            x = 0                
            for i in range (len(e1)):
                #print i
                print('--Try element s number: ' + str(x+1))

                highlight(e1[x])
                
                for y in range(len(e2)):
                    #print y
                    
                    if e2[y] == e1[i]:
                        print('--Bingo!!')
                        
                        highlight(e2[y])
                        try:
                            e2[y].click()                 
                            info = '--Success: "' + element1 + '" | Number: ' + str(i+1) + ' | Option: ' + num + ' && "' +  element2  + '" | Number: ' + str(y+1) +' can click'
                            print(info)
                            return 1
                            
                        except:
                            info = '--Error: "' + element1 + '" | Number: ' + str(i+1) + ' | Option: ' + num + ' && "' +  element2  + '" | Number: ' + str(y+1) +' can not click'
                            print(info)
                x +=1
    
    except:
        info =  '--Error: "' + element1 + '"  && "' +  element2  + '" can not click'
        print(info)
        return 0
    
def SBselectTO (element1,element2):
    if BselectTO (element1,element2) == 0:
           ErrorCon()
    else:
        return 1        


def Bxxx (mode, element, txt = ''):
    
    info1 = '\n[' + str (datetime.now()) + '] ' + mode + ' | ' + element + ' | ' + txt
    print(info1)
    
    c1c = 666
    if mode == 'Bfill':
        msg1 = 'fill: "' + txt + '"'

    elif mode == 'Bkey':
        msg1 = 'key: "' + txt + '"'        

    elif mode == 'Bclick':
        msg1 = 'click'

    elif mode == 'Bcheck':
        msg1 = 'check'
        c1c = 0
               
    elif mode == 'Bncheck':
        msg1 = 'disable check'
        c1c = 1

    else:
        info = '--Error: "' + mode + '" not support!!'
        return 0
        

    e1 = Felement(element)
    if e1 == 0:
        info = '--Error: "' + element + '" not found'
        print(info)
        return 0

    c1 = 666
    if mode == 'Bcheck' or mode == 'Bncheck':     
        c1 = e1.is_selected()

    if c1 == c1c:
        try:
            if mode == 'Bfill':
                e1.clear()
                e1.send_keys(txt)
            
            elif mode == 'Bkey':
                e1.send_keys(txt)
                
            else:
                e1.click()
            info = '--Success: "' + element + ' can ' + msg1
            print(info)
            return 1

        except:
            info = '--Error: "' + element  + ' can not ' + msg1
            print(info)
            return 0

    else:
        info = '--Error: "' + element + '" can not ' + msg1
        print(info)
        return 0

def BxxxD (driver,mode, element,  txt = ''):
    
    info1 = '\n[' + str (datetime.now()) + '] ' + mode + ' | ' + element + ' | ' + txt
    print(info1)
    
    c1c = 666
    if mode == 'Bfill':
        msg1 = 'fill: "' + txt + '"'

    elif mode == 'Bkey':
        msg1 = 'key: "' + txt + '"'        

    elif mode == 'Bclick':
        msg1 = 'click'

    elif mode == 'Bcheck':
        msg1 = 'check'
        c1c = 0
               
    elif mode == 'Bncheck':
        msg1 = 'disable check'
        c1c = 1

    else:
        info = '--Error: "' + mode + '" not support!!'
        return 0
        

    e1 = FelementD(driver,element)
    if e1 == 0:
        info = '--Error: "' + element + '" not found'
        print(info)
        return 0

    c1 = 666
    if mode == 'Bcheck' or mode == 'Bncheck':     
        c1 = e1.is_selected()

    if c1 == c1c:
        try:
            if mode == 'Bfill':
                e1.clear()
                e1.send_keys(txt)
            
            elif mode == 'Bkey':
                e1.send_keys(txt)
                
            else:
                e1.click()
            info = '--Success: "' + element + ' can ' + msg1
            print(info)
            return 1

        except:
            info = '--Error: "' + element  + ' can not ' + msg1
            print(info)
            return 0

    else:
        info = '--Error: "' + element + '" can not ' + msg1
        print(info)
        return 0


def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent   
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 2px solid red;")
    time.sleep(.5)
    apply_style(original_style)        
