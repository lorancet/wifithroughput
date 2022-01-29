#-*- coding: utf-8 -*-
'''
主要 Smoke 測試相關控制元件

2021/10/20 1.1.0 AndersonW 增加FH_UIresetD, FH_default_login, SFC_UIresetD, SFC_default_login 測試
2021/08/12 1.0.9 AndersonW 增加Config_File_Upload3M , Config_File_Upload3MM
2020/10/19 1.0.8 UIRestD 相關功能修正相容
2020/09/18 1.0.7 tn.close -> tn.close()
2020/09/11 1.0.6 LABINFO 支援
2020/09/10 1.0.5 環境變數調整
2020/09/08 1.0.4 bug fix
2020/09/07 1.0.3 drop-in 網卡切換對應
2020/08/20 1.0.2 Email From 修正
2020/08/19 1.0.1 bug fix , 改 email 通知 Gamil
2020/08/13 1.0.0 First Release


'''



from config import *
from Smoke_Update import *
from Smoke_Modules.LoSmokTest_PEPLINK import *
from Smoke_Modules.modules import *

'''
PogoUpdate1('B310_Smoke_Test_Balance.py','/QaPythonTemp/QaAutoRunTest/U64_Smoke_Test/','')

UpdateSfolder = 'QaPythonTemp/QaAutoRunTest/U64_Smoke_Test/ConfigFile/T02'
UpdateDfolder = 'ConfigFile/T02'
PogoUpdateF(UpdateSfolder,UpdateDfolder)
'''
script_dir = os.path.dirname(__file__)
#logging.basicConfig(level=logging.INFO)

# Pogo 改部分

#testWAN = '1' #測試的 WAN, 程式內有 判斷 MOTG 改為5, 有需要調到不同WAN測試改這兒, 用USB 設為 'E'

IpAdd = '192.168.1.1' #設備IP
pepurl = 'http://'+IpAdd #http:// + 設備IP

intC = 'ens3'
extC = 'ens4'
FHLANC = 'ens5'

#OWPath = os.getcwd() # 工作起始目錄
#DefaultCFG1 = OWPath + '/Config2/default1.conf' #生成的 預設 config 檔完整檔名與路徑, 重要!!

LOGName = "Pogo_Smoke_T1"
logging.basicConfig( stream=sys.stderr )
logging.getLogger( LOGName ).setLevel( logging.DEBUG )
log= logging.getLogger(LOGName)

try:
    print (LABINFO)
except:
    LABINFO = ''
    print ('please add LABINFO = "any txt" to config.py')



def NIC_Down(nic): #關卡
    Popen('nmcli device disconnect '+ nic ,shell=True).wait()
    #Bsleep(10)

def NIC_Up(nic): #開卡
    Popen('nmcli device connect '+ nic ,shell=True).wait()
    #Bsleep(10)

def NIC_Res(nic): #重啟卡
    NIC_Down(nic)
    NIC_Up(nic)
    #Bsleep(10)

def NIC_extC_Down_intC_DHCP(): # 外卡關 內卡DHCP , 含重啟網卡
    #Popen('nmcli connection down "static-intC"',shell=True).wait()
    #Popen('nmcli connection down "di-static-intC"',shell=True).wait()
    Popen('nmcli connection up "dhcp-intC"',shell=True).wait()
    if platform.system() == 'Linux':
        os_uname = platform.uname()
        if not ('16.04' in os_uname[3]):
            print ('Need to wait 10 sec for "dhcp-intC" up in Ubuntu 21' )#AW test
            time.sleep(10)
    NIC_Down(extC)
    NIC_Res(intC)

def NIC_extC_Up_intC_Static(): # 外卡開 內卡static IP , 含重啟網卡
    #Popen('nmcli connection down "dhcp-intC"',shell=True).wait()
    #Popen('nmcli connection down "di-static-intC"',shell=True).wait()
    Popen('nmcli connection up "static-intC"',shell=True).wait()
    NIC_Res(extC)
    NIC_Res(intC)

def NIC_extC_Down_intC_diStatic(): # 外卡關 內卡drop-in static IP , 含重啟網卡
    #Popen('nmcli connection down "dhcp-intC"',shell=True).wait()
    #Popen('nmcli connection down "static-intC"',shell=True).wait()
    Popen('nmcli connection up "di-static-intC"',shell=True).wait()
    NIC_Down(extC)
    NIC_Res(intC)



