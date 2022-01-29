# coding=UTF-8
PogoPeplinkVer = '2021/05/06 v2.1.14'

'''
為了 Peplink 設備操作, 相關的專屬模組

2021/05/06 v2.1.14 HWCheck 增加 AP 相容, 沒 LAN mac 直接拿 WAN mac 用
2021/01/05 v2.1.13 HD2 Fiber 支援
2020/12/23 v2.1.12 AP相關 IPQ64 (BR1 5G)支援
2020/12/16 v2.1.11 Peplink Balance 310 5G 支援
2020/11/23 v2.1.10 改 firmware expire 也判定 login 成功
2020/11/12 v2.1.9 增加 statup page 開啟的等待時間2 sec -> 10 sec
2020/09/29 v2.1.8 RA addkeyto 設備後 強制啟用 allow direct connection, 功能加了先保留, 運作怪怪
2020/09/25 v2.1.7 bug fix
2020/09/24 v2.1.6 SDX Pro 支援
2020/09/08 v2.1.5 Apply change 再調整
2020/08/31 v2.1.4 Apply change 再調整
2020/08/28 v2.1.3 Apply change 在 8.2 後的會失誤, 再調整
2020/08/06 v2.1.2 status UI 的 Router Name -> Device Name
2020/07/10 v2.1.1 新增 ConfigChangeM 
2020/07/08 v2.1.0 新增 ConfigChange ConfigCompareF 算是 config 處理指令集簡化操作
2020/06/05 v2.0.17 B310X B580X 支援
2020/04/27 v2.0.16 firmware 7 相容加強
2020/04/16 v2.0.15 bug fix 相容加強
2020/04/16 v2.0.14 HWCheck 重整, 加強 8.1.0 相容
2020/03/24 v2.0.13 EPX SN 相容修正
2020/03/24 v2.0.12 8.1.0 2020/3/24 status UI 更改相容
2020/03/17 v2.0.11 RA 新增 \為 escapec 字元
2020/02/27 v2.0.10 UBR , BR1 Pro HW4 support
2020/02/10 v2.0.9 8.1.0 SN 新格式相容
2020/02/05 v2.0.8 Balance Two support
2020/01/16 v2.0.7 FWFiles 路徑加強 windows linux 相容, ipq firmware 檔名更動對應
2020/01/08 v2.0.6 RA 改版的相容修正
2019/11/13 v2.0.5 Apply change 後回首頁 前 先 ping 有沒活著
2019/11/4 v2.0.4 Apply change 後回首頁
2019/10/29 v2.0.3 UIUconfigD 只選第一個 button , 避免用到 ha pair 的 upload , 會造成 pepwave LAN ip 更改失敗
2019/10/16 v2.0.2 bug fix
2019/10/9 v2.0.1 RA() Python2 相容修正, 新增 ConfigPatchM 指令, 可以置換 config patch 文件中的 && 字元達成動態配置
2019/10/9 v2.0.0 與 Python3 版本合併, 直接相容 Python 2 & 3
2019/10/2 v1.6.4 新增 CleanFolder() 指令, 預設清除 Download Folder
2019/10/2 v1.6.3 config 文字檔控制工具 取消 = , 改為 + 自動偵測, - 時只比對欄位, 不比對值, bug fix 
2019/10/1 v1.6.2 config 文字檔控制工具加強, 提供狀態訊息,增加刪除功能, 取消 CFuploadD 改為 UIUconfigD
2019/9/27 v1.6.1 bug fix
2019/9/27 v1.6.0 新增 config 文字檔控制工具, 目前只能在 linux 運作
2019/8/19 v1.5.14 AP support 
2019/7/12 v1.5.13 2019/7/12 後的 daily build password 更改頁面的對應
2019/7/11 v1.5.12 SpeedFusiion Tester 支援
2019/7/11 v1.5.11 appliy change 按之前的等待時間由 5 sec -> 10 sec
2019/6/14 v1.5.10 Transit Mini support 
2019/5/31 v1.5.9 IPQ support B20X 
2019/5/28 v1.5.8 SDX support
2019/5/23 v1.5.7 RA 讀取命令檔的容錯加強, 不再因空白行造成中斷
2019/5/21 v1.5.6 bug fix
2019/5/21 v1.5.5 SUIsLoginD fix 
2019/5/21 v1.5.4 配合 8.0.1 預設 admin password 強制改為 Admin!2345
2019/5/17 v1.5.3 RA timeout 時間增至 300 sec
2019/5/15 v1.5.2 改善 RA 的多工處理
2019/4/24 v1.5.1 加大 RA 處理的 buffer , 避免資料過多回傳被丟
2019/4/17 v1.5.0 配 合 PogoUI 3.3+ 指令尾 D 的多網頁支援
2019/3/12 v1.4.20 CX support
2019/3/19 v1.4.19 UIRA 相容再修改
2019/3/19 v1.4.18 RA 調整, 減少 direct access 時的等待時間
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


文字檔控制 config  範例

IpAdd = '192.168.1.1' #設備IP
pepurl = 'http://'+IpAdd #http:// + 設備IP

driver = Bopen()
config_file = UIDconfigD(driver,pepurl) # 抓config
Bsleep(5)
ConfigUnpack(config_file) # 解 config 
Bsleep(5)
ConfigPatch('patch1.txt') # 改 config
ConfigPatchM('DDDD','patch2.txt') # 改 config 並把 patch2.txt 中的 && 置換 成 DDDD
ConfigPack(config_file) # 包 config 

new_config_file = config_file + '.updated'
CFuploadD(driver, pepurl , new_config_file) # 上傳 config
BquitD(driver)


文字檔控制 config 更多範例

ConfigCompare('config','configM') # 比對 config 產生 patch 文件

以下自訂目錄等用法  

ConfigUnpack('20190925_b1hw1_192C15237845.conf','../temp')
ConfigPatch('patch3.txt','../temp')
ConfigPack('20190925_b1hw1_192C15237845.conf','../temp')


文字檔控制 config patch 的語法

+ 新增或修改 config
- 刪除整行 config


'''

from .PogoUI import *
import re,paramiko,csv,os,shutil,sys,platform

pyver = sys.version_info[0] # Python 主版本

