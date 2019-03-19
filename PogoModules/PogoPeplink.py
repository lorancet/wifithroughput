# coding=UTF-8
PogoPeplinkVer = '2019/1/4 v1.4.17'

'''
為了 Peplink 設備操作, 相關的專屬模組

2019/1/4 v1.4.17 RA 修正
2019/1/3 v1.4.16 暫時停用 RA recv_ready , 很怪在 linux 會卡
2019/1/3 v1.4.15 RA 修正
2018/12/27 v1.4.14 RA 再加強
2018/12/26 v1.4.13 RA addkey 功能 bug fix
2018/12/25 v1.4.12 RA 再加強
2018/12/25 v1.4.11 RA 功能增強, 增加 Offline 判斷, 等待回應等機制, 加速與穩定提升
2018/12/21 v1.4.10 MBX support
2018/8/23 v1.4.9 apply change 與 confug upload 相容
2018/3/29 v1.4.8 改變 log 的時間格式, 增加 RA 登入後的等待時間
2018/3/13 v1.4.7 Pepwave MAX Transit with MediaFast support
2018/3/7 v1.4.6 EPX support
2018/2/7 v1.4.5 HWcheck 增加 Optrion 5 把差不多 status page 的訊息都回傳了
2017/10/20 v1.4.4 增加 B30LTE & BR1 的判斷 & Switch Firmware 判斷
2017/9/26 v1.4.3 Bver 語法移至 PogoPeplink.py
2017/8/30 v1.4.2 add Firmware upgrade comment 
2017/6/14 v1.4.1 修改 UIsApply 語法, 取消回 dashboard 確認的動作, 不知為什麼在 7.0.1 GA 會造成異常
2017/5/22 v1.4 大量調整, 改變 UIsLogin 重試機制, 增加 SUIsLogin (失敗中斷)功能, 調整相闗需要 login 為 SUIsLogin , 增加 PogoPeplinkInfo 加強訊息顯示
2017/5/18 v1.3.22 login 時間微調
2017/5/17 v1.3.21 詭異的以Enter login 方式在非 IDLE 會因編碼問題卡住, 暫取消按 Enter 方式
2017/5/8 v1.3.20 配合要合的 firfox 52 後的版本, 改變 login 方式為按 Enter
2017/4/24 v1.3.19 FIPS support
2017/4/21 v1.3.18 bug fix
2017/4/20 v1.3.17 bug fix 
2017/4/19 v1.3.16 改變版本號判斷為自動
2017/3/21 v1.3.15 增加 HD2/4 MFA & HD2 HW5 的判斷
2017/3/17 v1.3.14 更改 Mtype 的 BR1AC 為 BxAC 避免與 BR 系列的判斷出錯
2017/3/16 v1.3.13 改變 enable RA Allow Direct 為 BchecKT
2017/3/14 v1.3.12 新增  UIRA() UI 快速啟用RA
2017/3/10 v1.3.11 RA 加入 快速 addkey 
2017/3/10 v1.3.10 RA 加入 Direct Access 模式
2017/3/10 v1.3.9 強制統一RA關聯檔案格式 設定檔統一檔名 RA.csv , 命令檔 格式需為 RAxxxxx.csv, 變數為 xxxxx
2017/3/9 v1.3.8 增加 RA() UIStart() 與 HWCheck 功能修正
2017/3/6 v1.3.7 7.1.0 Support
2017/1/13 v1.3.6 7.0.1 Support
2017/1/12 v1.3.5 UIsLogin 修改
2016/12/1 v1.3.4 7.0.0 Support
2016/11/22 v.1.3.3 讓子程序能回依成功失敗回傳 1 或 0
2016/9/23 v1.3.2 修改 apply change 的判斷
2016/9/22 v1.3.1 SOHO MK3 判斷 
2016/9/9 v1.3 大量整合設備必要資訊判斷與 firmware 操作功能
2016/8/23 v1.2.13 BR1 MK2 判斷
2016/8/17 v1.2.12 6.3.3 Support
2016/8/10 v1.2.11 VM Balance 判斷
2016/8/5 v1.2.10 MAX Hotspot 判斷
2016/6/28 v1.2.9 BR1 mini 判斷
2016/5/11 v1.2.8 6.4.0 Support
2016/4/26 v1.2.7 HWcheck 增加 SN UP time 回報 修改 UIsLogin 相容性 
2016/4/20 v1.2.6 UIsLogin UIsApply 重寫後歸入
2016/3/17 v1.2.5 BR1 Slim 判斷
2016/1/25 v1.2.4 FushioHub HWver fix
2016/1/22 v1.2.3 FushioHub 支援
2016/1/19 v1.2.2 HWmodel 功能拆開, 方便配合 Reporter & 6.3.2 判斷
2016/1/18 v1.2.1 增加版本 log 配合
2016/1/12 v1.2 修正 HD2 mini 判斷
2015/12/15 v1.1 修改整合部分 HW SW Check 
2015/12/14 v1.0 first release

注意!! 需要 PogoUI.py

使用方式

from PogoModules.PogoPeplink import *

前一個Bopen() 必需改為 driver = Bopen()

HWmode, Mtype, HWmodel, HWver, FWver, HWmodels  = HWCheck(driver)

'''