#UI 回預設值
def UIRestD1(config_file=DefaultCFG1,url=pepurl): # Reset Default , 再調回 預設 config
    
    UIRestD(url)

    NIC_extC_Down_intC_DHCP()
    
    if ispepwave == True:

        NIC_Res(extC)

        NIC_Res(intC)

        if PingCheck('192.168.50.1'):       
        
            IpAdd = '192.168.50.1'
            pepurl = 'http://'+IpAdd #http:// + 設備IP
            url = pepurl
    else:
        IpAdd = '192.168.1.1' 
        pepurl = 'http://'+IpAdd #http:// + 設備IP
        url = pepurl
        
    try:
        testAdd = url.replace('http://','')
        testAdd = testAdd.replace('https://','')
        testAdd = testAdd.replace('/','')
        
        if PingCheck(testAdd):
            driver = Bopen()
            UIsLogin (url)
            Bsleep(120)
            Bquit()
    except:
        Bsleep(120)
        driver = Bopen()
        UIsLogin (url)        
        Bsleep(120)
        Bquit()
    #以上的用途在小設備 reset default 後, 第一次登入會改 id pass , 太快再上傳 config 就死機


    Config_File_Upload1(config_file,url)

    if ispepwave == True:

        NIC_Res(extC)

        NIC_Res(intC)
      
        IpAdd = '192.168.1.1' 
        pepurl = 'http://'+IpAdd #http:// + 設備IP  


def UIRestD2(patch_file,config_file=DefaultCFG1,url=pepurl): # Reset Default , 再 上傳修改的 config
    
    UIRestD(url)

    NIC_extC_Down_intC_DHCP()
    
    if ispepwave == True:

        NIC_Res(extC)

        NIC_Res(intC)

        if PingCheck('192.168.50.1'):       
        
            IpAdd = '192.168.50.1'
            pepurl = 'http://'+IpAdd #http:// + 設備IP
            url = pepurl

    else:
        IpAdd = '192.168.1.1' 
        pepurl = 'http://'+IpAdd #http:// + 設備IP
        url = pepurl

    try:
        testAdd = url.replace('http://','')
        testAdd = testAdd.replace('https://','')
        testAdd = testAdd.replace('/','')
        
        if PingCheck(testAdd):
            driver = Bopen()
            UIsLogin (url)
            Bsleep(120)
            Bquit()
    except:
        Bsleep(120)
        driver = Bopen()
        UIsLogin (url)
        Bsleep(120)
        Bquit()
    #以上的用途在小設備 reset default 後, 第一次登入會改 id pass , 太快再上傳 config 就死機            

    Config_File_Upload2(patch_file,config_file,url)

    if ispepwave == True:

        NIC_Res(extC)

        NIC_Res(intC)
      
        IpAdd = '192.168.1.1' 
        pepurl = 'http://'+IpAdd #http:// + 設備IP  


def UIRestD(url=pepurl):
    driver = Bopen()
    UIsLogin(url) #Login  
    Bvisit (url + '/cgi-bin/MANGA/index.cgi?mode=config&option=utconfig')
    SBwait('.restore_action')
    SBclick('.restore_action')
    Bwait('button.ui-button:nth-child(1)')
    SBclick('button.ui-button:nth-child(1)')
    Bsleep(240)
    Bsleep(AppWait)
    Bquit()