def HWCheck(driver,opt=0):

    code8100324 = False
    
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
    Rname       Pogo-TestR1             直接由UI讀到的 Router Name 
    Pcode       R123444                 早期版本會有 Product Code , 好像沒在用, 先保留    
    PepV        9.7.8                   直接由UI讀到的 PepVPN 版本
    Hname       pogo-testr1             直接由UI讀到的 Host Name
    Msupport    1024                    直接由UI讀到的 Modem Support Version


    使用說明

    !! 必需 !! 先開到 設備的 Status Page 後再使用

    或 改用 UIStart 語法, 可直接完成登入並取得必要變數

    基本用法1
    HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP = HWCheck(driver)
    會取得以上變數

    基本用法2
    Data = HWCheck(driver)
    類似1 但如要取得 HWmode 必需用
    Hwmode = Data[0]
    以下類推

    加強用法
    Data = HWCheck(driver,5)
    Rname = Data[11]
    用 opton 5 取得全部變數回傳

    option 的對應直見程式碼, 因為陸續需要的資訊變多與向下相容, 目前己有多個模式      
   

    '''
    
    ModelUni = re.findall(r'<div class="form_field">Model</div></td><td style="font-weight: bold;">(.*?)</td></tr>',driver.page_source)
    if not ModelUni:                        
        ModelUni = re.findall(r'Model</td><td class="tablecontent2b" style="font-weight: bold;">(.*?)</td>',driver.page_source)
        if not ModelUni:
            ModelUni = re.findall(r'<div class="form_field">Model</div></td><td>(.*?)</td>',driver.page_source)  # 8.1.0 3/24 後
            code8100324 = True
        
    HWverUni = re.findall(r'<div class="form_field">Hardware Revision</div></td><td style="font-weight: bold;">(.*?)</td></tr>',driver.page_source)
    if not HWverUni:                         
         HWverUni =  re.findall(r'Hardware Revision</td><td class="tablecontent2b" style="font-weight: bold;">(.*?)</td></tr>',driver.page_source)
         if not HWverUni:
             HWverUni =  re.findall(r'<div class="form_field">Hardware Revision</div></td><td>(.*?)</td>',driver.page_source) # 8.1.0 3/24 後
             if not HWverUni:
                 HWverUni = ['0'] # for FusionHub    
    SNUni = re.findall(r'<div class="form_field">Serial Number</div></td><td style="font-weight: bold;">(.*?)</td></tr>',driver.page_source)
    if not SNUni:
        SNUni = re.findall(r'Serial Number</td><td class="tablecontent2b" style="font-weight: bold;">(.*?)</td></tr>',driver.page_source)
        if not SNUni:
            SNUni = re.findall(r'<div class="form_field">Serial Number</div></td><td>(.*?)</td>',driver.page_source) # 8.1.0 3/24 後
            if not SNUni:
                SNUni = ['Err'] 
                
            
    FWverUni = re.findall(r'<div class="form_field">Firmware</div></td><td style="font-weight: bold;">(.*?)</td></tr>',driver.page_source)
    if not FWverUni:
        FWverUni = re.findall(r'Firmware</td><td class="tablecontent2b" style="font-weight: bold;">(.*?)</td>',driver.page_source)
        if not FWverUni:
            FWverUni = re.findall(r'<div class="form_field">Firmware</div></td><td>(.*?)</td>',driver.page_source) # 8.1.0 3/24 後
            if not FWverUni:
                FWverUni = ['Err']
            

        
    UPUni = re.findall(r'<span class="uptime">(.*?)</span>',driver.page_source)
    if not UPUni:
        UPUni = re.findall(r'Uptime</td><td class="tablecontent2b" style="font-weight: bold;">(.*?)</td>',driver.page_source)
        if not UPUni:
            UPUni = re.findall(r'<div class="form_field">Uptime</div></td><td style="font-weight: bold;">(.*?)</td>',driver.page_source) # 8.1.0 3/24 後
            if not UPUni:
                UPUni = ['Err']
        

    LANmacUni = re.findall('<div class="form_field">LAN</div></td><td>(.*?)</td></tr>',driver.page_source)    
    if not LANmacUni:
        LANmacUni = re.findall('<div class="form_field">LAN </div></td><td>(.*?)</td></tr>',driver.page_source) # for FushionHub 不知為什麼多了一個空白
        if not LANmacUni:
            LANmacUni = re.findall('<div class="form_field">WAN</div></td><td>(.*?)</td></tr>',driver.page_source) # for AP, 沒 LAN mac 直接拿 WAN, 作用相同
            if not LANmacUni:            
                LANmacUni = ['0']

    
    

    if '<div class="form_field">FIPS 140-2 Crypto Module</div></td><td style="font-weight: bold;">Activated</td>' in driver.page_source: 
        FIPS = True
    else:
        FIPS = False


    
    RnameUni =  re.findall(r'<tr class="tablecontent2"><td class="tabletitle2 form_legend"><div class="form_field">Router Name</div></td><td style="font-weight: bold;">(.*?)</td></tr>',driver.page_source) # Router Name
    if not RnameUni:
        RnameUni = re.findall(r'Router Name</div></td><td><span>(.*?)</span>',driver.page_source) # 8.1.0 3/24 後
        if not RnameUni:
            RnameUni = re.findall(r'Device Name</div></td><td><span>(.*?)</span>',driver.page_source) # 8.1.0 RC 後
            if not RnameUni:                
                RnameUni = ['Err']
        
    PcodeUni = re.findall(r'<tr class="tablecontent2"><td class="tabletitle2 form_legend"><div class="form_field">Product Code</div></td><td style="font-weight: bold;">(.*?)</td></tr>',driver.page_source) #Product Code
    if not PcodeUni: 
        PcodeUni = ['']

    PepVUni = re.findall(r'<tr class="tablecontent2"><td class="tabletitle2 form_legend"><div class="form_field">PepVPN Version</div></td><td style="font-weight: bold;">(.*?)</td></tr>',driver.page_source) #PepVPN Version
    if not  PepVUni:
         PepVUni = re.findall(r'PepVPN Version</div></td><td>(.*?)</td>',driver.page_source) # 8.1.0 3/24 後
         if not  PepVUni:
             PepVUni = ['Err']
         
    HnameUni = re.findall(r'<tr class="tablecontent2"><td class="tabletitle2 form_legend"><div class="form_field">Host Name</div></td><td style="font-weight: bold;">(.*?)\n</td></tr>',driver.page_source) #Host Name
    if not HnameUni:
        HnameUni = re.findall(r'Host Name</div></td><td>(.*?)</td>',driver.page_source) # 8.1.0 3/24 後
        if not HnameUni:
            HnameUni = ['Err']
    
    MsupportUni = re.findall(r'<tr class="tablecontent2"><td class="tabletitle2 form_legend"><div class="form_field">Modem Support Version</div></td><td style="font-weight: bold;"><span>(.*?)</span> ',driver.page_source) #Modem Support Version
    if not MsupportUni:
        MsupportUni = re.findall(r'Modem Support Version</div></td><td><span>(.*?)</span>',driver.page_source) # 8.1.0 3/24 後
        if not MsupportUni:
            MsupportUni = ['Err']
        
    print('== Original Data form Status Page ==')
    print(ModelUni)
    print(HWverUni)
    print(FWverUni)
    print(LANmacUni)
    print(RnameUni)
    print(PcodeUni)
    print(PepVUni)
    print(HnameUni)
    print(MsupportUni)    
    print('== Convert to ASCII ==')

    HWmodel = ModelUni[0]
    HWver = HWverUni[0]
    FWver = FWverUni[0]
    SN = SNUni[0]
    UP = UPUni[0]
    LANmac = LANmacUni[0]
    Rname = RnameUni[0]
    Pcode = PcodeUni[0]     
    PepV = PepVUni[0]
    Hname = HnameUni[0]
    Msupport = MsupportUni[0]

    
    if pyver == 2: #Python 2 相容
        HWmodel = ModelUni[0].encode('ascii', 'ignore')
        HWver = HWverUni[0].encode('ascii', 'ignore')
        FWver = FWverUni[0].encode('ascii', 'ignore')
        SN = SNUni[0].encode('ascii', 'ignore')
        UP = UPUni[0].encode('ascii', 'ignore')
        LANmac = LANmacUni[0].encode('ascii', 'ignore')
        Rname = RnameUni[0].encode('ascii', 'ignore')
        Pcode = PcodeUni[0].encode('ascii', 'ignore')
        PepV = PepVUni[0].encode('ascii', 'ignore')
        Hname = HnameUni[0].encode('ascii', 'ignore')
        Msupport = MsupportUni[0].encode('ascii', 'ignore')

       



    print(HWmodel)
    print(HWver)
    print(FWver)

    if 'div' in SN: # 模組 SN 排除
        SN  = re.findall(r'">(.*?)</div>',SN)[0]
              
    print(SN)        
    print(UP)
    print(LANmac)
    print(Rname)
    print(Pcode)
    print(PepV)
    print(Hname)
    print(Msupport)    


    print('FIPS: ' + str(FIPS))
    
    HWmodels, Mtype = HWMapping(HWmodel,HWver)


    
    print('HWCheck return: ' + HWmodels + 'hw' + HWver)
    HWmode = HWmodels + 'hw' + HWver
    SWprefix = '<div class="form_field">Firmware</div></td><td style="font-weight: bold;">'
    if code8100324 is True:
        SWprefix = '<div class="form_field">Firmware</div></td><td>' # 8.1.0 3/24 後 
    
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
    print(data)
  
    return data    

    
    
def SWCheck(driver): # SW check 由 Dashboard 把版本變成數值方便判斷
    SWprefix = '<div class="left">Firmware:</div><div class="right"><span>'
    SWver = FWFormat(SWprefix,driver)
    return SWver

def FWFormat(SWprefix,driver):

    DS = driver.page_source
    FWL = DS.index(SWprefix) + len (SWprefix)
    FW = DS[FWL:FWL+5].replace('.','')
    if pyver == 2: #Python 2 相容
        FW = DS[FWL:FWL+5].replace('.','').encode('ascii', 'ignore')
    
    return FW
        
 
def HWMapping(HWmodel,HWver):
    
    #Peplink 系列


    if 'Peplink Balance 20X' in HWmodel:
        HWmodels = 'B20X'
        Mtype = 'IPQ'

    elif 'Peplink Balance 310 5G' in HWmodel:
        HWmodels = 'B3105G'
        Mtype = 'EPX'        

    elif 'Peplink Balance 310X' in HWmodel:
        HWmodels = 'B310X'
        Mtype = 'EPX'

    elif 'Peplink Balance 580X' in HWmodel:
        HWmodels = 'B580X'
        Mtype = 'EPX'
    
    elif 'Peplink Balance 310' in HWmodel:
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

    elif 'Peplink Balance Two' in HWmodel:
        HWmodels = 'BTwo'
        Mtype = 'EPX'

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
        Mtype = 'EPX'            

    elif 'Pepwave MAX HD4 MediaFast' in HWmodel:
        HWmodels = 'HD4MFA'
        Mtype = 'PPC'        

    elif 'Pepwave MAX HD4' in HWmodel:
        HWmodels = 'HD4'
        Mtype = 'PPC'

    elif 'Pepwave MAX HD2 Fiber' in HWmodel:
        HWmodels = 'HD2Fiber'
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
        if int(HWver) == 3:
            Mtype = 'M700'            
        else:
            Mtype = 'BR'        

    elif 'Pepwave MAX BR1 5G' in HWmodel:
        HWmodels = 'BR15G'
        Mtype = 'IPQ64'

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

    elif 'Pepwave MAX Transit Mini' in HWmodel:
        HWmodels = 'TransitMini'
        Mtype = 'BR'

    elif 'Pepwave MAX Transit with MediaFast' in HWmodel:
        HWmodels = 'TransitMFA'
        Mtype = 'PPC'
    
    elif 'Pepwave MAX Transit' in HWmodel:
        HWmodels = 'Transit'
        Mtype = 'PPC'

    elif 'Pepwave MAX CX' in HWmodel:
        HWmodels = 'CX'
        Mtype = 'PPC'

    elif 'Pepwave MAX Hotspot' in HWmodel:
        HWmodels = 'Hotspot'
        Mtype = 'BxAC'

    elif 'Pepwave UBR' in HWmodel:
        HWmodels = 'UBR'
        Mtype = 'BR'

        

    elif 'EPX' in HWmodel:
        HWmodels = 'EPX'
        Mtype = 'EPX'

    elif 'SDX Pro' in HWmodel:
        HWmodels = 'SDXP'
        Mtype = 'EPX'

    elif 'SDX' in HWmodel:
        HWmodels = 'SDX'
        Mtype = 'EPX'


    # Peplink FusionHub
    elif 'Peplink FusionHub' in HWmodel:
        HWmodels = 'FH'
        Mtype = 'FH'       

    # VM Balance
    elif 'Peplink SpeedFusion Tester' in HWmodel:
        HWmodels = 'VMB'
        Mtype = 'VMB'       

    # SD Switch
    elif 'Peplink SD Switch 8P' in HWmodel:
        HWmodels = 'SS8P'
        Mtype = 'SS8P'       

    elif 'Peplink SD Switch 16P' in HWmodel:
        HWmodels = 'SS16P'
        Mtype = 'SS16P'       

    elif 'Peplink SD Switch 24P' in HWmodel:
        HWmodels = 'SS24P'
        Mtype = 'SS24P'       

    elif 'Peplink SD Switch 48P' in HWmodel:
        HWmodels = 'SS48P'
        Mtype = 'SS48P'       

    # AP
    
    elif 'Pepwave AP One AX' in HWmodel:
        HWmodels = 'AP1AX'
        Mtype = 'AP1AX'       

    elif 'Pepwave AP One AC Mini' in HWmodel:
        HWmodels = 'AP1ACM'
        Mtype = 'AP1AC'       

    elif 'Pepwave AP One Flex' in HWmodel:
        HWmodels = 'AP1ACF'
        Mtype = 'AP1AC'       

    else:
        Mtype = 'None'
        HWmodels = 'None'
        
    return [HWmodels, Mtype]
    

#UI Login 
def UIsLogin(url,usern = 'admin', passw = 'Admin!2345'):

    info = 'UIsLogin | ' + str(url) + ' | ' + str(usern) + ' | ' + str(passw)
    print(PogoPeplinkInfo(info,'Start'))
    
    def Login ():

        isAP = False
        
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
                if Bwait_text('Invalid Username or Password.'):

                    # for Balance
                    Bfill('username', 'admin')
                    Bsleep(1)        
                    Bfill('password', 'admin')
                    Bkey('username', '')
                    Bsleep(1)
                    BclickTB('Login')
                    Bsleep(5)
                    if not Bwait_text('Device Information'):
                        if Bwait_text('Invalid Username or Password.'):

                            # for AP
                            Bfill('username', 'admin')
                            Bsleep(1)        
                            Bfill('password', 'public')
                            Bkey('username', '')
                            Bsleep(1)
                            BclickTB('Login')
                            Bsleep(5)
                            isAP = True


                    if not Bwait_text('You must change your default password'):
                        Bvisit(url + '/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
                        
                        if not Bwait_text('Admin Settings'):
                            Bvisit(url + '/cgi-bin/MANGA/index.cgi?mode=config&option=utadmin') # for firmware 7
                            
                        BfillT('Admin Password','Admin!2345')
                        BclickT('Save')
                        Bsleep(5)
                        UIsApply(url)
                        
                    else:                   
                    
                        Bsleep(1)
                        if isAP is True:
                            BfillT('Current Password','public')
                        else:    
                            BfillT('Current Password','admin')
                        BfillT('New Password','Admin!2345')
                        Bsleep(5)
                        BfillT('Confirm New Password','Admin!2345')
                        BclickT('Save')
                        Bsleep(5)
                        BclickT('OK')
                        Bsleep(5)
                        
                    if Bwait_text('Device Information'):
                        return 1

                    elif Bwait_text('System Information'):
                        print ('Firmware expired!!')
                        return 1

                    else:
                        return 0
                        

                else:
                    return 0
            else:              
                return 1
        except:
            print('UIsLogin - Login Fail')
            return 0
    
    
    count = 1

    while count < 4:
        print('Login Try: ' + str(count))
        if Login ():
            print('Login Suceess: ' + str(count))
            print(PogoPeplinkInfo(info,'End:Success'))
            return 1
        else:
            print('Try Login Fail: ' + str(count))
            count += 1
            if count < 4:
                print('wanit for 3 sec . will have next try...')
                Bsleep(3)
    print(PogoPeplinkInfo(info,'End:Fail'))
    return 0

def UIsLoginD(driver, url,usern = 'admin', passw = 'Admin!2345'):

    info = 'UIsLogin | ' + str(url) + ' | ' + str(usern) + ' | ' + str(passw)
    print(PogoPeplinkInfo(info,'Start'))
    
    def Login ():

        isAP = False
        
        try:
            BvisitD(driver, url)
            Bwait_textD(driver, 'Login')
            # id password
            BfillD(driver, 'username', usern)
            Bsleep(1)        
            BfillD(driver, 'password', passw)
            BkeyD(driver, 'username', '')
            Bsleep(1)
            BclickTBD(driver, 'Login')
            Bsleep(5)
            if not Bwait_textD(driver, 'Device Information'):
                if Bwait_textD(driver, 'Invalid Username or Password.'):

                    # for Balance
                    BfillD(driver, 'username', 'admin')
                    Bsleep(1)        
                    BfillD(driver, 'password', 'admin')
                    BkeyD(driver, 'username', '')
                    Bsleep(1)
                    BclickTBD(driver, 'Login')
                    Bsleep(5)
                    if not Bwait_textD(driver, 'Device Information'):
                        if Bwait_textD(driver, 'Invalid Username or Password.'):

                            # for AP
                            BfillD(driver, 'username', 'admin')
                            Bsleep(1)        
                            BfillD(driver, 'password', 'public')
                            BkeyD(driver, 'username', '')
                            Bsleep(1)
                            BclickTBD(driver, 'Login')
                            Bsleep(5)
                            isAP = True


                    if not Bwait_textD(driver, 'You must change your default password'):
                        BvisitD(driver, url + '/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
                        
                        if not Bwait_text('Admin Settings'):
                            Bvisit(url + '/cgi-bin/MANGA/index.cgi?mode=config&option=utadmin') # for firmware 7
                        
                        BfillTD(driver, 'Admin Password','Admin!2345')
                        BclickTD(driver, 'Save')
                        Bsleep(5)
                        UIsApplyD(driver, url)
                        
                    else:                   
                    
                        Bsleep(1)
                        if isAP is True:
                            BfillTD(driver, 'Current Password','public')
                        else:    
                            BfillTD(driver, 'Current Password','admin')
                        BfillTD(driver, 'New Password','Admin!2345')
                        Bsleep(5)
                        BfillTD(driver, 'Confirm New Password','Admin!2345')
                        BclickTD(driver, 'Save')
                        Bsleep(5)
                        BclickTD(driver, 'OK')
                        Bsleep(5)
                        
                    if Bwait_textD(driver, 'Device Information'):
                        return 1

                    elif Bwait_textD(driver, 'System Information'):
                        print ('Firmware expired!!')
                        return 1

                    else:
                        return 0
                        

                else:
                    return 0
            else:              
                return 1
        except:
            print('UIsLogin - Login Fail')
            return 0
    
    
    count = 1

    while count < 4:
        print('Login Try: ' + str(count))
        if Login ():
            print('Login Suceess: ' + str(count))
            print(PogoPeplinkInfo(info,'End:Success'))
            return 1
        else:
            print('Try Login Fail: ' + str(count))
            count += 1
            if count < 4:
                print('wanit for 3 sec . will have next try...')
                Bsleep(3)
    print(PogoPeplinkInfo(info,'End:Fail'))
    return 0
        
def SUIsLogin(url,usern = 'admin', passw = 'Admin!2345'):
    print('-----[UIsLogin with S , will stop process if Fail!!]-----')
    if not UIsLogin(url,usern, passw):
        print('-----[process STOP , check last status!!]-----')
        raise SystemExit


def SUIsLoginD(driver,url,usern = 'admin', passw = 'Admin!2345'):
    print('-----[UIsLoginD with S , will stop process if Fail!!]-----')
    if not UIsLoginD(driver,url,usern, passw):
        print('-----[process STOP , check last status!!]-----')
        raise SystemExit




#UI Apply Change -  url 指 balance 設備, run 是等 見到成功 save 的時間, wait 是 apply change 後等生效的時間
def UIsApply(url,run = 30,wait = 10):
    
    info = 'UIsApply | ' + str(run) + ' | ' + str(wait)
    print(PogoPeplinkInfo(info,'Start'))
    
  
    if run < 10:
        print('Error !! run can not less than 10sec, will force change to 10sec')
        run = 10
    if wait < 10:
        print('Error !! wait can not less than 10sec, will force change to 10sec')
        wait = 10         
    ctime = int(run // 2)
    if Bwait_text('will be effective after clicking the', ctime) == 0:        
        print('Error !! not find "will be effective after clicking the"')
    Bsleep(10)
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

    # 8.2.0 後的再確認

    try:
        testAdd = url.replace('http://','')
        testAdd = testAdd.replace('https://','')
        testAdd = testAdd.replace('/','')
        
        if PingCheck(testAdd):        
            Bvisit (url)
            if Bwait_text('Changes pending'):
                    BclickT('Apply Changes')
                    Bsleep(wait)
            else:
                print(PogoPeplinkInfo(info,'2nd Apply Fail[1st Sucees]'))
    except:
        print(PogoPeplinkInfo(info,'2nd Apply Fail[IP Changed]'))
      
       
    print(PogoPeplinkInfo(info,'End:Success'))

def UIsApplyD(driver,url,run = 30,wait = 10):
    
    info = 'UIsApply | ' + str(run) + ' | ' + str(wait)
    print(PogoPeplinkInfo(info,'Start'))
    
  
    if run < 10:
        print('Error !! run can not less than 10sec, will force change to 10sec')
        run = 10
    if wait < 10:
        print('Error !! wait can not less than 10sec, will force change to 10sec')
        wait = 10         
    ctime = int(run // 2)
    if Bwait_textD(driver,'will be effective after clicking the', ctime) == 0:        
        print('Error !! not find "will be effective after clicking the"')
    Bsleep(10)
    BclickTD(driver,'Apply Changes')
    Bsleep(wait)

    # 8.2.0 後的再確認
    try:

        testAdd = url.replace('http://','')
        testAdd = testAdd.replace('https://','')
        testAdd = testAdd.replace('/','')
        
        if PingCheck(testAdd):                
            BvisitD (driver, url)
            if Bwait_textD(driver, 'Changes pending'):
                    BclickTD(driver, 'Apply Changes')
                    Bsleep(wait)    

            else:
                print(PogoPeplinkInfo(info,'2nd Apply Fail[1st Sucees]'))
    except:
        print(PogoPeplinkInfo(info,'2nd Apply Fail[IP Changed]'))

    testAdd = url.replace('http://','')
    testAdd = testAdd.replace('https://','')
    testAdd = testAdd.replace('/','')
    
    if PingCheck(testAdd):
        BvisitD (driver,url)
        
    print(PogoPeplinkInfo(info,'End:Success'))



def FWFile(SS = 'N', FWfolder = 'firmware/'):
    '''
    FWfolder 放  firmware 的目錄
    SS N 預設找最新的, O 找最舊的

    以下 Swith 的功能暫保留不放入
    global FX86,FBx10,FSurf,FMOTG,FPPC,FBx0,FM700,FX64,FBR,FFH,FBxAC,FSS8P,FSS24P,FSS48P

    return FX86,FBx10,FSurf,FMOTG,FPPC,FBx0,FM700,FX64,FBR,FFH,FBxAC,FSS8P,FSS24P,FSS48P

    '''

    global FX86,FBx10,FSurf,FMOTG,FPPC,FBx0,FM700,FX64,FBR,FFH,FBxAC,FSS8P,FSS24P,FSS48P,FEPX,FIPQ,FVMB,FAP1AX,FAP1AC,FIPQ64,FSS16P
    
    
    FWlist = os.listdir (FWfolder)

    if FWfolder != 'firmware/':
        FWfolder1 = FWfolder
    else:
        
        if platform.system() == 'Windows':
            defpath = '\\firmware\\'
        else:
            defpath = '/firmware/'

        FWfolder1 = os.getcwd() + defpath

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
    print('x86: ' + FX86)
    FBx10 = FWF('fw-b210_310_hw2_hw3',SS) # olde 210 310 ..
    print('old Bx10: ' + FBx10)
    FSurf = FWF('fw-surf_soho',SS) # Surf
    print('Surf: ' + FSurf)
    FMOTG = FWF('fw-maxotg',SS) # MOTG
    print('MOTG: ' + FMOTG)
    FPPC = FWF('fw-b1_210hw4',SS) # PowerPC
    print('PPC: ' + FPPC)
    FBx0 = FWF('fw-b20_30',SS) # 20 30 ...
    print('Bx0: ' + FBx0)
    FM700 = FWF('fw-m700_hd2',SS) # old Max700 HD2
    print('M700: ' + FM700)
    FX64 = FWF('fw-b305hw2_380hw6',SS) # x64
    print('x86: ' + FX64)
    FBR = FWF('fw-max_br1_',SS) # old BR
    print('BRx: ' + FBR)
    FFH = FWF('fw-fusionhub',SS) # FusionHub
    print('FusionHub: ' + FFH)
    FBxAC = FWF('fw-max_br1mk2_',SS) # BR1MK2 hotsport....
    print('BRxAC: ' + FBxAC)
    FSS8P = FWF('fw-plsw8',SS) # SD Switch 8P
    print('SS8P: ' + FSS8P)
    FSS24P = FWF('fw-plsw24',SS) # SD Switch 24P
    print('SS24P: ' + FSS24P)
    FSS48P = FWF('fw-plsw48',SS) # SD Switch 48P
    print('SS48P: ' + FSS8P)    
    FEPX = FWF('fw-epx',SS) # EPX
    print('EPX: ' + FEPX)
    FIPQ = FWF('fw-b20x',SS) # IPQ
    print('IPQ: ' + FIPQ)   
    FVMB = FWF('fw-sftvm',SS) # VMB
    print('VMB: ' + FVMB)
    FAP1AX = FWF('fw-aponeax',SS) # AP1AX
    print('AP1AX: ' + FAP1AX)
    FAP1AC = FWF('fw-apone_ac',SS) # AP1AC
    print('AP1AC: ' + FAP1AC)    
    FIPQ64 = FWF('fw-br1c',SS) # IPQ64
    print('IPQ64: ' + FIPQ64)
    FSS16P = FWF('fw-plsw16',SS) # SD Switch 16P
    print('SS16P: ' + FSS16P)    

    return [FX86,FBx10,FSurf,FMOTG,FPPC,FBx0,FM700,FX64,FBR,FFH,FBxAC,FSS8P,FSS24P,FSS48P,FEPX,FIPQ,FVMB,FAP1AX,FAP1AC,FIPQ64,FSS16P]


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
    if Mtype == 'EPX':
        return FEPX
    if Mtype == 'IPQ':
        return FIPQ
    if Mtype == 'VMB':
        return FVMB
    if Mtype == 'AP1AX':
        return FAP1AX
    if Mtype == 'AP1AC':
        return FAP1AC    
    if Mtype == 'IPQ64':
        return FIPQ64
    if Mtype == 'SS16P':
        return FSS16P    


def UIStartUP(url,driver,usern = 'admin', passw = 'Admin!2345'):
    global SWver, HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,LANmac
    SUIsLogin(url,usern, passw)#Login


    Bvisit (url + '/cgi-bin/MANGA/index.cgi?mode=config&option=utsysinfo')
    Bsleep(10)    
    HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac = HWCheck(driver,2)
    
    print('HWmode = '+ HWmode)
    print('Mtype = ' + Mtype)
    print('HWmodel = ' + HWmodel)
    print('HWver = ' + HWver)
    print('FWver = ' + FWver)
    print('HWmodels = ' + HWmodels)
    print('SWver = ' + str(SWver))

    print('LANmac = ' + LANmac)

    return SWver, HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,LANmac

def UIStart(url,driver,opt = 0 , usern = 'admin', passw = 'Admin!2345'):  #預計取代 UIStartUP

    '''
    自動登入, 取得設備變數

    更多用法可以配合 HWCheck 直用

    基本用法1
    HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP = UIStart("http://10.91.168.1",driver)
    會取得以上變數

    基本用法2
    Data = UIStart("http://10.91.168.1",driver)
    類似1 但如要取得 HWmode 必需用
    Hwmode = Data[0]
    以下類推

    加強用法
    Data = UIStart("http://10.91.168.1",driver,2)
    Rname = Data[11]
    用 opton 2 取得全部變數回傳
    
    


    '''

    
    info = 'UIStart | ' + str(url) + ' | ' + str(driver)  + ' | ' + str(opt) + ' | ' + str(usern)  + ' | ' + str(passw) 
    print(PogoPeplinkInfo(info,'Start'))
        
    
    global HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP,FIPS
    SUIsLogin(url,usern, passw)#Login            
    Bvisit (url + '/cgi-bin/MANGA/index.cgi?mode=config&option=utsysinfo')
    Bsleep(10)

    if opt == 0:        
        data = HWCheck(driver,3)    
        HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP = data        
    if opt == 1:        
        data = HWCheck(driver,4)    
        HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP,FIPS = data              
    if opt == 2:        
        data = HWCheck(driver,5)    
        HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP,FIPS,Rname,Pcode,PepV,Hname,Msupport = data       

    
    print('HWmode = '+ HWmode)
    print('Mtype = ' + Mtype)
    print('HWmodel = ' + HWmodel)
    print('HWver = ' + HWver)
    print('FWver = ' + FWver)
    print('HWmodels = ' + HWmodels)
    print('SWver = ' + str(SWver))

    print('LANmac = ' + LANmac)

    print('SN = ' + SN)
    print('UP = ' + UP)

    if opt == 1:
        print('FIPS = ' + str(FIPS))
    
    
    print(data)
    print(PogoPeplinkInfo(info,'End:Success'))
    return data

def UIStartD(driver,url,opt = 0 , usern = 'admin', passw = 'Admin!2345'):  #預計取代 UIStartUP

    
    info = 'UIStart | ' + str(url) + ' | ' + str(driver)  + ' | ' + str(opt) + ' | ' + str(usern)  + ' | ' + str(passw) 
    print(PogoPeplinkInfo(info,'Start'))
        
    
    global HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP,FIPS
    SUIsLoginD(driver,url,usern, passw)#Login            
    BvisitD (driver,url + '/cgi-bin/MANGA/index.cgi?mode=config&option=utsysinfo')
    Bsleep(10)

    if opt == 0:        
        data = HWCheck(driver,3)    
        HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP = data        
    if opt == 1:        
        data = HWCheck(driver,4)    
        HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP,FIPS = data              
    if opt == 2:        
        data = HWCheck(driver,5)    
        HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP,FIPS,Rname,Pcode,PepV,Hname,Msupport = data       

    
    print('HWmode = '+ HWmode)
    print('Mtype = ' + Mtype)
    print('HWmodel = ' + HWmodel)
    print('HWver = ' + HWver)
    print('FWver = ' + FWver)
    print('HWmodels = ' + HWmodels)
    print('SWver = ' + str(SWver))

    print('LANmac = ' + LANmac)

    print('SN = ' + SN)
    print('UP = ' + UP)

    if opt == 1:
        print('FIPS = ' + str(FIPS))
    
    
    print(data)
    print(PogoPeplinkInfo(info,'End:Success'))
    return data



def UIRA(url,driver,usern = 'admin', passw = 'Admin!2345'):    
    SUIsLogin(url,usern, passw)#Login
    Bvisit (url + '/cgi-bin/MANGA/index.cgi?mode=config&option=utsysinfo')
    Bsleep(2)    
    data = HWCheck(driver,3)
    SN = data[8]
    if not BclickT("Turn on"):
        BclickT("Turn On") # 8.0 媽的又改=.=
    Bsleep(5)
    print('SN = ' + SN)
    Bvisit (url + '/cgi-bin/MANGA/support.cgi')
    Bsleep(2)  
    BcheckT('Allow direct connection')
    Bsleep(5)
    return SN

def UIRAD(driver,url,usern = 'admin', passw = 'Admin!2345'):    
    SUIsLoginD(driver,url,usern, passw)#Login
    BvisitD (driver,url + '/cgi-bin/MANGA/index.cgi?mode=config&option=utsysinfo')
    Bsleep(2)    
    data = HWCheck(driver,3)
    SN = data[8]
    if not BclickTD(driver,"Turn on"):
        BclickTD(driver,"Turn On") # 8.0 媽的又改=.=
    Bsleep(5)
    print('SN = ' + SN)
    BvisitD (driver, url + '/cgi-bin/MANGA/support.cgi')
    Bsleep(2)  
    BcheckTD(driver,'Allow direct connection')
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


def FWUpgradeD(driver,url, filename):
    '''
    !!filename must fill path!!
    
    filename = 'C:/QA/temp/fw-b305hw2_380hw6_580hw2_710hw3_1350hw2_2500-7.1.0.201708300019-r18669.bin'
    or
    filename = 'C:\\QA\\temp\\fw-b305hw2_380hw6_580hw2_710hw3_1350hw2_2500-7.1.0.201708300019-r18669.bin'
    '''
    
    BvisitD (driver,url + '/cgi-bin/MANGA/index.cgi?mode=config&option=firmware')
    Bsleep(2)
    BfillTD (driver,'Firmware Image',filename)
    Bsleep(2)
    BclickTD (driver,'Manual Upgrade')
    Bsleep(2)
    BclickTD (driver,'OK')



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

    \ 為 escapec 字元, 也就是說
    在命令要用到 " 要下 \"
    在命令要用 \ 要下 \\

    
    
    '''
    raconf = open('RA.csv', 'r').readlines()
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
        print('\n[' + str (datetime.now()) + '] ' +'RA Command file: ' + racomm)
        raaddkeyto = False

    #global buffdata
    buffdata = {0:''}
    k = paramiko.RSAKey.from_private_key_file(rakey,rapass)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('\n[' + str (datetime.now()) + '] ' +"RA Server connecting")    
    c.connect( hostname = rahost , username = rauser , pkey = k , port=raport , timeout = 300)
    output = "RA Host: " + rahost + '\n'
    buffdata[0]= "".join([buffdata[0],output])
    print(output)    
    output = "RA Port: " + str(raport) + '\n'
    buffdata[0] = "".join([buffdata[0],output])
    print(output)
    print('\n[' + str (datetime.now()) + '] ' +"RA Server connected")


    remote_conn = c.invoke_shell()
       

    def writebuffer():
        #buffdata
            try:
                    if remote_conn.recv_ready():
                        
                        if pyver == 2: #Python 2 相容
                            output = remote_conn.recv(1000)
                        else:
                            output = remote_conn.recv(1000).decode()
                            
                        buffdata[0] = "".join([buffdata[0],output])
                        print('\n[' + str (datetime.now()) + '] ' +  'RA Receive: ' + '\n\n' + output + '\n\n') 
                    else:
                        print('\n[' + str (datetime.now()) + '] ' +  'Remote not ready <- debug message only , for check remote status.\n')
                        return ''           

            except:
                print('write buffer error')

    def waitready():
            if rassh == False:
                    Bsleep(1)
            else:
                    Bsleep(5)
            writebuffer()
            return 1
            ''' # 2019/1/3 mark 這段會卡, 暫時改用 Bsleep 
            #global buffdata
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
        #buffdata
        x = 0
        textready = False
        while not textready and x < 10:
            writebuffer()

            if txt in buffdata[0]:
                print('\n[' + str (datetime.now()) + '] ' + 'waiting specific text: '+ str(txt) + ' | success!!')
                return 1
                
                
            x += 1
            time.sleep(1)
            print('\n[' + str (datetime.now()) + '] ' + 'waiting specific text: '+ str(txt) + ' | ' + str(x) + 'sec\n')
            if x == 10:
                print('\n[' + str (datetime.now()) + '] Warring !! wait 10 sec server not ready , pass wait , please check !!\n')
                return 0
        
        

    def proccomm(wait,times,command):
            #buffdata
            for i in range(int(times)):
                    commands = command + '\n'
                    x = 0
                    remote_conn.send('\n')
                    if waitready() == 0:
                         break

                    remote_conn.send(commands)
                    info1 = '\n[' + str (datetime.now()) + '] ' + 'RA Send: ' + commands + '\n'
                    print(info1)
                    Bsleep(int(wait))

                    
                    

                    if pyver == 2: #Python 2 相容
                        output = remote_conn.recv(6000)
                    else:
                        output = remote_conn.recv(6000).decode()
                        
                    buffdata[0] = "".join([buffdata[0],output])
                    info1 = '\n[' + str (datetime.now()) + '] ' +  'RA Receive: ' + '\n\n' + output + '\n\n'
                    print(info1)
    
    writebuffer()
    #time.sleep(10) # 2018/3 不知為什麼 RA Server 反應越來越慢, 增加送 cammand 前等待
    waitready()
        
    
    if rassh is True: # 以序號連結
        rcount = 0
        while 'Web admin:' not in buffdata[0] and rcount < 3:
            rcount += 1     
            proccomm(3,1,"sshbalance " + SN)
            if 'OFFLINE' in buffdata[0]:
                print('[RA faild] Device ' + SN + ' is OFFLINE')
            waitready()
        if 'Web admin:' in buffdata[0]:      
            raconnected = True

                

    elif raaddkeyto is True: # 以序號加 ssh key     
        rcount = 0
        while 'Web admin:' not in buffdata[0] and rcount < 3:
           
            rcount += 1     
            proccomm(3,1,"addkeyto " + SN)
            if 'OFFLINE' in buffdata[0]:
                print('[RA faild] Device ' + SN + ' is OFFLINE')
            waitready()
            waittext('Added your public key to the device')
            '''
            proccomm(3,1,"sshbalance " + SN)
            if 'OFFLINE' in buffdata[0]:
                print('[RA faild] Device ' + SN + ' is OFFLINE')
            waitready()
            proccomm(10,1,'ssh_activate start_and_listen')            
            '''
              
    elif rassh is False and raaddkeyto is False: # 以 IP 直連
            print('Direct Access Mode')
            rcount = 0
            waitready()
            print(buffdata[0])
            if 'BusyBox' in buffdata[0]:      
                    raconnected = True

           


    if raconnected is True:
        with open(racomm, 'r') as tasklist:
                taskreader = csv.reader(tasklist, delimiter=';', quotechar='"',escapechar='\\')                
                for row in taskreader:
                        if row == []:
                            continue
                        info1 =  '\n[' + str (datetime.now()) + '] ' +'Found CSV row: %s' % ','.join(row)
                        print(info1)
                        wait = row[0]
                        times = row[1]
                        command = row[2]
                        proccomm(wait,times,command)

    
    c.close()
    print('RA Disconnected')
    print('\n\n----[print last RA Data , Start]--------------\n\n')
    print(buffdata[0])
    print('\n----[print last RA Data , End]----------------\n\n')
    return buffdata[0]


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
    print(info1)

    
    if int(sver) == 0:
        if int(SWver) <= int(ever):
            print('-' + str(SWver) + ' <= ' + str (ever) + ' | now process | ' + str(cmd))
            exec (cmd)
        else:
            print('-' + str(SWver) + ' > ' + str (ever) + ' | will not process | ' + str(cmd))
            return 0
        
    elif int(ever) == 0:
        if int(SWver) >= int(sver):            
            print('-' + str(SWver) + ' >= ' + str (sver) + ' | now process | ' + str(cmd))
            exec (cmd)
        else:
            print('-' + str(SWver) + ' < ' + str (sver) + ' | will not process | ' + str(cmd))
            return 0

    else:
        if int(SWver) <= int(ever) and int(SWver) >= int(sver):
            print('-' + str(SWver) + ' does between ' + str (sver) + ' and ' + str (ever) + ' | now process | ' + str(cmd))
            exec (cmd)

        else:
            print('-' + str(SWver) + ' not between ' + str (sver) + ' and ' + str (ever) + ' | will not process | ' + str(cmd))
            return 0    
    

def ConfigUnpack (config_file,CONFIG_DIR='config_tmp'): # 解 config

    info = 'ConfigUnpack | ' + str(config_file) + ' | ' + str(CONFIG_DIR)
    print (PogoPeplinkInfo (info , 'Start'))

    TMP_TGZ_FILE='tmp.pogo.tgz'
    

    cmd = 'mkdir -p ' + CONFIG_DIR
    Popen(cmd, shell=True).wait()

    cmd = 'dd if=' + config_file + ' of=' + TMP_TGZ_FILE +' bs=1 skip=36'
    Popen(cmd, shell=True).wait()

    cmd = 'tar xvzf ' + TMP_TGZ_FILE + ' -C ' + CONFIG_DIR
    Popen(cmd, shell=True).wait()

    cmd = 'rm -f ' + TMP_TGZ_FILE
    Popen(cmd, shell=True).wait()

    print (PogoPeplinkInfo (info , 'End'))

def ConfigPack (config_file,CONFIG_DIR='config_tmp'): # 重包 config 成 conf.updated !! 注意需要原始 config 檔存在

    info = 'ConfigPack | ' + str(config_file) + ' | ' + str(CONFIG_DIR)
    print (PogoPeplinkInfo (info , 'Start'))

    TMP_TGZ_FILE='tmp.pogo.tgz'
        
    cmd = '(cd ' + CONFIG_DIR + ' ; echo $(md5sum config > __md5__))'
    Popen(cmd, shell=True).wait()

    cmd = 'tar czf ' + TMP_TGZ_FILE + ' -C ' + CONFIG_DIR + '/ .'
    Popen(cmd, shell=True).wait()
   
    cmd = '( dd if=' + config_file + ' bs=1 count=36 ; dd if=' + TMP_TGZ_FILE + ' ) > ' + config_file + '.updated'
    Popen(cmd, shell=True).wait()

    cmd = 'rm -f ' + TMP_TGZ_FILE
    Popen(cmd, shell=True).wait()

    print (PogoPeplinkInfo (info , 'End'))


def ConfigPatchM (modify , patch_file,CONFIG_DIR='config_tmp'): # ConfigPatch M mode 的快速語法
    ConfigPatch (patch_file,CONFIG_DIR,'M',modify)    


def ConfigPatch (patch_file,CONFIG_DIR='config_tmp',mode='S',modify=''): # 比對 patch 文檔寫入 config

    '''
    mode = 'M' 時啟動字元置換, 會把 patch_file 中 有 && 的更換為你想要的字串
    
    '''


    info = 'ConfigPatch | ' + str(patch_file) + ' | ' + str(CONFIG_DIR)
    print (PogoPeplinkInfo (info , 'Start'))    

    templine = ''
    tempadd = ''
    
    patch_of = open(patch_file,'r')
    print (PogoPeplinkInfo (info , 'Patch loaded: ' + str(patch_file)))
    
    patch_ofd = patch_of.readlines()

    config_of = open(CONFIG_DIR + '/config' ,'r')
    print (PogoPeplinkInfo (info , 'Config folder loaded: ' + str(CONFIG_DIR)))
    config_ofd = config_of.readlines()

    
    for pi , pline in enumerate(patch_ofd):

        if mode is 'M':
            pline = pline.replace('&&',modify)
                
        if '+' in pline[:2:]:            
            pdata = pline[2::].split('=',1)         

            vmatch = False
            for ci , cline in enumerate(config_ofd):            
                cdata = cline.split('=',1)
                if cdata[0] == pdata[0]:
                    config_ofd[ci] = pline[2::]
                    vmatch = True
                    print (PogoPeplinkInfo (info , 'Config modified: ' + str(cdata[0]) + ' | ' + str(cdata[1]) + ' | ' + str(pdata[1])))

            if vmatch is False:                        
                tempadd += pline[2::]
                print (PogoPeplinkInfo (info , 'Config added: ' + pline[2:-2:]))

        if '-' in pline[:2:]:
            pdata = pline[2::].split('=',1)
                   
            for ci , cline in enumerate(config_ofd):
                cdata = cline.split('=',1)
                if cdata[0] == pdata[0]:
                    config_ofd[ci] = ''
                    print (PogoPeplinkInfo (info , 'Config deleted: ' + pline[2:-2:]))

    templine = config_ofd

    config_of.close()
    config_of = open(CONFIG_DIR + '/config' ,'w')    
    config_of.writelines(templine)
    config_of.write(tempadd)
    patch_of.close()
    config_of.close()
    print (PogoPeplinkInfo (info , 'End'))

def ConfigCompare (source_file, modified_file, exp_patch = 'PogoPatch.txt'): #比對 config , 自動生成 patch 檔

    info = 'ConfigCompare | ' + str(source_file) + ' | ' + str(modified_file) + ' | ' + str(exp_patch)
    print (PogoPeplinkInfo (info , 'Start'))
    tempadd = ''
    
    source_of = open(source_file,'r')
    source_ofd = source_of.readlines()
    print (PogoPeplinkInfo (info , 'Source loaded: ' + source_file))
    
    modified_of = open(modified_file,'r')
    modified_ofd = modified_of.readlines()
    print (PogoPeplinkInfo (info , 'Modifid loaded: ' + modified_file))

    patch_of = open(exp_patch, 'w')
    print (PogoPeplinkInfo (info , 'Patch created: ' + exp_patch))

    for mi , mline in enumerate(modified_ofd):
        mdata = mline.split('=',1)

        vmatch = False
        for si , sline in enumerate(source_ofd):
            sdata = sline.split('=',1)
            if sdata[0] ==  mdata[0]:
                vmatch = True
                if sdata[1] != mdata[1]:
                    tempadd += '+ ' + mline
                    print (PogoPeplinkInfo (info , 'Compare find: ' + '+ ' + mline))
    
        if vmatch is False:
            tempadd += '+ ' +mline
            print (PogoPeplinkInfo (info , 'Compare find: ' + '+ ' + mline))

    for si , sline in enumerate(source_ofd):
        sdata = sline.split('=',1)

        vmatch = False
        for mi , mline in enumerate(modified_ofd):
            mdata = mline.split('=',1)
            if sdata[0] ==  mdata[0]:
                vmatch = True                
    
        if vmatch is False:
            tempadd += '- ' +sline
            print (PogoPeplinkInfo (info , 'Compare find: ' + '- ' + sline))

    
       
    patch_of.write(tempadd)
    patch_of.close()
    source_of.close()
    modified_of.close()
    print (PogoPeplinkInfo (info , 'End'))
    
def UIDconfigD(driver,url,usern = 'admin', passw = 'Admin!2345'): # 自動下載 config 

    info = 'UIDconfigD | ' + str(driver) + ' | ' + str(url) + ' | ' + str(usern) + ' | ' + str(passw)
    print (PogoPeplinkInfo (info , 'Start'))    

    SUIsLoginD(driver,url,usern, passw)#Login
    BvisitD (driver,url + '/cgi-bin/MANGA/index.cgi?mode=config&option=utconfig')
    BclickTD(driver,"Download")
    Bsleep(5)
    Configfolder = '/home/peplink/Downloads/'
    Flist = [f for f in os.listdir(Configfolder) if re.match(r'(.*?).conf',f) ]
    lastConfig = Configfolder + Flist[-1]
    print (PogoPeplinkInfo (info , 'End'))
    return lastConfig
    


def UIUconfigD(driver,url, filename, usern = 'admin', passw = 'Admin!2345'): #  自動上傳 config

    info = 'UIUconfigD | ' + str(driver) + ' | ' + str(url) + ' | ' + str(filename) + ' | ' + str(usern) + ' | ' + str(passw)
    print (PogoPeplinkInfo (info , 'Start'))     

    SUIsLoginD(driver,url,usern, passw)#Login
    BvisitD (driver,url + '/cgi-bin/MANGA/index.cgi?mode=config&option=utconfig')
    Bsleep(2)
    BfillTD (driver,'Configuration File',filename)
    Bsleep(2)
    BclickTD (driver, 'Upload','1')
    Bsleep(2)
    print (PogoPeplinkInfo (info , 'End'))
    

def CleanFolder(folder = '/home/peplink/Downloads'):

    info = 'CleanFolder | ' + str(folder)
    print (PogoPeplinkInfo (info , 'Start')) 
    shutil.rmtree(folder)
    os.makedirs(folder)
    print (PogoPeplinkInfo (info , 'End'))


def ConfigChange (config_file, patch_file,CONFIG_DIR='config_tmp'): # 直接 patch config 檔後生成 config.update

    cmd = 'rm ' + config_file + '.update -f'
    Popen(cmd, shell=True).wait()
    
    ConfigUnpack (config_file, CONFIG_DIR)
    ConfigPatch (patch_file, CONFIG_DIR)
    ConfigPack (config_file, CONFIG_DIR)

def ConfigChangeM (modify, config_file, patch_file,CONFIG_DIR='config_tmp'): # 直接 patch config 檔後生成 config.update M mode

    cmd = 'rm ' + config_file + '.update -f'
    Popen(cmd, shell=True).wait()
    
    ConfigUnpack (config_file, CONFIG_DIR)
    ConfigPatchM (modify, patch_file, CONFIG_DIR)
    ConfigPack (config_file, CONFIG_DIR)
    

def ConfigCompareF (source_config, modified_config, exp_patch = 'PogoPatch.txt'): #直接比對 config 檔, 生成差異文件

    ConfigUnpack (source_config , 'config_tmp1')
    ConfigUnpack (modified_config , 'config_tmp2')
    ConfigCompare ('config_tmp1/config' , 'config_tmp2/config' , exp_patch)
    
    