from PogoUI import *
import re,paramiko,csv

def HWCheck(driver,opt=0):
    '''
    變數說明 以 Pepwave MAX HD2 Hardware 1 6.3.3 build 1234 FFFF-AAAA-DDDD 為例
    
    HWmode      HD2hw1                  設備型號簡寫+硬體版本         
    Mtype       M700                    設備對應的 Firmware 類型       
    HWmodel     Pepwave MAX HD2         直接由UI讀到的型號          
    HWmodels    HD2                     設備型號簡寫
    HWver       1                       硬體版本
    FWver       6.3.3 build 1234        直接由UI讀到的 Firmware 版本
    SWver       633                     方便對應的轉格式 Firmware 代數 6.3.3 = 633 而 5.2.1 = 521 所以 633 > 521 方便判斷版本
    SN          FFFF-AAAA-DDDD          直接由UI讀到的 序號
    UP          1d 1hr 32min            直接由UI讀到的 開機時間
    LANmac      1F:1F:1F:1F:1F:1F:1F:1F 直接由UI讀到的 LAN port MAC Address
    FIPS        True                    FIPS 的啟用狀況

    '''
    
    ModelUni = re.findall(r'<div class="form_field">Model</div></td><td style="font-weight: bold;">(.*?)</td></tr>',driver.page_source)
    if not ModelUni:                        
        ModelUni = re.findall(r'Model</td><td class="tablecontent2b" style="font-weight: bold;">(.*?)</td>',driver.page_source)                        
    HWverUni = re.findall(r'<div class="form_field">Hardware Revision</div></td><td style="font-weight: bold;">(.*?)</td></tr>',driver.page_source)
    if not HWverUni:                         
         HWverUni =  re.findall(r'Hardware Revision</td><td class="tablecontent2b" style="font-weight: bold;">(.*?)</td></tr>',driver.page_source)
         if not HWverUni:
             HWverUni = '0' # for FusionHub    
    SNUni = re.findall(r'<div class="form_field">Serial Number</div></td><td style="font-weight: bold;">(.*?)</td></tr>',driver.page_source)
    if not SNUni:
        SNUni = re.findall(r'Serial Number</td><td class="tablecontent2b" style="font-weight: bold;">(.*?)</td></tr>',driver.page_source)
    FWverUni = re.findall(r'<div class="form_field">Firmware</div></td><td style="font-weight: bold;">(.*?)</td></tr>',driver.page_source)
    if not FWverUni:
        FWverUni = re.findall(r'Firmware</td><td class="tablecontent2b" style="font-weight: bold;">(.*?)</td>',driver.page_source)
    UPUni = re.findall(r'<span class="uptime">(.*?)</span>',driver.page_source)
    if not UPUni:
        UPUni = re.findall(r'Uptime</td><td class="tablecontent2b" style="font-weight: bold;">(.*?)</td>',driver.page_source)

    LANmacUni = re.findall('<div class="form_field">LAN</div></td><td>(.*?)</td></tr>',driver.page_source)    
    if not LANmacUni:
        LANmacUni = re.findall('<div class="form_field">LAN </div></td><td>(.*?)</td></tr>',driver.page_source) # for FushionHub 不知為什麼多了一個空白
        if not LANmacUni:
            LANmacUni = '0'

    if '<div class="form_field">FIPS 140-2 Crypto Module</div></td><td style="font-weight: bold;">Activated</td>' in driver.page_source:
        FIPS = True
    else:
        FIPS = False
    if opt == 5:
        Rname =  re.findall(r'<tr class="tablecontent2"><td class="tabletitle2 form_legend"><div class="form_field">Router Name</div></td><td style="font-weight: bold;">(.*?)</td></tr>',driver.page_source)[0].encode('ascii', 'ignore') # Router Name
        PcodeUni = re.findall(r'<tr class="tablecontent2"><td class="tabletitle2 form_legend"><div class="form_field">Product Code</div></td><td style="font-weight: bold;">(.*?)</td></tr>',driver.page_source) #Product Code
        if not PcodeUni: 
            Pcode = ''
        else:
            Pcode = PcodeUni[0].encode('ascii', 'ignore')
        PepV = re.findall(r'<tr class="tablecontent2"><td class="tabletitle2 form_legend"><div class="form_field">PepVPN Version</div></td><td style="font-weight: bold;">(.*?)</td></tr>',driver.page_source)[0].encode('ascii', 'ignore') #PepVPN Version
        Hname = re.findall(r'<tr class="tablecontent2"><td class="tabletitle2 form_legend"><div class="form_field">Host Name</div></td><td style="font-weight: bold;">(.*?)\n</td></tr>',driver.page_source)[0].encode('ascii', 'ignore') #Host Name
        Msupport = re.findall(r'<tr class="tablecontent2"><td class="tabletitle2 form_legend"><div class="form_field">Modem Support Version</div></td><td style="font-weight: bold;"><span>(.*?)</span> ',driver.page_source)[0].encode('ascii', 'ignore') #Modem Support Version
    print '== Original Data form Status Page =='
    print ModelUni
    print HWverUni
    print FWverUni
    print LANmacUni
    print '== Convert to ASCII =='
    HWmodel = ModelUni[0].encode('ascii', 'ignore')
    print HWmodel
    HWver = HWverUni[0].encode('ascii', 'ignore') 
    print HWver
    FWver = FWverUni[0].encode('ascii', 'ignore')
    print FWver
    SN = SNUni[0].encode('ascii', 'ignore')
    print SN
    UP = UPUni[0].encode('ascii', 'ignore')
    print UP
    LANmac = LANmacUni[0].encode('ascii', 'ignore')
    print LANmac

    print 'FIPS: ' + str(FIPS)
    
    HWmodels, Mtype = HWMapping(HWmodel,HWver)


    
    print 'HWCheck return: ' + HWmodels + 'hw' + HWver
    HWmode = HWmodels + 'hw' + HWver
    SWprefix = '<div class="form_field">Firmware</div></td><td style="font-weight: bold;">'
    SWver = FWFormat(SWprefix,driver)

    if opt == 0:
        data =  [HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver]
    elif opt == 1:
        data = [HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,SN,UP]
    elif opt == 2:
        data = [HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac]
    elif opt == 3:
        data = [HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP]
        
    elif opt == 4:
        data = [HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP,FIPS]
            
    elif opt == 5:
        data = [HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP,FIPS,Rname,Pcode,PepV,Hname,Msupport]
    print data
    return data    

    
    