#For FusionHub reset default in Eric LAB
def FH_UIRsetD(): 
    #NIC_Up(extC)
    #NIC_Up(intC)

    log.debug('s1,000_1')
    driver = Bopen()
    UIsLogin("http://10.88.81.1")
    Bsleep(10)
    Bvisit("http://10.88.81.1/cgi-bin/MANGA/index.cgi?mode=config&option=utconfig")
    Bsleep(2)
    BclickT("Restore Factory Settings")
    Bsleep(2)
    BclickT("Restore and Reboot")
    Bsleep(5)
    Bquit()
    print ("Restore Factory Settings")
    Bsleep(100)


    driver = Bopen()
    Bvisit("http://10.88.81.100/cgi-bin/MANGA/index.cgi")
    Bwait_text('Login')
    Bfill("username","admin")
    Bsleep(2)
    Bfill("password","admin")
    Bsleep(2)
    BclickT("Login","2")
    Bsleep(10)
    Bclick("#forward_button")
    Bsleep(2)
    Bcheck("wan_conn_method_static")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bfill("wan_conn_static_ip","10.88.81.1")
    Bsleep(2)
    Bfill("wan_conn_static_gw","10.88.81.254")
    Bsleep(2)
    Bfill("wan_conn_static_dns1","10.88.3.1")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bcheck("lan_conn_method_static")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bfill("lan_conn_static_ip","192.168.1.1")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bfill("site_id","TEST1")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bclick("#save_setting_button")
    Bsleep(10)
    Bquit()
    Bsleep(20)

    driver = Bopen()
    Bvisit("http://10.88.81.1/cgi-bin/MANGA/index.cgi")
    Bwait_text('Login')
    Bfill("username","admin")
    Bsleep(2)
    Bfill("password","admin")
    Bsleep(2)
    BclickT("Login","2")
    Bsleep(10)
    Bfill("currentPassword","admin")
    Bsleep(2)
    Bfill("newPassword","Admin!2345")
    Bsleep(2)
    Bfill("confirmPassword","Admin!2345")
    Bsleep(2)
    BclickT("Save and apply")
    Bsleep(2)
    BclickT("OK")
    Bsleep(10)

    if Btext('10.88.81.1'):

        print ("PASS")
        Bquit()
        log.debug('p1.000_1')

    else:
        Bquit()
        log.debug('f1.000_1')
    
    print ("FH Login Setup Default")



#For SFC reset default in Eric LAB
def SFC_UIRsetD():
    
    #NIC_extC_Up_intC_Static()

    log.debug('s1,000_1')
    driver = Bopen()
    UIsLogin("http://10.88.81.1")
    Bsleep(10)
    Bvisit("http://10.88.81.1/cgi-bin/MANGA/index.cgi?mode=config&option=utconfig")
    Bsleep(2)
    BclickT("Restore Factory Settings")
    Bsleep(2)
    BclickT("Restore and Reboot")
    Bsleep(5)
    Bquit()
    print ("Restore Factory Settings")
    Bsleep(100)


    driver = Bopen()
    Bvisit("http://10.88.81.100/cgi-bin/MANGA/index.cgi")
    Bwait_text('Login')
    Bfill("username","admin")
    Bsleep(2)
    Bfill("password","admin")
    Bsleep(2)
    BclickT("Login","2")
    Bsleep(10)
    Bfill("currentPassword","admin")
    Bsleep(2)
    Bfill("newPassword","Admin!2345")
    Bsleep(2)
    Bfill("confirmPassword","Admin!2345")
    Bsleep(2)
    BclickT("Save and apply")
    Bsleep(2)
    BclickT("OK")
    Bsleep(10)
    Bvisit("http://10.88.81.100/cgi-bin/MANGA/index.cgi?mode=config&option=qzwan2")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bcheck("wan_conn_method_static")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bfill("wan_conn_static_ip","10.88.81.1")
    Bsleep(2)
    Bfill("wan_conn_static_gw","10.88.81.254")
    Bsleep(2)
    Bfill("wan_conn_static_dns1","10.88.3.1")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bcheck("lan_conn_method_static")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bfill("lan_conn_static_ip","192.168.1.1")
    Bsleep(2)
    BclickTO("","24","0","A")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bfill("site_id","TEST1")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    BclickTO("","6","0","A")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bclick("#save_setting_button")
    Bsleep(10)
    Bquit()
    Bsleep(20)
    driver = Bopen()
    UIsLogin("http://10.88.81.1")
    Bsleep(10)
    Bvisit("http://10.88.81.1/cgi-bin/MANGA/index.cgi?mode=config&option=hubwan")
    Bsleep(5)
    Bncheck("ipp_enable")
    Bsleep(2)
    BclickT("Save")
    Bsleep(5)
    UIsApply("http://10.88.81.1")
    Bsleep(10)

    ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
    Bsleep(2)
    stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.81.1')
    Bsleep(30)
    t = stdout.read()
    print('t',str(t))
    ssh.close()

    if '4 received' in str(t):
        log.debug('c1.000_1')

        print ("PASS")
        Bquit()


        log.debug('p1.000_1')
            
    else:

        log.debug('f1.000_1')
        

    print ("SFC Login Setup Default")




#For FusionHub default login in ERIC LAB, 等測完再移回PogoPeplink.py
def FH_default_login(): 
    log.debug('s1,000')

    driver = Bopen()

    Bvisit("http://10.88.81.100/cgi-bin/MANGA/index.cgi")
    Bwait_text('Login')
    Bfill("username","admin")
    Bsleep(2)
    Bfill("password","admin")
    Bsleep(2)
    BclickT("Login","2")
    Bsleep(10)
    Bclick("#forward_button")
    Bsleep(2)
    Bcheck("wan_conn_method_static")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bfill("wan_conn_static_ip","10.88.81.1")
    Bsleep(2)
    Bfill("wan_conn_static_gw","10.88.81.254")
    Bsleep(2)
    Bfill("wan_conn_static_dns1","10.88.3.1")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bcheck("lan_conn_method_static")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bfill("lan_conn_static_ip","192.168.1.1")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bfill("site_id","TEST1")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bclick("#save_setting_button")
    Bsleep(10)
    Bquit()
    Bsleep(20)
    driver = Bopen()
    Bvisit("http://10.88.81.1/cgi-bin/MANGA/index.cgi")
    Bwait_text('Login')
    Bfill("username","admin")
    Bsleep(2)
    Bfill("password","admin")
    Bsleep(2)
    BclickT("Login","2")
    Bsleep(10)
    Bfill("currentPassword","admin")
    Bsleep(2)
    Bfill("newPassword","Admin!2345")
    Bsleep(2)
    Bfill("confirmPassword","Admin!2345")
    Bsleep(2)
    BclickT("Save and apply")
    Bsleep(2)
    BclickT("OK")
    Bsleep(10)

    if Btext('10.88.81.1'):

        print ("PASS")
        Bquit()
        log.debug('p1.000_1')

    else:
        Bquit()
        log.debug('f1.000_1')
        
    print ("Login Setup Default")

#For SFC default login in ERIC LAB, 等測完再移回PogoPeplink.py
def SFC_default_login():

    #NIC_extC_Up_intC_Static()
    log.debug('s1,000')

    driver = Bopen()
    Bvisit("http://10.88.81.100/cgi-bin/MANGA/index.cgi")
    Bwait_text('Login')
    Bfill("username","admin")
    Bsleep(2)
    Bfill("password","admin")
    Bsleep(2)
    BclickT("Login","2")
    Bsleep(10)
    Bfill("currentPassword","admin")
    Bsleep(2)
    Bfill("newPassword","Admin!2345")
    Bsleep(2)
    Bfill("confirmPassword","Admin!2345")
    Bsleep(2)
    BclickT("Save and apply")
    Bsleep(2)
    BclickT("OK")
    Bsleep(10)
    Bvisit("http://10.88.81.100/cgi-bin/MANGA/index.cgi?mode=config&option=qzwan2")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bcheck("wan_conn_method_static")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bfill("wan_conn_static_ip","10.88.81.1")
    Bsleep(2)
    Bfill("wan_conn_static_gw","10.88.81.254")
    Bsleep(2)
    Bfill("wan_conn_static_dns1","10.88.3.1")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bcheck("lan_conn_method_static")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bfill("lan_conn_static_ip","192.168.1.1")
    Bsleep(2)
    BclickTO("","24","0","A")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bfill("site_id","TEST1")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    BclickTO("","6","0","A")
    Bsleep(2)
    Bclick("#forward_button")
    Bsleep(2)
    Bclick("#save_setting_button")
    Bsleep(10)
    Bquit()
    Bsleep(20)
    driver = Bopen()
    UIsLogin("http://10.88.81.1")
    Bsleep(10)
    Bvisit("http://10.88.81.1/cgi-bin/MANGA/index.cgi?mode=config&option=hubwan")
    Bsleep(5)
    Bncheck("ipp_enable")
    Bsleep(2)
    BclickT("Save")
    Bsleep(5)
    UIsApply("http://10.88.81.1")
    Bsleep(10)

    ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
    Bsleep(2)
    stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.81.1')
    Bsleep(30)
    t = stdout.read()
    print('t',str(t))
    ssh.close()

    if '4 received' in str(t):
        log.debug('c1.000_1')

        print ("PASS")
        Bquit()


        log.debug('p1.000_1')
            
    else:

        log.debug('f1.000_1')
        

    print ("SFC Login Setup Default")