def SWCheck(driver): # SW check 由 Dashboard 把版本變成數值方便判斷
    SWprefix = '<div class="left">Firmware:</div><div class="right"><span>'
    SWver = FWFormat(SWprefix,driver)
    return SWver

def FWFormat(SWprefix,driver):

    DS = driver.page_source
    FWL = DS.index(SWprefix) + len (SWprefix)
    FW = DS[FWL:FWL+5].replace('.','').encode('ascii', 'ignore')
    return FW
        
 
def HWMapping(HWmodel,HWver):
    
    #Peplink 系列
    if 'Peplink Balance 310' in HWmodel:
        HWmodels = 'B310'
        if int(HWver) >= 4:
            Mtype = 'PPC'            
        else:
            Mtype = 'Bx10'

    elif 'Peplink Balance 210' in HWmodel:
        HWmodels = 'B210'
        if int(HWver) >= 4:
            Mtype = 'PPC'            
        else:
            Mtype = 'Bx10'

    elif 'Peplink Balance 20' in HWmodel:
        HWmodels = 'B20'
        Mtype = 'Bx0'

    elif 'Peplink Balance 50' in HWmodel:
        HWmodels = 'B50'
        Mtype = 'Bx0'

    elif 'Peplink Balance 305' in HWmodel:
        HWmodels = 'B305'
        if int(HWver) >= 2:
            Mtype = 'X64'            
        else:
            Mtype = 'X86'

    elif 'Peplink Balance 30 LTE' in HWmodel:
        HWmodels = 'B30LTE'
        if int(HWver) >=3:
            Mtype = 'PPC'            
        else:
            Mtype = 'M700'


    elif 'Peplink Balance 30' in HWmodel:
        HWmodels = 'B30'
        Mtype = 'Bx0'

    elif 'Peplink Balance 380' in HWmodel:
        HWmodels = 'B380'
        if int(HWver) >= 6:
            Mtype = 'X64'            
        else:
            Mtype = 'X86'

    elif 'Peplink Balance 580' in HWmodel:
        HWmodels = 'B580'
        if int(HWver) >= 2:
            Mtype = 'X64'            
        else:
            Mtype = 'X86'

    elif 'Peplink Balance 710' in HWmodel:
        HWmodels = 'B710'
        if int(HWver) >= 3:
            Mtype = 'X64'            
        else:
            Mtype = 'X86'

    elif 'Peplink Balance 1350' in HWmodel:
        HWmodels = 'B1350'
        if int(HWver) >= 2:
            Mtype = 'X64'            
        else:
            Mtype = 'X86'

    elif 'Peplink Balance 2500' in HWmodel:
        HWmodels = 'B2500'
        Mtype = 'X64'

    elif 'Peplink Balance One' in HWmodel:
        HWmodels = 'BOne'
        Mtype = 'PPC'

    elif 'Peplink MediaFast 200' in HWmodel:
        HWmodels = 'MFA200'
        Mtype = 'PPC'

    elif 'Peplink MediaFast 500' in HWmodel:
        HWmodels = 'MFA500'
        Mtype = 'X64'

    elif 'Peplink MediaFast 750' in HWmodel:
        HWmodels = 'MFA750'
        Mtype = 'X64'

    #Pepwave 系列

    elif 'Pepwave MAX HD4 MBX' in HWmodel:
        HWmodels = 'HD4MBX'
        Mtype = 'MBX'            

    elif 'Pepwave MAX HD4 MediaFast' in HWmodel:
        HWmodels = 'HD4MFA'
        Mtype = 'PPC'        

    elif 'Pepwave MAX HD4' in HWmodel:
        HWmodels = 'HD4'
        Mtype = 'PPC'

    elif 'Pepwave MAX HD2 MediaFast' in HWmodel:
        HWmodels = 'HD2MFA'
        Mtype = 'PPC'        
        
    elif 'Pepwave MAX HD2 Mini' in HWmodel:
        HWmodels = 'HD2mini'
        Mtype = 'PPC'

        
    elif 'Pepwave MAX HD2' in HWmodel:
        HWmodels = 'HD2'
        if int(HWver) >= 5:
            Mtype = 'PPC'            
        else:
            Mtype = 'M700'

    elif 'Pepwave MAX 700' in HWmodel:
        HWmodels = 'M700'
        if int(HWver) >= 3:
            Mtype = 'PPC'            
        else:
            Mtype = 'M700'

    elif 'Pepwave MAX BR1 Pro' in HWmodel:
        HWmodels = 'BR1Pro'
        if int(HWver) >= 3:
            Mtype = 'M700'            
        else:
            Mtype = 'BR'        

    elif 'Pepwave MAX BR1 Mini' in HWmodel:
        HWmodels = 'BR1Mini'
        Mtype = 'BR'


    elif 'Pepwave MAX BR1 ENT' in HWmodel:
        HWmodels = 'BR1ENT'
        Mtype = 'PPC'

    elif 'Pepwave MAX BR1 Slim' in HWmodel:
        HWmodels = 'BR1Slim'
        Mtype = 'BR'

    elif 'Pepwave MAX BR1 MK2' in HWmodel:
        HWmodels = 'BR1MK2'
        Mtype = 'BxAC'

    elif 'Pepwave MAX BR1' in HWmodel:
        HWmodels = 'BR1'
        Mtype = 'BR'

    elif 'Pepwave MAX BR' in HWmodel:
        HWmodels = 'BR'
        Mtype = 'BR'

    elif 'Pepwave MAX On-The-Go' in HWmodel:
        HWmodels = 'MOTG'
        Mtype = 'MOTG'

    elif 'Pepwave Surf SOHO MK3' in HWmodel:
        HWmodels = 'SOHOMK3'
        Mtype = 'BxAC'

    elif 'Pepwave Surf' in HWmodel:
        HWmodels = 'Surf'
        Mtype = 'Surf'

    elif 'Pepwave MAX Transit with MediaFast' in HWmodel:
        HWmodels = 'TransitMFA'
        Mtype = 'PPC'
    
    elif 'Pepwave MAX Transit' in HWmodel:
        HWmodels = 'Transit'
        Mtype = 'PPC'

    elif 'Pepwave MAX Hotspot' in HWmodel:
        HWmodels = 'Hotspot'
        Mtype = 'BxAC'

    elif 'EPX' in HWmodel:
        HWmodels = 'EPX'
        Mtype = 'EPX'

    # Peplink FusionHub
    elif 'Peplink FusionHub' in HWmodel:
        HWmodels = 'FH'
        Mtype = 'FH'       

    # VM Balance
    elif 'Peplink Virtual Balance' in HWmodel:
        HWmodels = 'VMB'
        Mtype = 'VMB'       

    # SD Switch
    elif 'Peplink SD Switch 8P' in HWmodel:
        HWmodels = 'SS8P'
        Mtype = 'SS8P'       

    elif 'Peplink SD Switch 24P' in HWmodel:
        HWmodels = 'SS24P'
        Mtype = 'SS24P'       

    elif 'Peplink SD Switch 48P' in HWmodel:
        HWmodels = 'SS48P'
        Mtype = 'SS48P'       



    else:
        Mtype = 'None'
        HWmodels = 'None'
        
    return [HWmodels, Mtype]
    