#用來上傳備份好的 Default config
def Config_File_Upload1(config_file=DefaultCFG1,url=pepurl): 
    driver = Bopen()
    UIUconfigD (driver,url,config_file)
    UIsApplyD (driver, url)
    Bsleep(120)
    Bsleep(AppWait)
    Bquit()    

#用來上傳 修改的 config
def Config_File_Upload2(patch_file,config_file=DefaultCFG1,url=pepurl):
    ConfigChange (config_file , patch_file)
    driver = Bopen()
    UIUconfigD (driver,url,config_file+'.updated')
    UIsApplyD (driver, url)
    Bsleep(120)
    Bsleep(AppWait)
    Bquit()    

#用來上傳 修改的 config M mode
def Config_File_Upload2M(modify, patch_file,config_file=DefaultCFG1,url=pepurl):
    ConfigChangeM (modify, config_file , patch_file)
    driver = Bopen()
    UIUconfigD (driver,url,config_file+'.updated')
    UIsApplyD (driver, url)
    Bsleep(120)
    Bsleep(AppWait)
    Bquit()
    
#先修改一般config-file後,
#再上傳 另外增加修改的 config M mode
def Config_File_Upload3M(modify, patch_file, patch_file_1,config_file=DefaultCFG1,url=pepurl):
    cmd = 'rm ' + config_file + '.temp1 -f'
    Popen(cmd, shell=True).wait()
    cmd = 'rm ' + config_file + '.temp1.updated -f'
    Popen(cmd, shell=True).wait()
    #先用Config-case???生成設定
    ConfigChange (config_file , patch_file)
    cmd = 'mv ' + config_file + '.updated ' + config_file + '.temp1'
    Popen(cmd, shell=True).wait()
    #再合成特別需求的設定,比如再加上Config-wifiwan.txt
    DefaultCFG2 = DefaultCFG1 + '.temp1'
    ConfigChangeM (modify, DefaultCFG2 , patch_file_1)
    driver = Bopen()
    UIUconfigD (driver,url,config_file+'.temp1.updated')
    UIsApplyD (driver, url)
    Bsleep(120)
    Bsleep(AppWait)
    Bquit()        

#先修改一般config-file而且是 M mode,
#再上傳 另外增加修改的 config M mode
def Config_File_Upload3MM(modify,modify_1, patch_file, patch_file_1,config_file=DefaultCFG1,url=pepurl):
    cmd = 'rm ' + config_file + '.temp1 -f'
    Popen(cmd, shell=True).wait()
    cmd = 'rm ' + config_file + '.temp1.updated -f'
    Popen(cmd, shell=True).wait()
    #先用Config-case???生成設定,而且是M mode
    ConfigChangeM (modify, config_file , patch_file)
    cmd = 'mv ' + config_file + '.updated ' + config_file + '.temp1'
    Popen(cmd, shell=True).wait()
    #再合成特別需求的設定,比如再加上Config-wifiwan.txt
    DefaultCFG2 = DefaultCFG1 + '.temp1'
    ConfigChangeM (modify_1, DefaultCFG2 , patch_file_1)
    driver = Bopen()
    UIUconfigD (driver,url,config_file+'.temp1.updated')
    UIsApplyD (driver, url)
    Bsleep(120)
    Bsleep(AppWait)
    Bquit()        

#Debug 加顏色
def add_coloring_to_emit_windows(fn):
        # add methods we need to the class
    def _out_handle(self):
        import ctypes
        return ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
    out_handle = property(_out_handle)

    def _set_color(self, code):
        import ctypes
        # Constants from the Windows API
        self.STD_OUTPUT_HANDLE = -11
        hdl = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetConsoleTextAttribute(hdl, code)

    setattr(logging.StreamHandler, '_set_color', _set_color)

    def new(*args):
        FOREGROUND_BLUE      = 0x0001 # text color contains blue.
        FOREGROUND_GREEN     = 0x0002 # text color contains green.
        FOREGROUND_RED       = 0x0004 # text color contains red.
        FOREGROUND_INTENSITY = 0x0008 # text color is intensified.
        FOREGROUND_WHITE     = FOREGROUND_BLUE|FOREGROUND_GREEN |FOREGROUND_RED
       # winbase.h
        STD_INPUT_HANDLE = -10
        STD_OUTPUT_HANDLE = -11
        STD_ERROR_HANDLE = -12

        # wincon.h
        FOREGROUND_BLACK     = 0x0000
        FOREGROUND_BLUE      = 0x0001
        FOREGROUND_GREEN     = 0x0002
        FOREGROUND_CYAN      = 0x0003
        FOREGROUND_RED       = 0x0004
        FOREGROUND_MAGENTA   = 0x0005
        FOREGROUND_YELLOW    = 0x0006
        FOREGROUND_GREY      = 0x0007
        FOREGROUND_INTENSITY = 0x0008 # foreground color is intensified.

        BACKGROUND_BLACK     = 0x0000
        BACKGROUND_BLUE      = 0x0010
        BACKGROUND_GREEN     = 0x0020
        BACKGROUND_CYAN      = 0x0030
        BACKGROUND_RED       = 0x0040
        BACKGROUND_MAGENTA   = 0x0050
        BACKGROUND_YELLOW    = 0x0060
        BACKGROUND_GREY      = 0x0070
        BACKGROUND_INTENSITY = 0x0080 # background color is intensified.     

        levelno = args[1].levelno
        if(levelno>=50):
            color = BACKGROUND_YELLOW | FOREGROUND_RED | FOREGROUND_INTENSITY | BACKGROUND_INTENSITY 
        elif(levelno>=40):
            color = FOREGROUND_RED | FOREGROUND_INTENSITY
        elif(levelno>=30):
            color = FOREGROUND_YELLOW | FOREGROUND_INTENSITY
        elif(levelno>=20):
            color = FOREGROUND_GREEN
        elif(levelno>=10):
            #color = FOREGROUND_MAGENTA
            color = BACKGROUND_BLUE | FOREGROUND_MAGENTA | FOREGROUND_INTENSITY | BACKGROUND_INTENSITY
  
        else:
            color =  FOREGROUND_WHITE
        args[0]._set_color(color)

        ret = fn(*args)
        args[0]._set_color( FOREGROUND_WHITE )
        #print "after"
        return ret
    return new

def add_coloring_to_emit_ansi(fn):
    # add methods we need to the class
    def new(*args):
        levelno = args[1].levelno
        if(levelno>=50):
            #color = '\x1b[31m' # red
            color = '\x1b[0;30;41m' # 紅底黑字
        elif(levelno>=40):
            #color = '\x1b[31m' # red
            color = '\x1b[0;30;41m' # 紅底黑字
        elif(levelno>=30):
            #color = '\x1b[33m' # yellow
            color = '\x1b[5;30;43m' # 亮黃底黑字
        elif(levelno>=20):
            #color = '\x1b[32m' # green
            color = '\x1b[1;32;42m' # 綠底亮綠字
        elif(levelno>=10):
            #color = '\x1b[35m' # pink
            color = '\x1b[1;35;44m' # 藍底亮紫字
        else:
            color = '\x1b[0m' # normal
        args[1].msg = color + args[1].msg +  '\x1b[0m'  # normal
        #print "after"
        return fn(*args)
    return new

import platform
if platform.system()=='Windows':
    # Windows does not support ANSI escapes and we are using API calls to set the console color
    logging.StreamHandler.emit = add_coloring_to_emit_windows(logging.StreamHandler.emit)
else:
    # all non-Windows platforms are supporting ANSI escapes so we use them
    logging.StreamHandler.emit = add_coloring_to_emit_ansi(logging.StreamHandler.emit)
    #log = logging.getLogger()
    #log.addFilter(log_filter())
    #//hdlr = logging.StreamHandler()
    #//hdlr.setFormatter(formatter())    



#以上


def Config_File_Upload(FileName):

    IpAdd = '192.168.1.1'
    pepurl = 'http://'+IpAdd #http:// + 設備IP
    FilePath = '/home/peplink/QA/QaPythonTemp/QaAutoRunTest/U64_Smoke_Test/ConfigFile/T02/'
    ConfigFile = FilePath + FileName
    driver = Bopen()
    UIsLogin(pepurl)
    Bsleep(2)
    Bvisit(pepurl + '/cgi-bin/MANGA/index.cgi?mode=config&option=utconfig')
    Bsleep(2)
    #BfillT('Configuration File',ConfigFile)
    Bfill('#config_panel > form:nth-child(7) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > input:nth-child(1)',ConfigFile)
    Bsleep(2)
    #BclickT ('Upload')
    Bclick('#config_panel > form:nth-child(7) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > button:nth-child(1)')
    Bsleep(10)
    UIsApply(pepurl)
    Bsleep(10)
    Bsleep(60)
    Bquit()