#UI Login 
def UIsLogin(url,usern = 'admin', passw = 'admin'):

    info = 'UIsLogin | ' + str(url) + ' | ' + str(usern) + ' | ' + str(passw)
    print PogoPeplinkInfo(info,'Start')
    
    def Login ():           
        try:
            Bvisit(url)
            Bwait_text('Login')
            # id password
            Bfill('username', usern)
            Bsleep(1)        
            Bfill('password', passw)
            Bkey('username', '')
            Bsleep(1)
            BclickTB('Login')
            Bsleep(5)
            if not Bwait_text('Device Information'):
                return 0
            else:              
                return 1
        except:
            print 'UIsLogin - Login Fail'
            return 0
    
    
    count = 1

    while count < 4:
        print 'Login Try: ' + str(count)
        if Login ():
            print 'Login Suceess: ' + str(count)
            print PogoPeplinkInfo(info,'End:Success')
            return 1
        else:
            print 'Try Login Fail: ' + str(count)
            count += 1
            if count < 4:
                print 'wanit for 3 sec . will have next try...'
                Bsleep(3)
    print PogoPeplinkInfo(info,'End:Fail')
    return 0
        
def SUIsLogin(url,usern = 'admin', passw = 'admin'):
    print '-----[UIsLogin with S , will stop process if Fail!!]-----'
    if not UIsLogin(url,usern, passw):
        print '-----[process STOP , check last status!!]-----'
        raise SystemExit