def U64Reboot():

    SSHD = ["10.88.80.11","192.168.1.8","192.168.1.9"]
    for iSSHD in SSHD:
        print (iSSHD)

        if  PingCheck(iSSHD) == 1:
            print ('Porcess reboot ' + iSSHD)
            try:
                #paramiko.util.log_to_file('sshtest.log')
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(iSSHD , port=22 ,username='peplink' , password='peplink')
                stdin, stdout, stderr = ssh.exec_command('sudo -S reboot')
                stdin.write('peplink'+'\n')
                stdin.flush()
                ssh.close()

                for std in stdout.readlines():
                    #log.write(std)
                    print (std),
                

            #except Exception,e: #python2
            except Exception as e: #python2 and python3
                print ('U64 Reboot failed:',e)            
                print (e)
                ssh.close()

def SendMail(to,sub,txtinfo,htmlinfo):
    
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib

    try:
        msg = MIMEMultipart()
        msg["Subject"] = sub
        msg["From"] = "TW LAB Auto Notify"
        msg["To"] = to    
        msg["Cc"] = ""
        body1 = MIMEText(txtinfo , 'plain')
        body2 = MIMEText(htmlinfo , 'html')

        msg.attach(body1)
        msg.attach(body2)
        
        username = 'twlab@peplink.com'
        password = 'oydflulkwahforgi'
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(msg["From"], msg["To"].split(",") + msg["Cc"].split(","), msg.as_string())
        server.quit()
        print ('SendMail() Success:')

    except Exception as e:
        print ('SendMail() failed:',e)
        return 0

    return 1

               



def TestDefault():

    print ('[TestDefault()]========================================================================================================================')

    #避免前面測試有異常中斷沒關乾淨
    try:
        
        Bquit()        
        #Popen ('pkill -9 chrome',shell=True).wait()
        #print ('clear chrome process')
        log.debug('c1-1.000')        
    except:
        log.debug('c1-f.000')

    try:
        ssh.close()        
        log.debug('c2-1.000')        
    except:
        log.debug('c2-f.000')

    try:
        os.chdir(OWPath)
        log.debug('c3-1.000')
    except:
        log.debug('c3-f.000')

    

        
        
    Config_File_Upload1()
    Bsleep(AppWait)
    
    NIC_extC_Down_intC_DHCP()
    Bsleep(10)
    log.debug('preset.000')
    

def setup_module(module): #每個 test case 前執行
    
    global count
    count = 0
    
    TestDefault()

def wan_sw_assign_vlantag():

    try:
        tn = telnetlib.Telnet(HOST)
        Bsleep(2)
        tn.read_until(b"User:")
        Bsleep(2)
        tn.write(b"admin\r\n")
        Bsleep(2)
        tn.read_until(b"Password:")
        Bsleep(2)
        tn.write (b'\r\n')
        Bsleep(2)
        tn.write(b"enable\r\n")
        Bsleep(2)        
        tn.write(b"config\r\n")
        Bsleep(2)
        tn.write(b"interface 0/"+str(PORT).encode('ascii')+b"\r\n")
        Bsleep(2)
        tn.write(b"vlan tag "+str(VID).encode('ascii')+b"\r\n")
        Bsleep(2)
        tn.write(b"no vlan pvid\r\n")
        Bsleep(2)
        tn.write(b"exit\r\n")
        Bsleep(2)
        tn.close()
        print ("port"+PORT+" assign tag "+VID)
    except Exception as e:
        print ('wan_sw_assign_vlantag() failed:',e)
        return 0

    return 1

def wan_sw_port_up():

    try:
        tn = telnetlib.Telnet(HOST)
        time.sleep(2)
        tn.read_until(b"User:")
        time.sleep(2)
        tn.write(b"admin\r\n")
        time.sleep(2)
        tn.read_until(b"Password:")
        time.sleep(2)
        tn.write (b'\r\n')
        time.sleep(2)
        tn.write(b"enable\r\n")
        time.sleep(2)        
        tn.write(b"config\r\n")
        time.sleep(2)
        tn.write(b"interface 0/"+str(PORT).encode('ascii')+b"\r\n")
        time.sleep(2)
        tn.write(b"no shutdown\r\n")
        time.sleep(2)
        tn.write(b"exit\r\n")
        tn.close()
    except Exception as e:
        print ('wan_sw_port_up() failed:',e)
        return 0

    return 1

def wan_sw_assign_vlan3002():

    try:
        tn = telnetlib.Telnet(HOST)
        Bsleep(2)
        tn.read_until(b"User:")
        Bsleep(2)
        tn.write(b"admin\r\n")
        Bsleep(2)
        tn.read_until(b"Password:")
        Bsleep(2)
        tn.write (b'\r\n')
        Bsleep(2)
        tn.write(b"enable\r\n")
        Bsleep(2)        
        tn.write(b"config\r\n")
        Bsleep(2)
        tn.write(b"interface 0/"+str(PORT).encode('ascii')+b"\r\n")
        Bsleep(2)
        tn.write(b"vlan participation include 3002\r\n")
        Bsleep(2)
        tn.write(b"vlan pvid 3002\r\n")
        Bsleep(2)
        tn.write(b"exit\r\n")
        Bsleep(2)
        tn.close()
        print ("port"+PORT+" assign untag 3002")
    except Exception as e:
        print ('wan_sw_assign_vlan3002() failed:',e)
        return 0

    return 1



def wan_sw_unassign_vlantag():

    try:
        tn = telnetlib.Telnet(HOST)
        Bsleep(2)        
        tn.read_until(b"User:")
        Bsleep(2)
        tn.write(b"admin\r\n")
        Bsleep(2)
        tn.read_until(b"Password:")
        Bsleep(2)
        tn.write (b'\r\n')
        Bsleep(2)
        tn.write(b"enable\r\n")
        Bsleep(2)
        tn.write(b"config\r\n")
        Bsleep(2)
        tn.write(b"interface 0/"+str(PORT).encode('ascii')+b"\r\n")
        Bsleep(2)
        tn.write(b"vlan pvid "+str(VID).encode('ascii')+b"\r\n")
        Bsleep(2)
        tn.write(b"no vlan tag "+str(VID).encode('ascii')+b"\r\n")
        Bsleep(2)
        tn.write(b"exit\r\n")
        Bsleep(2)
        tn.close()
        print ("port"+PORT+" assign untag "+VID)
    except Exception as e:
        print ('wan_sw_unassign_vlantag() failed:',e)
        return 0

    return 1

def wan_sw_unassign_vlan3002():

    try:
        tn = telnetlib.Telnet(HOST)
        Bsleep(2)        
        tn.read_until(b"User:")
        Bsleep(2)
        tn.write(b"admin\r\n")
        Bsleep(2)
        tn.read_until(b"Password:")
        Bsleep(2)
        tn.write (b'\r\n')
        Bsleep(2)
        tn.write(b"enable\r\n")
        Bsleep(2)
        tn.write(b"config\r\n")
        Bsleep(2)
        tn.write(b"interface 0/"+str(PORT).encode('ascii')+b"\r\n")
        Bsleep(2)
        tn.write(b"vlan pvid "+str(VID).encode('ascii')+b"\r\n")
        Bsleep(2)
        tn.write(b"vlan participation auto 3002\r\n")
        Bsleep(2)
        tn.write(b"exit\r\n")
        Bsleep(2)
        tn.close()
        print ("port"+PORT+" assign untag "+VID)
    except Exception as e:
        print ('wan_sw_unassign_vlan3002() failed:',e)
        return 0

    return 1

def wan_sw_port_down():

    try:
        tn = telnetlib.Telnet(HOST)
        time.sleep(2)
        tn.read_until(b"User:")
        time.sleep(2)
        tn.write(b"admin\r\n")
        time.sleep(2)
        tn.read_until(b"Password:")
        time.sleep(2)
        tn.write (b'\r\n')
        time.sleep(2)
        tn.write(b"enable\r\n")
        time.sleep(2)        
        tn.write(b"config\r\n")
        time.sleep(2)
        tn.write(b"interface 0/"+str(PORT).encode('ascii')+b"\r\n")
        time.sleep(2)
        tn.write(b"shutdown\r\n")
        time.sleep(2)
        tn.write(b"exit\r\n")
        tn.close()
    except Exception as e:
        print ('wan_sw_port_down() failed:',e)
        return 0

    return 1

   
    
    
    
    