#UI Apply Change -  url 指 balance 設備, run 是等 見到成功 save 的時間, wait 是 apply change 後等生效的時間
def UIsApply(url,run = 30,wait = 10):
    
    info = 'UIsApply | ' + str(run) + ' | ' + str(wait)
    print PogoPeplinkInfo(info,'Start')
    
  
    if run < 10:
        print 'Error !! run can not less than 10sec, will force change to 10sec'
        run = 10
    if wait < 10:
        print 'Error !! wait can not less than 10sec, will force change to 10sec'
        wait = 10         
    ctime = int(run // 2)
    if Bwait_text('will be effective after clicking the', ctime) == 0:        
        print 'Error !! not find "will be effective after clicking the"'
    Bsleep(5)
    '''
    #原本這段是要加強確認. 7.0.1 GA 後就變會發生異常中斷..
    
    Bvisit (url)
    if Bwait_text('Device Information') == 0:
        PogoPeplinkInfo(info,'End:Fail')
        raise SystemExit
    Bsleep(5)
    x = 0
    while Bwait_text('Changes pending') == 0:
        x += 1
        Bvisit (url)
        if Bwait_text('Device Information') == 0:
            print PogoPeplinkInfo(info,'End:Fail')
            raise SystemExit
        if x == run:
            print PogoPeplinkInfo(info,'End:Fail')
            raise SystemExit
        Bsleep(10)
    '''    
    BclickT('Apply Changes')
    Bsleep(wait)
    print PogoPeplinkInfo(info,'End:Success')

def FWFile(SS = 'N', FWfolder = 'firmware/'):
    '''
    FWfolder 放  firmware 的目錄
    SS N 預設找最新的, O 找最舊的

    以下 Swith 的功能暫保留不放入
    global FX86,FBx10,FSurf,FMOTG,FPPC,FBx0,FM700,FX64,FBR,FFH,FBxAC,FSS8P,FSS24P,FSS48P

    return FX86,FBx10,FSurf,FMOTG,FPPC,FBx0,FM700,FX64,FBR,FFH,FBxAC,FSS8P,FSS24P,FSS48P

    '''

    global FX86,FBx10,FSurf,FMOTG,FPPC,FBx0,FM700,FX64,FBR,FFH,FBxAC
    
    
    FWlist = os.listdir (FWfolder)

    if FWfolder != 'firmware/':
        FWfolder1 = FWfolder
    else:
        FWfolder1 = os.getcwd() + '\\firmware\\'

    def FWF(mod,SS):
        try:
            Flist = [f for f in os.listdir(FWfolder) if re.match(r''+ mod +'+.*\.bin', f)]
            Flist.sort()
            if SS == 'O':
                return FWfolder1 + Flist[0]
            else:
                return FWfolder1 + Flist[-1]
        except:
            return ''

   
    FX86 = FWF('fw-b305_380_580_710_1350',SS) # x86
    print 'x86: ' + FX86
    FBx10 = FWF('fw-b210_310_hw2_hw3',SS) # olde 210 310 ..
    print 'old Bx10: ' + FBx10
    FSurf = FWF('fw-surf_soho',SS) # Surf
    print 'Surf: ' + FSurf
    FMOTG = FWF('fw-maxotg',SS) # MOTG
    print 'MOTG: ' + FMOTG
    FPPC = FWF('fw-b1_210hw4',SS) # PowerPC
    print 'PPC: ' + FPPC
    FBx0 = FWF('fw-b20_30',SS) # 20 30 ...
    print 'Bx0: ' + FBx0
    FM700 = FWF('fw-m700_hd2',SS) # old Max700 HD2
    print 'M700: ' + FM700
    FX64 = FWF('fw-b305hw2_380hw6',SS) # x64
    print 'x86: ' + FX64
    FBR = FWF('fw-max_br1_',SS) # old BR
    print 'BRx: ' + FBR
    FFH = FWF('fw-fusionhub',SS) # FusionHub
    print 'FusionHub: ' + FFH
    FBxAC = FWF('fw-max_br1mk2_',SS) # BR1MK2 hotsport....
    print 'BRxAC: ' + FBxAC
    FSS8P = FWF('fw-plsw8',SS) # SD Switch 8P
    print 'SS8P: ' + FSS8P
    FSS24P = FWF('fw-plsw24',SS) # SD Switch 24P
    print 'SS24P: ' + FSS24P
    FSS48P = FWF('fw-plsw48',SS) # SD Switch 8P
    print 'SS48P: ' + FSS8P    

    return FX86,FBx10,FSurf,FMOTG,FPPC,FBx0,FM700,FX64,FBR,FFH,FBxAC


def FWMapping(Mtype):

    if Mtype == 'X86':
        return FX86
    if Mtype == 'Bx10':
        return FBx10
    if Mtype == 'Surf':
        return FSurf
    if Mtype == 'MOTG':
        return FMOTG
    if Mtype == 'PPC':
        return FPPC
    if Mtype == 'Bx0':
        return FBx0
    if Mtype == 'M700':
        return FM700
    if Mtype == 'X64':
        return FX64
    if Mtype == 'BR':
        return FBR
    if Mtype == 'FH':
        return FFH
    if Mtype == 'BxAC':
        return FBxAC
    if Mtype == 'SS8P':
        return FSS8P
    if Mtype == 'SS24P':
        return FSS24P
    if Mtype == 'SS48P':
        return FSS48P

def UIStartUP(url,driver,usern = 'admin', passw = 'admin'):
    global SWver, HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,LANmac
    SUIsLogin(url,usern, passw)#Login


    Bvisit (url + '/cgi-bin/MANGA/index.cgi?mode=config&option=utsysinfo')
    Bsleep(2)    
    HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac = HWCheck(driver,2)
    
    print 'HWmode = '+ HWmode
    print 'Mtype = ' + Mtype
    print 'HWmodel = ' + HWmodel
    print 'HWver = ' + HWver
    print 'FWver = ' + FWver
    print 'HWmodels = ' + HWmodels
    print 'SWver = ' + str(SWver)

    print 'LANmac = ' + LANmac

    return SWver, HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,LANmac

def UIStart(url,driver,opt = 0 , usern = 'admin', passw = 'admin'):  #預計取代 UIStartUP

    
    info = 'UIStart | ' + str(url) + ' | ' + str(driver)  + ' | ' + str(opt) + ' | ' + str(usern)  + ' | ' + str(passw) 
    print PogoPeplinkInfo(info,'Start')
        
    
    global HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP,FIPS
    SUIsLogin(url,usern, passw)#Login            
    Bvisit (url + '/cgi-bin/MANGA/index.cgi?mode=config&option=utsysinfo')
    Bsleep(2)

    if opt == 0:        
        data = HWCheck(driver,3)    
        HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP = data        
    if opt == 1:        
        data = HWCheck(driver,4)    
        HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP,FIPS = data              
    if opt == 2:        
        data = HWCheck(driver,5)    
        HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP,FIPS,Rname,Pcode,PepV,Hname,Msupport = data       

    
    print 'HWmode = '+ HWmode
    print 'Mtype = ' + Mtype
    print 'HWmodel = ' + HWmodel
    print 'HWver = ' + HWver
    print 'FWver = ' + FWver
    print 'HWmodels = ' + HWmodels
    print 'SWver = ' + str(SWver)

    print 'LANmac = ' + LANmac

    print 'SN = ' + SN
    print 'UP = ' + UP

    if opt == 1:
        print 'FIPS = ' + str(FIPS)
    
    
    print data
    print PogoPeplinkInfo(info,'End:Success')
    return data

def UIRA(url,driver,usern = 'admin', passw = 'admin'):    
    SUIsLogin(url,usern, passw)#Login
    Bvisit (url + '/cgi-bin/MANGA/index.cgi?mode=config&option=utsysinfo')
    Bsleep(2)    
    data = HWCheck(driver,3)
    SN = data[8]
    BclickT("Turn on")
    Bsleep(5)
    print 'SN = ' + SN
    Bvisit (url + '/cgi-bin/MANGA/support.cgi')
    Bsleep(2)  
    BcheckT('Allow direct connection')
    Bsleep(5)
    return SN

def FWUpgrade(url, filename):
    '''
    !!filename must fill path!!
    
    filename = 'C:/QA/temp/fw-b305hw2_380hw6_580hw2_710hw3_1350hw2_2500-7.1.0.201708300019-r18669.bin'
    or
    filename = 'C:\\QA\\temp\\fw-b305hw2_380hw6_580hw2_710hw3_1350hw2_2500-7.1.0.201708300019-r18669.bin'
    '''
    
    Bvisit (url + '/cgi-bin/MANGA/index.cgi?mode=config&option=firmware')
    Bsleep(2)
    BfillT ('Firmware Image',filename)
    Bsleep(2)
    BclickT ('Manual Upgrade')
    Bsleep(2)
    BclickT ('OK')

def RA (SN,commfile):
    '''

    SN 直接用 IP 會進入 Direct Access 模式
    
    帳密檔案 格式 RA.csv
    

    第一行: RA key 轉換後的 pem 檔
    第二行: RA key password
    第三行: RA login 帳戶
    

    commfile 格式 RAxxx.csv

    每行為一個指令

    等待時間;重覆次數;"指令"

    以下範本
    10;1;"gethwinfo -a"
    10;1;"cat /etc/software-release"
    10;1;"date"
    10;1;"uptime"
    10;1;"head /proc/meminfo"
    10;1;"df -h"
    10;1;"cat /proc/sys/net/nf_conntrack_max"
    10;3;"wc /proc/net/ip_conntrack"

    commfile 直接打 'addkeyto' 會變 addkeyto 模式 
    
    '''
    raconf = file ('RA.csv', 'r').readlines()
    rakey = raconf[0].strip('\r\n')
    rapass = raconf[1].strip('\r\n')
    rauser = raconf[2].strip('\r\n')
    raconnected = False

    if '.' in SN :
        rahost = SN
        raport = 2222
        rauser = 'root'
        rassh = False
    else:
        rahost = "ra.peplink.com"
        raport = 443
        rassh = True

    if commfile is 'addkeyto':
        raaddkeyto = True
        rassh = False
    else:        
        racomm = 'RA' + str(commfile) + '.csv'
        print  '\n[' + str (datetime.now()) + '] ' +'RA Command file: ' + racomm
        raaddkeyto = False

    global buffdata
    buffdata = ''
    k = paramiko.RSAKey.from_private_key_file(rakey,rapass)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print '\n[' + str (datetime.now()) + '] ' +"RA Server connecting"    
    c.connect( hostname = rahost , username = rauser , pkey = k , port=raport)
    output = "RA Host: " + rahost + '\n'
    buffdata = "".join([buffdata,output])
    print output    
    output = "RA Port: " + str(raport) + '\n'
    buffdata = "".join([buffdata,output])
    print output
    print '\n[' + str (datetime.now()) + '] ' +"RA Server connected"


    remote_conn = c.invoke_shell()
       

    def writebuffer():
        global buffdata
	try:
            if remote_conn.recv_ready():
                output = remote_conn.recv(1000)
                buffdata = "".join([buffdata,output])
                print '\n[' + str (datetime.now()) + '] ' +  'RA Receive: ' + '\n\n' + output + '\n\n' 
            else:
                print '\n[' + str (datetime.now()) + '] ' +  'Remote not ready <- debug message only , for check remote status.\n'
                return ''           

	except:
            print 'write buffer error'

    def waitready():
	Bsleep(5)
	writebuffer()
	''' # 2019/1/3 mark 這段會卡, 暫時改用 Bsleep 
        global buffdata
        x = 0
        #remote_conn.send('\n')
        while not remote_conn.recv_ready() and x < 30:
            x += 1
            #print '\n[' + str (datetime.now()) + '] ' + 'Send "Enter" and wait ready | try: ' + str(x) + ' times'
            #remote_conn.send('\n')            
            time.sleep(1)
            print '\n[' + str (datetime.now()) + '] ' + 'waiting server ready: ' + str(x) + 'sec\n'
            if x == 30:
                print '\n[' + str (datetime.now()) + '] Warring !! wait 30 try server not ready , pass wait , please check !!\n'
                writebuffer()
                return 1
        writebuffer()
        return 1
	'''

    def waittext(txt):
        global buffdata
        x = 0
        textready = False
        while not textready and x < 10:
            writebuffer()

            if txt in buffdata:
                print '\n[' + str (datetime.now()) + '] ' + 'waiting specific text: '+ str(txt) + ' | success!!'
                return 1
                
                
            x += 1
            time.sleep(1)
            print '\n[' + str (datetime.now()) + '] ' + 'waiting specific text: '+ str(txt) + ' | ' + str(x) + 'sec\n'
            if x == 10:
                print '\n[' + str (datetime.now()) + '] Warring !! wait 10 sec server not ready , pass wait , please check !!\n'
                return 0
        
        

    def proccomm(wait,times,command):
            global buffdata
            for i in range(int(times)):
                    commands = command + '\n'
                    x = 0
                    remote_conn.send('\n')
                    if waitready() == 0:
                         break

                    remote_conn.send(commands)
                    info1 = '\n[' + str (datetime.now()) + '] ' + 'RA Send: ' + commands + '\n'
                    print info1
                    Bsleep(int(wait))

                    
                    output = remote_conn.recv(1000)                    
                    buffdata = "".join([buffdata,output])
                    info1 = '\n[' + str (datetime.now()) + '] ' +  'RA Receive: ' + '\n\n' + output + '\n\n'
                    print info1
    
    writebuffer()
    #time.sleep(10) # 2018/3 不知為什麼 RA Server 反應越來越慢, 增加送 cammand 前等待
    waitready()
        
    
    if rassh is True: # 以序號連結
        rcount = 0
        while 'http://raweb.peplink.com' not in buffdata and rcount < 3:
            rcount += 1     
            proccomm(3,1,"sshbalance " + SN)
            if 'OFFLINE' in buffdata:
                print '[RA faild] Device ' + SN + ' is OFFLINE'
            waitready()
        if 'http://raweb.peplink.com' in buffdata:      
            raconnected = True

                

    elif raaddkeyto is True: # 以序號加 ssh key     
        rcount = 0
        while 'http://raweb.peplink.com' not in buffdata and rcount < 3:
            rcount += 1     
            proccomm(3,1,"addkeyto " + SN)
            if 'OFFLINE' in buffdata:
                print '[RA faild] Device ' + SN + ' is OFFLINE'
            waitready()
            waittext('Added your public key to the device')

    
    elif rassh is False and raaddkeyto is False: # 以 IP 直連
	print 'Direct Access Mode'
        rcount = 0
        waitready()
	print buffdata
        if 'BusyBox' in buffdata:      
        	raconnected = True

           


    if raconnected is True:
        with open(racomm, 'rb') as tasklist:
                taskreader = csv.reader(tasklist, delimiter=';', quotechar='"')
                for row in taskreader:
                    
                        info1 =  '\n[' + str (datetime.now()) + '] ' +'Found CSV row: %s' % ','.join(row)
                        print info1
                        wait = row[0]
                        times = row[1]
                        command = row[2]
                        proccomm(wait,times,command)

    
    c.close()
    print 'RA Disconnected'
    print '\n\n----[print last RA Data , Start]--------------\n\n'
    print buffdata
    print '\n----[print last RA Data , End]----------------\n\n'
    return buffdata


def PogoPeplinkInfo(cmd,status):
    tt = str (datetime.now())
    info = '\n[' + tt + '][PogoPeplink Module ' + PogoPeplinkVer + ']['+ cmd + ' ][' + status + ']'
    return info 
    
def Bver (SWver,sver,ever,cmd):
    '''
    Bfill('#IPA', '10.88.81.211')
    
    以 希望 6.1.2 版本以前執行為例, 
    Bver(SWver, 0 , 612, "Bfill('#IPA', '10.88.81.211')")

    以 希望 6.2.0 版本以後執行為例,
    Bver(SWver, 620 , 0, "Bfill('#IPA', '10.88.81.211')")

    以 希望 6.3.0至 6.4.0 執行為例
    Bver(SWver, 630 , 640, "Bfill('#IPA', '10.88.81.211')")
    

    '''

    info1 = '\n[' + str (datetime.now()) + '] Bver | ' + str(SWver) + ' | ' + str(sver) +  ' | ' + str(ever) +  ' | ' + str(cmd)
    print info1

    
    if int(sver) == 0:
        if int(SWver) <= int(ever):
            print '-' + str(SWver) + ' <= ' + str (ever) + ' | now process | ' + str(cmd)
            exec (cmd)
        else:
            print '-' + str(SWver) + ' > ' + str (ever) + ' | will not process | ' + str(cmd)
            return 0
        
    elif int(ever) == 0:
        if int(SWver) >= int(sver):            
            print '-' + str(SWver) + ' >= ' + str (sver) + ' | now process | ' + str(cmd)
            exec (cmd)
        else:
            print '-' + str(SWver) + ' < ' + str (sver) + ' | will not process | ' + str(cmd)
            return 0

    else:
        if int(SWver) <= int(ever) and int(SWver) >= int(sver):
            print '-' + str(SWver) + ' does between ' + str (sver) + ' and ' + str (ever) + ' | now process | ' + str(cmd)
            exec (cmd)

        else:
            print '-' + str(SWver) + ' not between ' + str (sver) + ' and ' + str (ever) + ' | will not process | ' + str(cmd)
            return 0    
    
