#-*- coding: utf-8 -*-
# 20190214001  新增自動上傳Report

from SmokTestModules.LoSmokeUpdate import *
from ConfigFile.T03.config import *
from SmokTestModules.modules import *
from SmokTestModules.LoSmokTest_PEPWAVE import *
from email.parser import HeaderParser


PogoUpdate1('HD2_Smoke_Test_Balance.py','/QaPythonTemp/QaAutoRunTest/U64_Smoke_Test/','')

UpdateSfolder = 'QaPythonTemp/QaAutoRunTest/U64_Smoke_Test/ConfigFile/T03'
UpdateDfolder = 'ConfigFile/T03'
PogoUpdateF(UpdateSfolder,UpdateDfolder)

B20Wait = 120
script_dir = os.path.dirname(__file__)
#logging.basicConfig(level=logging.INFO)

global Mtype

def Wan_set_1(wan):
          
    link = 0

    for i in range(wan):
            link += 1
                       
            Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink='+str(link)) 
            #Bcheck('Enable')
            #SBclickT('Static IP') #選 static 
            Bclick('.conn_method_action > option:nth-child(3)') #Static IP
            #SBfillT('IP Address', '10.88.8'+str(link)+'.1','1','0','1')
            Bfill('.static_panel > tr:nth-child(2) > td:nth-child(2) > input:nth-child(1)','10.88.8'+str(link)+'.1')
            #BfillT('Default Gateway', '10.88.8'+str(link)+'.254')
            Bfill('.static_panel > tr:nth-child(4) > td:nth-child(2) > input:nth-child(1)','10.88.8'+str(link)+'.254')
            #SBfillT('DNS Server 1', '10.88.3.1')
            Bfill('div.dns_server_textbox:nth-child(5) > input:nth-child(1)','10.88.3.1')
            #SBfillT('DNS Server 2', '168.95.1.1')
            Bfill('div.dns_server_textbox:nth-child(6) > input:nth-child(1)','168.95.1.1')
            #SBfillT('IP Address List', '10.88.8'+str(link)+'.51')
            Bfill('.multiip_panel > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)','10.88.8'+str(link)+'.51')
            #BclickT('255.255.255.255','6')
            Bclick('.style_netmask > select:nth-child(2) > option:nth-child(9)')
            #SBclickTB('IP Address List')
            Bclick('.downarrowIcon')
            time.sleep(5)
            #SBclickT('Save')
            Bclick('.save_action')
    
def WAN2_Disable():

        time.sleep(2)    
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=2')
        time.sleep(2)
        Bncheck('#enable_display > td:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        SBclickT ('Save')
        time.sleep(20)
    
def UILanToPeplink(): # Pepwave 設備使用改網段 to 192.168.1.x for 6.2.1    
    IpAdd = '192.168.50.1'
    pepurl = 'http://'+IpAdd #http:// + 設備IP
    UIsLogin(pepurl) #Login
    #SWver = SWCheck()
    Bvisit (pepurl + '/cgi-bin/MANGA/index.cgi?mode=config&option=advlan')
    Bsleep(2)
    Bclick('#mainContent > div.smart_content > div.lan_network > table > tbody > tr > td.tabletitle2 > a')
    Bfill('#ui-id-3 > form > table.form_table.sep.lan_ip > tbody > tr.tablecontent2.base_subnet > td:nth-child(2) > input','192.168.1.1')
    Bfill('#ui-id-3 > form > table.form_table.dhcp_server_panel.sep > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(2) > input:nth-child(1)', '192.168.1.10')
    Bfill('#ui-id-3 > form > table.form_table.dhcp_server_panel.sep > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(2) > input:nth-child(3)', '192.168.1.250')
    BclickT ('Save')
    
    UIsApply(pepurl) #apply change
    
    
def RA1 (SN,commfile):
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

    if '.' in SN :
        rahost = SN
        raport = 2222
        rauser = 'root'
        rassh = False
    else:
        #rahost = "ra.peplink.com"
        rahost = "54.254.186.173"
        raport = 443
        rassh = True

    if commfile is 'addkeyto':
        raaddkeyto = True
        rassh = False
    else:        
        racomm = 'RA' + str(commfile) + '.csv'
        print  '\n[' + str (time.time()) + '] ' +'RA Command file: ' + racomm
        raaddkeyto = False

    global buffdata
    buffdata = ''
    k = paramiko.RSAKey.from_private_key_file(rakey,rapass)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print '\n[' + str (time.time()) + '] ' +"RA Server connecting"    
    c.connect( hostname = rahost , username = rauser , pkey = k , port=raport)
    output = "RA Host: " + rahost + '\n'
    buffdata = "".join([buffdata,output])
    print output    
    output = "RA Port: " + str(raport) + '\n'
    buffdata = "".join([buffdata,output])
    print output
    print '\n[' + str (time.time()) + '] ' +"RA Server connected"


    remote_conn = c.invoke_shell()
    output = remote_conn.recv(1000)
    info1 = '\n[' + str (time.time()) + '] ' +  'RA Receive: ' + '\n\n' + output + '\n\n'
    print info1

    
def SendMail():
    
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    import smtplib

    msg = MIMEMultipart()
    msg["Subject"] = "Smoke-Test " + HWmode + " " + FWver
    msg["From"] = "AutoQA@msa.hinet.net"
    msg["To"] = "andersonw@peplink.com"
    msg["Cc"] = ""
    body = MIMEText("Dear All \n\nSmoke-Test " + HWmode + " " + FWver+ "\n\nTest Report \nhttp://10.88.1.198:99/SmokeTestReportAuto/" + HWmode + "_TestReport_" + idt + ".html")
    msg.attach(body)

    username = 'peplink.tw'
    password = 'peplink%068'
    server = smtplib.SMTP('msr.hinet.net')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(msg["From"], msg["To"].split(",") + msg["Cc"].split(","), msg.as_string())
    server.quit()

    
def Inboun_access_HD4(DL1):
        
        #Service setting HTTP
        time.sleep(2)
        Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=inbounddistribution_b20')
        time.sleep(2)
        Bclick('.add_action')
        time.sleep(2)
        Bfill('name','HTTP')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.tablecontent2.protocol_tr > td:nth-child(2) > select.protocol_selector_action > optgroup:nth-child(2) > option:nth-child(1)')
        time.sleep(2)
        Bcheck('#inbound_conn_1_hasSelect')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bfill('#ui-id-1 > table > tr.tablecontent2.single_server_panel > td:nth-child(2) > input',DL1)
        time.sleep(2)
        BclickT ('Save')
        time.sleep(2)
        
        #Service setting SSH
        time.sleep(2)
        Bclick('.add_action')
        time.sleep(2)
        Bfill('name','SSH')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.tablecontent2.protocol_tr > td:nth-child(2) > select.protocol_selector_action > optgroup:nth-child(2) > option:nth-child(7)')
        time.sleep(2)
        Bcheck('#inbound_conn_1_hasSelect')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bfill('#ui-id-1 > table > tr.tablecontent2.single_server_panel > td:nth-child(2) > input',DL1)
        time.sleep(2)
        BclickT ('Save')
        time.sleep(2)
        
        #Service setting FTP
        time.sleep(2)
        Bclick('.add_action')
        time.sleep(2)
        Bfill('name','FTP')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.tablecontent2.protocol_tr > td:nth-child(2) > select.protocol_selector_action > optgroup:nth-child(4) > option:nth-child(5)')
        time.sleep(2)
        Bcheck('#inbound_conn_1_hasSelect')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bfill('#ui-id-1 > table > tr.tablecontent2.single_server_panel > td:nth-child(2) > input',DL1)
        time.sleep(2)
        BclickT ('Save')
        time.sleep(2)
        
        #Service setting POP3
        Bclick('.add_action')
        time.sleep(2)
        Bfill('name','POP3')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.tablecontent2.protocol_tr > td:nth-child(2) > select.protocol_selector_action > optgroup:nth-child(2) > option:nth-child(4)')
        time.sleep(2)
        Bcheck('#inbound_conn_1_hasSelect')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bfill('#ui-id-1 > table > tr.tablecontent2.single_server_panel > td:nth-child(2) > input',DL1)
        time.sleep(2)
        BclickT ('Save')
        time.sleep(2)
        
        #Service setting SMTP
        time.sleep(2)
        Bclick('.add_action')
        time.sleep(2)
        Bfill('name','SMTP')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.tablecontent2.protocol_tr > td:nth-child(2) > select.protocol_selector_action > optgroup:nth-child(2) > option:nth-child(6)')
        time.sleep(2)
        Bcheck('#inbound_conn_1_hasSelect')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bfill('#ui-id-1 > table > tr.tablecontent2.single_server_panel > td:nth-child(2) > input',DL1)
        time.sleep(2)
        BclickT ('Save')
        time.sleep(2)
        
        #Service setting ICMP
        time.sleep(2)
        Bclick('.add_action')
        time.sleep(2)
        Bfill('name','ICMP')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.tablecontent2.protocol_tr > td:nth-child(2) > select.protocol_selector_action > optgroup:nth-child(3) > option:nth-child(3)')
        time.sleep(2)
        Bcheck('#inbound_conn_1_hasSelect')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bfill('#ui-id-1 > table > tr.tablecontent2.single_server_panel > td:nth-child(2) > input',DL1)
        time.sleep(2)
        BclickT ('Save')
        time.sleep(2)
        
        #Service setting UDP
        time.sleep(2)
        Bclick('.add_action')
        time.sleep(2)
        Bfill('name','UDP')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.tablecontent2.protocol_tr > td:nth-child(2) > select.protocol_action > option:nth-child(2)')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr:nth-child(5) > td:nth-child(2) > div > select > option:nth-child(1)')
        time.sleep(2)
        Bcheck('#inbound_conn_1_hasSelect')
        time.sleep(2)
        Bcheck('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bcheck('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bfill('#ui-id-1 > table > tr.tablecontent2.single_server_panel > td:nth-child(2) > input',DL1)
        time.sleep(2)
        BclickT ('Save')
        time.sleep(2)

def HD2_Wan_set_1(wan):


        link = 0
        for i in range(wan):

                link += 1
                e = i + 2
                #Bclick("li.pt__item:nth-child("+str(e)+") > div:nth-child(1) > span:nth-child(3) > span:nth-child(2) > button:nth-child(2)")
                Bclick("li.pt__item:nth-child("+str(e)+") > div:nth-child(1) > span:nth-child(3) > span:nth-child(2) > button:nth-child(1)")
                #li.pt__item:nth-child(3) > div:nth-child(1) > span:nth-child(3) > span:nth-child(2) > button:nth-child(1)
                Bsleep(5)
                SBclickT('Static IP')
                #SBfillT('IP Address', '10.88.8'+str(link)+'.1','1','9','1')
                Bfill('form.ethernet_settings:nth-child(2) > table:nth-child(7) > tbody:nth-child(6) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)','10.88.8'+str(link)+'.1')
                #SBfillT('Default Gateway', '10.88.8'+str(link)+'.254','1','6','1')
                Bfill('form.ethernet_settings:nth-child(2) > table:nth-child(7) > tbody:nth-child(6) > tr:nth-child(3) > td:nth-child(2) > input:nth-child(1)','10.88.8'+str(link)+'.254')
                SBfillT('DNS Server 1', '10.88.3.1')
                SBfillT('DNS Server 2', '168.95.1.1')
                #SBfillT('Additional Public IP Address', '10.88.8'+str(link)+'.51','2')
                Bfill('form.ethernet_settings:nth-child(2) > table:nth-child(11) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)','10.88.8'+str(link)+'.51')
                #SBclickT('255.255.255.255','9')
                Bclick('form.ethernet_settings:nth-child(2) > table:nth-child(11) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > select:nth-child(3) > option:nth-child(9)')
                #SBclickTB('Additional Public IP Address')
                Bclick('form.ethernet_settings:nth-child(2) > table:nth-child(11) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > button:nth-child(1)')
                Bsleep(7)
                SBclickT('Save and Apply')
                #Bclick('div.ui-dialog:nth-child(11) > div:nth-child(3) > div:nth-child(1) > button:nth-child(1)')
                Bsleep(10)

                if wan == 1 :
                        try:
                                Bsleep(5)
                                Bdrop_offset('li.pt__item:nth-child(3) > div:nth-child(1) > div:nth-child(4)',0,170)

                        except:
                                print e

def Config_File_Upload(FileName):
    
    #print 'Start Config file upload....'
    IpAdd = '192.168.50.1'
    pepurl = 'http://'+IpAdd #http:// + 設備IP
    FilePath = '/home/peplink/QA/QaPythonTemp/QaAutoRunTest/U64_Smoke_Test/ConfigFile/T03/'
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
    Bsleep(7)
    UIsApply(pepurl)
    Bsleep(3)
    Bquit()

def Di_Config_File_Upload(FileName):
    
    #print 'Start Config file upload....'
    IpAdd = '10.88.81.1'
    pepurl = 'http://'+IpAdd #http:// + 設備IP
    FilePath = '/home/peplink/QA/QaPythonTemp/QaAutoRunTest/U64_Smoke_Test/ConfigFile/T03/'
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
    Bsleep(7)
    UIsApply(pepurl)
    Bsleep(3)
    Bquit()
    

class SmokeTest (unittest.TestCase):

    @classmethod

    def setUp(self):
        "Setup the test case"
        global count
        count = 0
        time.sleep(5)


    def test_case001(self):

        "Case_1037 WAI access via WAN side with NAT-Mappings enabled"
        try:
            Config_File_Upload('hd2hw4_720_test_case001.conf')
            time.sleep(30)
            os.system('nmcli device connect ens19') 
            time.sleep(8)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.50.50/24') 
            time.sleep(10)
            os.system('nmcli connection up "static-ens18"')
            time.sleep(10)
            driver = Bopen()
            Bvisit('http://10.88.81.1/')
            Bwait_text('Login')
            Bsleep(3)
            Bfill('username', 'admin')
            Bsleep(1)
            Bfill('password', 'admin')
            Bsleep(1)
            BclickTB('Login')
            Bsleep(8)
            result = re.findall(r'Connected',driver.page_source)
            if result[0] == 'Connected':
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                print ("PASS")
                Bsleep(10)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(5)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(10)
                
            else:

                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
               
            except:
                a=0

            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(8)
            os.system('nmcli connection up "dhcp-ens18"')
            time.sleep(10)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(5)

            if count <3:
                count+=1
                self.test_case001()

            else:
                self.assertEqual(1,0)

    def test_case002(self):

        "Case_1374 - WAI-Read Only user support"

        try:
            Config_File_Upload('hd2hw4_720_test_case002.conf')
            time.sleep(30)
            driver = Bopen()
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi')
            Bwait_text('Login')
            Bfill('username', 'peplink')
            Bsleep(1)
            Bfill('password', '0912#$%^')
            Bsleep(1)
            BclickTB('Login')
            Bsleep(5)

            result = re.findall(r'You logged in as a read-only user',driver.page_source)

            if result[0] == 'You logged in as a read-only user':

                print ("PASS")
                ssh.close()
                Bquit()
                time.sleep(3)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')


            else:

                ssh.close()
                Bquit()
                self.assertEqual(1,0)
        except:

            global count
            try:
                Bquit()

            except:
                a=0
            ssh.close()
            time.sleep(3)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')


            if count <3:
                count+=1
                self.test_case002()

            else:
                self.assertEqual(1,0)

    def test_case003(self):

        "Case_1041 WAI access from selected WAN interface(s)"
        
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case003.conf')
            Bsleep(30)
            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.50.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"')
            Bsleep(15)
            driver = Bopen()
            Bvisit('http://10.88.81.1/cgi-bin/MANGA/index.cgi')
            Bwait_text('Login')
            Bfill('username', 'admin')
            Bsleep(1)
            Bfill('password', 'admin')
            Bsleep(1)
            BclickTB('Login')
            Bsleep(5)

            result1 = re.findall(r'Connected',driver.page_source)

            if result1[0] == 'Connected':

                a += 1
                Bquit()
                
            driver = Bopen()
            Bvisit('http://10.88.81.51/cgi-bin/MANGA/index.cgi')
            Bwait_text('Login')
            Bfill('username','admin')
            Bsleep(1)
            Bfill('password','admin')
            Bsleep(1)
            BclickTB('Login')
            Bsleep(5)

            result2 = re.findall(r'Connected',driver.page_source)

            if result2[0] == 'Connected':

                a += 1
                Bquit()

            driver = Bopen()
            Bvisit('http://10.88.82.1/cgi-bin/MANGA/index.cgi')
            Bwait_text('Login')
            Bfill('username', 'admin')
            Bsleep(1)        
            Bfill('password', 'admin')
            Bsleep(1)
            BclickTB('Login')
            Bsleep(5)

            result3 = re.findall(r'Connected',driver.page_source)

            if result3[0] == 'Connected':

                a += 1
                Bquit()

            driver = Bopen()
            Bvisit('http://10.88.82.51/cgi-bin/MANGA/index.cgi')
            Bwait_text('Login')
            Bfill('username', 'admin')
            Bsleep(1)        
            Bfill('password', 'admin')
            Bsleep(1)
            BclickTB('Login')
            Bsleep(5)

            result4 = re.findall(r'Connected',driver.page_source)

            if result4[0] == 'Connected':

                a += 1
                Bquit()

            print a

            if a == 4:

                print ("PASS")
                time.sleep(3)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')


            else:
                
                Bquit()
                #UIRestD()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            #UIRestD()
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 

            if count <3:
                count+=1
                self.test_case003()

            else:
                self.assertEqual(1,0)

    def test_case004(self):

        "Case_1048-Throughput test with VLAN Tagging enable"
        global qos        
        a = 0

        try:
            Config_File_Upload('hd2hw4_720_test_case004.conf')
            Bsleep(20)
            os.system('nmcli device connect ens19') 
            time.sleep(6)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.50.50/24') 
            time.sleep(6)
            os.system('nmcli connection up "static-ens18"') 
            
            time.sleep(10)
            tn = telnetlib.Telnet(HOST)
            Bsleep(6)
            tn.read_until("User:")
            Bsleep(6)
            tn.write("admin\r\n")
            Bsleep(6)
            tn.read_until("Password:")
            Bsleep(6)
            tn.write ('\r\n')
            Bsleep(6)
            tn.write("enable\r\n")
            Bsleep(6)        
            tn.write("config\r\n")
            Bsleep(6)
            tn.write("interface 0/"+PORT+"\r\n")
            Bsleep(6)
            tn.write("vlan tag "+VID+"\r\n")
            Bsleep(6)
            tn.write("no vlan pvid\r\n")
            Bsleep(6)
            tn.write("exit\r\n")
            print "port assign tag "+VID
            Bsleep(6)
            tn.close

            Bsleep(20)

            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(6)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            time.sleep(6)
            result1 = []
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(6)
            cmd = "echo peplink | sudo -S iperf -c 10.88.80.11 -t60 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(6)
            for std in stdout.readlines():
                result1.append(std)

            c = re.findall(r'MBytes(.*?)Mbits/sec',str(result1))
            print " Result = "
            print (c[-1])
            
            if float(c[-1]) > 1 and float(c[-1]) < 45:

                a += 1
                ssh.close()

            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(6)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            time.sleep(6)
            result2 = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(6)
            cmd = "echo peplink | sudo -S iperf -c 10.88.81.1 -t60 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(6)
            for std in stdout.readlines():
                result2.append(std)

            s = re.findall(r'MBytes(.*?)Mbits/sec',str(result2))
            print "Result = "
            print (s[-1])

            if float(s[-1]) > 1 and float(s[-1]) < 45:
                print (s[-1])
                a += 1
                ssh.close()

            if a == 2:

                Bquit()
                time.sleep(10)
                tn = telnetlib.Telnet(HOST)
                time.sleep(6)        
                tn.read_until("User:")
                time.sleep(6)
                tn.write("admin\r\n")
                time.sleep(6)
                tn.read_until("Password:")
                time.sleep(6)
                tn.write ('\r\n')
                time.sleep(6)
                tn.write("enable\r\n")
                time.sleep(6)
                tn.write("config\r\n")
                time.sleep(6)
                tn.write("interface 0/"+PORT+"\r\n")
                time.sleep(6)
                tn.write("vlan pvid "+VID+"\r\n")
                time.sleep(6)
                tn.write("no vlan tag "+VID+"\r\n")
                time.sleep(6)
                tn.write("exit\r\n")
                print "port assign untag "+VID
                time.sleep(6)
                tn.close
                time.sleep(20)
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(6)
                os.system('nmcli connection up "dhcp-ens18"')  
                time.sleep(6)
                os.system('nmcli device disconnect ens18')
                time.sleep(6)
                os.system('nmcli device connect ens18')
                time.sleep(8)   

            else:

                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                               
            except:
                a=0
            time.sleep(10)
            tn = telnetlib.Telnet(HOST)
            time.sleep(6)        
            tn.read_until("User:")
            time.sleep(6)
            tn.write("admin\r\n")
            time.sleep(6)
            tn.read_until("Password:")
            time.sleep(6)
            tn.write ('\r\n')
            time.sleep(6)
            tn.write("enable\r\n")
            time.sleep(6)
            tn.write("config\r\n")
            time.sleep(6)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(6)
            tn.write("vlan pvid "+VID+"\r\n")
            time.sleep(6)
            tn.write("no vlan tag "+VID+"\r\n")
            time.sleep(6)
            tn.write("exit\r\n")
            print "port assign untag "+VID
            time.sleep(6)
            tn.close
            time.sleep(6)
            os.system('nmcli device disconnect ens19') 
            time.sleep(6)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(6)
            os.system('nmcli connection up "dhcp-ens18"')  
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(6)
            os.system('nmcli device connect ens18')
            time.sleep(8)   

            if count <6:
                count+=1
                self.test_case004()

            else:
                self.assertEqual(1,0)

    def test_case005(self):

        "Case_1047- WAN interface with VLAN tagging and Static connection enabled"

        try:
            Config_File_Upload('hd2hw4_720_test_case005.conf')
            Bsleep(30)
            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.50.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"') 

            tn = telnetlib.Telnet(HOST)
            time.sleep(2)
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)        
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan tag "+VID+"\r\n")
            time.sleep(2)
            tn.write("no vlan pvid\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            print "port assign tag "+VID
            time.sleep(2)
            tn.close
            Bsleep(5)
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.80.11')
            t = stdout.read()
            print('t',str(t))
            ssh.close()
            
            if '4 received' in str(t):

                print ("PASS")

                time.sleep(10)
                tn = telnetlib.Telnet(HOST)
                time.sleep(2)        
                tn.read_until("User:")
                time.sleep(2)
                tn.write("admin\r\n")
                time.sleep(2)
                tn.read_until("Password:")
                time.sleep(2)
                tn.write ('\r\n')
                time.sleep(2)
                tn.write("enable\r\n")
                time.sleep(2)
                tn.write("config\r\n")
                time.sleep(2)
                tn.write("interface 0/"+PORT+"\r\n")
                time.sleep(2)
                tn.write("vlan pvid "+VID+"\r\n")
                time.sleep(2)
                tn.write("no vlan tag "+VID+"\r\n")
                time.sleep(2)
                tn.write("exit\r\n")
                print "port assign untag "+VID
                time.sleep(2)
                tn.close
                time.sleep(2)
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')  
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')  
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                
            else:
                
                self.assertEqual(1,0)

        except:
             
            global count
            try:
                Bquit()
                
            except:
                a=0
            time.sleep(10)
            tn = telnetlib.Telnet(HOST)
            time.sleep(2)        
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan pvid "+VID+"\r\n")
            time.sleep(2)
            tn.write("no vlan tag "+VID+"\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            print "port assign untag "+VID
            time.sleep(2)
            tn.close
            time.sleep(2)
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')  
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')  
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case005()

            else:
                self.assertEqual(1,0)

    def test_case006(self):

        "Case_1046- WAN interface with VLAN tagging and PPPoE enabled"

        try:
            Config_File_Upload('hd2hw4_720_test_case006.conf')
            time.sleep(30)
            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.50.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"') 
            Bsleep(5)

            tn = telnetlib.Telnet(HOST)
            time.sleep(2)
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)        
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan tag "+VID+"\r\n")
            time.sleep(2)
            tn.write("no vlan pvid\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            print "port assign tag "+VID
            time.sleep(2)
            tn.close
            Bsleep(5)
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.80.11')
            t = stdout.read()
            print('t',str(t))
            ssh.close()
          
            if '4 received' in str(t):

                print ("PASS")

                time.sleep(10)
                tn = telnetlib.Telnet(HOST)
                time.sleep(2)        
                tn.read_until("User:")
                time.sleep(2)
                tn.write("admin\r\n")
                time.sleep(2)
                tn.read_until("Password:")
                time.sleep(2)
                tn.write ('\r\n')
                time.sleep(2)
                tn.write("enable\r\n")
                time.sleep(2)
                tn.write("config\r\n")
                time.sleep(2)
                tn.write("interface 0/"+PORT+"\r\n")
                time.sleep(2)
                tn.write("vlan pvid "+VID+"\r\n")
                time.sleep(2)
                tn.write("no vlan tag "+VID+"\r\n")
                time.sleep(2)
                tn.write("exit\r\n")
                print "port assign untag "+VID
                time.sleep(2)
                tn.close
                time.sleep(2)
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')  
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')  
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
            else:
                
                self.assertEqual(1,0)

        except:
                     
            global count
            try:
                Bquit()

            except:
                a=0
            time.sleep(10)
            tn = telnetlib.Telnet(HOST)
            time.sleep(2)        
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan pvid "+VID+"\r\n")
            time.sleep(2)
            tn.write("no vlan tag "+VID+"\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            print "port assign untag "+VID
            time.sleep(2)
            tn.close
            time.sleep(2)
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')  
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')  
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   
            if count <3:
                count+=1
                self.test_case006()

            else:
                self.assertEqual(1,0)

    def test_case007(self):

        "Case_1045- WAN interface with VLAN tagging and DHCP enabled"

        try:
            Config_File_Upload('hd2hw4_720_test_case007.conf')
            time.sleep(30)
            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.50.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"') 

            tn = telnetlib.Telnet(HOST)
            time.sleep(2)
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)        
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan tag "+VID+"\r\n")
            time.sleep(2)
            tn.write("no vlan pvid\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            print "port assign tag "+VID
            time.sleep(2)
            tn.close
            Bsleep(5)
            
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.80.11')
            t = stdout.read()
            print('t',str(t))
            ssh.close()
            
            if '4 received' in str(t):

                print ("PASS")

                time.sleep(10)
                tn = telnetlib.Telnet(HOST)
                time.sleep(2)        
                tn.read_until("User:")
                time.sleep(2)
                tn.write("admin\r\n")
                time.sleep(2)
                tn.read_until("Password:")
                time.sleep(2)
                tn.write ('\r\n')
                time.sleep(2)
                tn.write("enable\r\n")
                time.sleep(2)
                tn.write("config\r\n")
                time.sleep(2)
                tn.write("interface 0/"+PORT+"\r\n")
                time.sleep(2)
                tn.write("vlan pvid "+VID+"\r\n")
                time.sleep(2)
                tn.write("no vlan tag "+VID+"\r\n")
                time.sleep(2)
                tn.write("exit\r\n")
                print "port assign untag "+VID
                time.sleep(2)
                tn.close
                time.sleep(2)
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')  
                
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')  
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
            else:

                self.assertEqual(1,0)

        except:
                     
            global count
            try:
                Bquit()

            except:
                a=0
            time.sleep(10)
            tn = telnetlib.Telnet(HOST)
            time.sleep(2)
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan pvid "+VID+"\r\n")
            time.sleep(2)
            tn.write("no vlan tag "+VID+"\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            print "port assign untag "+VID
            time.sleep(2)
            tn.close
            time.sleep(2)
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')  
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')  
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   

            if count <3:
                count+=1
                self.test_case007()

            else:
                self.assertEqual(1,0)


    def test_case008(self):

        "Case_1069 Static connection MTU, MSS modify manually"
        try:
            Config_File_Upload('hd2hw4_720_test_case008.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens19')
            time.sleep(30)

            MTU = 500

            try:
                while True:

                    runtest = subprocess.check_output('ping -M do -s '+ str(MTU) +' -c 1 10.88.81.254', shell = True)
                    print str(runtest)
                    Bsleep(1)
                    if 'ms' in str(runtest):
                        MTU += 1

            except:

                print MTU
                if MTU + 27 == 1300:

                        #UIRestD()
                        #time.sleep(32)
                        Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                        os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                        time.sleep(2)
                        os.system('nmcli connection up "dhcp-ens18"')  
                        os.system('nmcli device disconnect ens18')
                        time.sleep(2)
                        os.system('nmcli device connect ens18')
                        time.sleep(5)   
                        print (str(MTU + 27))
                        self.assertEqual(1,1)

                else:

                        #UIRestD()
                        #time.sleep(32)
                        Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                        os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                        time.sleep(2)
                        os.system('nmcli connection up "dhcp-ens18"')  
                        os.system('nmcli device disconnect ens18')
                        time.sleep(2)
                        os.system('nmcli device connect ens18')
                        time.sleep(5)   
                        print (str(MTU + 27))
                        self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')  
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   

            if count <3:
                count+=1
                self.test_case008()

            else:
                self.assertEqual(1,0)


    def test_case009(self):

        "Case_1070 Default connection MTU, Mss value"

        try:
            Config_File_Upload('hd2hw4_720_test_case009.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)

            MTU = 500
            time.sleep(10)
            try:
                while True:

                    runtest = subprocess.check_output('ping -M do -s '+ str(MTU) +' -c 1 10.88.81.254', shell = True)
                    print str(runtest)

                    if 'ms' in str(runtest):
                        MTU += 1
            except:

                print MTU
                if MTU + 27 == 1440:

                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                    time.sleep(2)
                    os.system('nmcli connection up "dhcp-ens18"')  
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)   
                    print (str(MTU + 27))
                    self.assertEqual(1,1)

                else:

                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                    time.sleep(2)
                    os.system('nmcli connection up "dhcp-ens18"')  
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)   
                    print (str(MTU + 27))
                    self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')  
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   

            if count <3:
                count+=1
                self.test_case009()

            else:
                self.assertEqual(1,0)
    
    def test_case010(self):

        "Case_1071 PPPoE connection MTU, MSS modify manually"
        try:
            Config_File_Upload('hd2hw4_720_test_case010.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens19')
            time.sleep(30)
            MTU = 500

            try:
                while True:
                    
                    runtest = subprocess.check_output('ping -M do -s '+ str(MTU) +' -c 1 10.88.81.254', shell = True)
                    print str(runtest)
                    Bsleep(1)
                    if 'ms' in str(runtest):
                        MTU += 1
                        
            except:

                print MTU
                if MTU + 27 == 1200:
                    print 'PASS'
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                    time.sleep(2)
                    os.system('nmcli connection up "dhcp-ens18"')  
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)

                    print (str(MTU + 27))
                    self.assertEqual(1,1)


                else:

                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                    time.sleep(2)
                    os.system('nmcli connection up "dhcp-ens18"')  
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(8)

                    print (str(MTU + 27))
                    self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')  
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)

            if count <3:
                count+=1
                self.test_case010()

            else:
                self.assertEqual(1,0)

                
                
    def test_case011(self):

        "Case_1190- Reply ICMP Ping Requests Disable / Enable"
        
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case011-1.conf')
            Bsleep(30)
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.81.1')
            t1 = stdout.read()
            print('t1',str(t1))
            if '0 received' in str(t1):

                a += 1
                Bsleep(3)
            else:
                
                Bquit()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(5)

                self.assertEqual(1,0)

            Config_File_Upload('hd2hw4_720_test_case011-2.conf')
            Bsleep(30)
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.81.1')
            t2 = stdout.read()
            print('t2',str(t2))
            if '4 received' in str(t2):

                a += 1
                Bsleep(3)
                
            if a == 2:
                
                print ("PASS")
                Bquit()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            else:
                
                Bquit()
                print (a)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')

                self.assertEqual(1,0)

        except:
                 
            global count
            try:
                Bquit()

            except:
                a=0

            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            time.sleep(30)
            if count <3:
                count+=1
                self.test_case011()

            else:
                self.assertEqual(1,0)


    def test_case012(self):

        "Case_1234 WAN Backup w/o Priority"
        try:
            Config_File_Upload('hd2hw4_720_test_case012.conf')
            Bsleep(30)
            driver = Bopen()
            UIsLogin(pepurl)
            time.sleep(AppWait)
            result1 = driver.page_source
            WAN_Status = re.findall(r'Connected',result1)
            #WAN1_Status = re.findall(r'<span id="conn_status_msg_1" style="padding: 0px 5px;">(.*?)</span>',result1)
            #WAN2_Status = re.findall(r'<span id="conn_status_msg_2" style="padding: 0px 5px;">(.*?)</span>',result1)
            print 'WAN_Status[0]=',WAN_Status[0]
            print 'WAN_Status[1]=',WAN_Status[1]
            
            if WAN_Status[0] == 'Connected' and WAN_Status[1] == 'Connected':

                Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
                time.sleep(2)
                SBclickT('Backup')
                SBclickT('Save')
                UIsApply(pepurl)
                time.sleep(AppWait)
                Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=main')
                result2 = driver.page_source
                WAN1_Status = re.findall(r'Standby',result2)
                WAN2_Status = re.findall(r'Connected',result2)
                #WAN1_Status = re.findall(r'<span id="conn_status_msg_1" style="padding: 0px 5px;">(.*?)</span>',result2)
                #WAN2_Status = re.findall(r'<span id="conn_status_msg_2" style="padding: 0px 5px;">(.*?)</span>',result2)
                print 'WAN1_Status[0]=',WAN1_Status[0]
                print 'WAN2_Status[0]=',WAN2_Status[0]
                if WAN1_Status[0] == 'Standby' and WAN2_Status[0] == 'Connected':
                    print 'pass'
                    
                    Bquit()
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                else:
                    Bquit()
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    
                    self.assertEqual(1,0)
            else:
                Bquit()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                
                self.assertEqual(1,0)
        
        except:

            global count
            try:
                Bquit()

            except:
                a=0
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            
            if count <3:
                count+=1
                self.test_case012()

            else:
                self.assertEqual(1,0)
                      
    def test_case013(self):

        "Case_1235 WAN Backup with Priority"
        try:
            Config_File_Upload('hd2hw4_720_test_case013-1.conf')
            Bsleep(30)
            driver = Bopen()
            UIsLogin(pepurl)
            time.sleep(AppWait)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=main')
            result1 = driver.page_source
            WAN1_Status = re.findall(r'Standby',result1)
            WAN2_Status = re.findall(r'Connected',result1)
            Bsleep(5)
            Bquit()
            if WAN1_Status[0] == 'Standby' and WAN2_Status[0] == 'Connected':

                #Bclick('#conn_button_disconnect_2')
                #SBclickT('OK')
                Config_File_Upload('hd2hw4_720_test_case013-2.conf')
                Bsleep(3)
                driver = Bopen()
                UIsLogin(pepurl)
                time.sleep(AppWait)
                Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=main')
                time.sleep(AppWait)
                result2 = driver.page_source
                WAN1_Status = re.findall(r'Connected',result2)
                WAN2_Status = re.findall(r'Disable',result2)
                Bsleep(5)
                
                if WAN1_Status[0] == 'Connected' and WAN2_Status[0] == 'Disable':
                    print 'pass'

                    Bquit()
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                else:
                
                    Bquit()
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')

                    self.assertEqual(1,0)
            else:

                Bquit()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                self.assertEqual(1,0)
        except:

            global count
            try:
                Bquit()

            except:
                a=0
                
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            time.sleep(30)  
            if count <3:
                count+=1
                self.test_case013()

            else:
                self.assertEqual(1,0)
                      

    def test_case014(self):

        "Case_1050 - Active Session"
        try:

            Config_File_Upload('hd2hw4_720_test_case014.conf')
            time.sleep(30)
            driver = Bopen()
            UIsLogin(pepurl)
            time.sleep(3)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=sessionv3')
            result1 = re.findall(r'<tr class="tablecontent2 zb2">(.*?)</tr>',driver.page_source)
            Total_Sessions1 = re.findall(r'<td>(.*?)</td>',str(result1))

            ssh.connect('192.168.50.9' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            #print 'Log folder Clear!!'
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            #print 'Python Task Clear!!'
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 80 &> log/T80.tmp&')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 21 &> log/T21.tmp&')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 110 &> log/T110.tmp&')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 25 &> log/T25.tmp&')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 U 666 &> log/U666.tmp&')
            time.sleep(2)
            
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            #print 'Log folder Clear!!'
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            #print 'Python Task Clear!!'
            time.sleep(2)
            #print 'Test Running Wait...' 
            stdin, stdout, stderr = ssh.exec_command("echo peplink | sudo -S python PogoU64.py W1 10.88.81.1 60")
            time.sleep(2)
            
            for std in stdout.readlines():
                print std

            time.sleep(5)
            SBclickT('Refresh')
            time.sleep(5)
            result2 = re.findall(r'<tr class="tablecontent2 zb2">(.*?)</tr>',driver.page_source)
            Total_Sessions2 = re.findall(r'<td>(.*?)</td>',str(result2))
            Bquit()

            if int(Total_Sessions1[-1]) < int(Total_Sessions2[-1]):

                print ("PASS")
                time.sleep(3)
                Bquit()
                #UIRestD()
                Bsleep(3)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')

            else:

                ssh.close()
                Bquit()
                #UIRestD()
                Bsleep(3)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(5)
                
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            ssh.close()
            #UIRestD()
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')

            if count <3:
                count+=1
                self.test_case014()

            else:
                self.assertEqual(1,0)


    
    def test_case015(self):
        "Case_1297-SNMP v1 v2"
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case015.conf')
            Bsleep(30)
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "snmpwalk -v 1 -c public 192.168.50.1"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(3)
            r1 = stdout.read()
            print (r1)
            
            if 'support@peplink.com' in str(r1):

                a += 1
                
            else:
                
                Bquit()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                
                self.assertEqual(1,0)

            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "snmpwalk -v 2c -c public 192.168.50.1"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(3)
            r2 = stdout.read()
            print (r2)

            if 'support@peplink.com' in str(r2):

               a += 1
                    
            else:
                
                Bquit()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                
                self.assertEqual(1,0)


            if a == 2:
            
                Result = "pass"
                print ("PASS")
                Bquit()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0

            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            
            if count <3:
                count+=1
                self.test_case015()

            else:
                self.assertEqual(1,0)


    def test_case016(self):
        "Case_1298-SNMP Peplink Info"
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case016.conf')
            time.sleep(30)
            
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "snmpwalk -v 1 -c public 192.168.50.1"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(3)
            r1 = stdout.read()
            print (r1)
            
            if 'Peplink' or 'Pepwave' in str(r):

                print ("PASS")

                time.sleep(10)
                Bquit()
                #UIRestD()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                
                self.assertEqual(1,1)
                    
            else:
                
                Bquit()
                #UIRestD()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                
                self.assertEqual(1,0)


        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            #UIRestD()
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            

            if count <3:
                count+=1
                self.test_case016()

            else:
                self.assertEqual(1,0)


    def test_case017(self):

        "Case_1300-SNMP v3 MD5"
        a = 0        
        try:

            Config_File_Upload('hd2hw4_720_test_case017.conf')
            Bsleep(30)
            
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = 'snmpwalk -v 3 -u md5 -a MD5 -A peplink5978 -l authNoPriv 192.168.50.1'
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(3)
            r = stdout.read()
            print (r)
            
            if 'support@peplink.com' in str(r):

                print ("PASS")
                Bquit()
                #UIRestD()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                ssh.close()
                self.assertEqual(1,1)
                    
            else:
                
                Bquit()
                #UIRestD()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                ssh.close()
                self.assertEqual(1,0)


        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            if count <3:
                count+=1
                self.test_case017()

            else:
                self.assertEqual(1,0)


    def test_case018(self):

        "Case_1301-SNMP v3 SHA"
        a = 0        
        try:

            Config_File_Upload('hd2hw4_720_test_case018.conf')
            time.sleep(30)
            
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = 'snmpwalk -v 3 -u sha -a SHA -A peplink5978 -l authNoPriv 192.168.50.1'
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(3)
            r = stdout.read()
            print (r)
            
            if 'support@peplink.com' in str(r):

                print ("PASS")
                Bquit()
                #UIRestD()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                
                ssh.close()
                self.assertEqual(1,1)
                    
            else:
                
                Bquit()
                #UIRestD()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                ssh.close()
                self.assertEqual(1,0)


        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            #UIRestD()
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            if count <3:
                count+=1
                self.test_case018()

            else:
                self.assertEqual(1,0)


    def test_case019(self):

        "Case_1974 SNMP - SNMP trap"

        try:
            a = 0
            Config_File_Upload('hd2hw4_720_test_case019.conf')
            time.sleep(30)

            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(6)
            ssh.exec_command("echo peplink | sudo -S snmptrapd -m all -Lf /tmp/traptest -d")
            time.sleep(6)
            ssh.close()
            time.sleep(30)
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
            time.sleep(6)
            Bncheck('#enable_display > td:nth-child(2) > input:nth-child(1)')
            time.sleep(6)
            Bclick('.save_action')
            time.sleep(6)
            UIsApply(pepurl)
            time.sleep(30)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
            time.sleep(6)
            Bcheck('#enable_display > td:nth-child(2) > input:nth-child(1)')
            time.sleep(6)
            Bclick('.save_action')
            time.sleep(6)
            UIsApply(pepurl)
            time.sleep(30)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=2')
            time.sleep(6)
            Bncheck('#enable_display > td:nth-child(2) > input:nth-child(1)')
            time.sleep(6)
            Bclick('.save_action')
            time.sleep(6)
            UIsApply(pepurl)
            time.sleep(30)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=2')
            time.sleep(6)
            Bcheck('#enable_display > td:nth-child(2) > input:nth-child(1)')
            time.sleep(6)
            Bclick('.save_action')
            time.sleep(6)
            UIsApply(pepurl)
            time.sleep(30)
            Bquit()
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(6)
            stdin, stdout, stderr = ssh.exec_command("cat /tmp/traptest |grep onn")
            time.sleep(6)
            ssh.exec_command("echo peplink | sudo -S killall snmptrapd")
            time.sleep(6)
            ssh.exec_command("echo peplink | sudo -S rm /tmp/traptest")
            time.sleep(6)
            ssh.close()

            result = []
            for std in stdout.readlines():
                result.append(std)
                print 'result = ',result


            if 'onnected0' in str(result):
                a += 1
                print 'a = ',a

            if 'nnected0' in str(result):
                a += 1
                print 'a = ',a

            if a == 2:

                print 'pass'
                #UIRestD()
                Bsleep(3)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
            else:
                print 'fail'
                #UIRestD()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                self.assertEqual(1,0)


        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            Bsleep(3)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            if count <3:
                count+=1
                self.test_case019()

            else:
                self.assertEqual(1,0)

    


    def test_case020(self):

        "Case_1051 Customer DHCP Server Lease Time, IP Range, DHCP Client List, Subnet Mask"

        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case020.conf')
            time.sleep(30)
            
            os.system('nmcli device disconnect ens18')
            time.sleep(5)
            os.system('nmcli device connect ens18')
            time.sleep(20)

            r = os.popen('nmcli device show |grep IP4').read()
            print r

            if '192.168.1.200/24' in str(r):

                print ("PASS")
                ssh.close()
                Bsleep(3)
                #UIRestD()
                IpAdd = '192.168.1.1'
                pepurl = 'http://'+IpAdd #http:// + 設備IP
                FilePath = '/home/peplink/QA/QaPythonTemp/QaAutoRunTest/U64_Smoke_Test/ConfigFile/T03/'
                FileName = 'hd2hw4_720_FactoryReset.conf'
                ConfigFile = FilePath + FileName
                driver = Bopen()
                UIsLogin(pepurl)
                Bsleep(2)
                Bvisit(pepurl + '/cgi-bin/MANGA/index.cgi?mode=config&option=utconfig')
                Bsleep(2)
                BfillT('Configuration File',ConfigFile)
                Bsleep(6)
                #BclickT ('Upload')
                Bclick('#config_panel > form:nth-child(7) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > button:nth-child(1)')

                Bsleep(7)
                UIsApply(pepurl)
                Bsleep(9)
                Bquit()
                Bsleep(20)
                os.system('nmcli device disconnect ens18')
                time.sleep(6)
                os.system('nmcli device connect ens18')
                time.sleep(8)
            else:

                ssh.close()
                Bquit()
                self.assertEqual(1,0)

        except:

            global count
            
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            IpAdd = '192.168.1.1'
            pepurl = 'http://'+IpAdd #http:// + 設備IP
            FilePath = '/home/peplink/QA/QaPythonTemp/QaAutoRunTest/U64_Smoke_Test/ConfigFile/T03/'
            FileName = 'hd2hw4_720_FactoryReset.conf'
            ConfigFile = FilePath + FileName
            driver = Bopen()
            UIsLogin(pepurl)
            Bsleep(2)
            Bvisit(pepurl + '/cgi-bin/MANGA/index.cgi?mode=config&option=utconfig')
            Bsleep(2)
            BfillT('Configuration File',ConfigFile)
            Bsleep(6)
            #BclickT ('Upload')
            Bclick('#config_panel > form:nth-child(7) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > button:nth-child(1)')

            Bsleep(7)
            UIsApply(pepurl)
            Bsleep(9)
            Bquit()
            
            Bsleep(20)
            os.system('nmcli device disconnect ens18')
            time.sleep(6)
            os.system('nmcli device connect ens18')
            time.sleep(20)
            
            if count <3:
                count+=1
                self.test_case020()

            else:
                self.assertEqual(1,0)

                
                
                
    def test_case021(self):

        "Case_1052 Assign Custom DNS Servers"
        
        a = 0
        try:

            Config_File_Upload('hd2hw4_720_test_case021.conf')
            time.sleep(30)

            os.system('nmcli device disconnect ens18')
            time.sleep(5)
            os.system('nmcli device connect ens18')
            time.sleep(5)

            r = os.popen('nmcli device show |grep DNS').read()
            print r
               
            if '1.1.1.1' in str(r):
                
                a += 1
            
            if '2.2.2.2' in str(r):
                
                a += 1
               
            if a == 2:

                print ("PASS")
                ssh.close()
                Bquit()
                #UIRestD()

                time.sleep(3)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                
            else:

                ssh.close()
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                
                self.assertEqual(1,0)

        except:
         
            global count
            try:
                Bquit()
                
            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            time.sleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case021()

            else:
                self.assertEqual(1,0)



    def test_case022(self):

        "Case_1053 DHCP Reservation"
        
        a = 0        
        try:

            Config_File_Upload('hd2hw4_720_test_case022.conf')
            time.sleep(30)
            
            os.system('nmcli device disconnect ens18')
            time.sleep(5)
            os.system('nmcli device connect ens18')
            time.sleep(10)

            r = os.popen('nmcli device show |grep IP4').read()
            print r
            b = 125
            print '192.168.50.'+str(b)+'/24'
            if '192.168.50.'+str(b)+'/24' in str(r):

                self.assertEqual(1,1)
                print ("PASS")
                ssh.close()
                Bquit()
                #UIRestD()

                Bsleep(3)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(10)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(10)
                
            else:

                ssh.close()
                Bquit()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            ssh.close()
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(10)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(10)
            
            if count <3:
                count+=1
                self.test_case022()

            else:
                self.assertEqual(1,0)


    def test_case023(self):

        "Case_1345 Extended DHCP Option"
        
        a = 0        
        try:

            Config_File_Upload('hd2hw4_720_test_case023.conf')
            time.sleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(5)
            os.system('nmcli device connect ens18')
            time.sleep(10)

            r = os.popen('nmcli device show |grep IP4.DOMAIN').read()
            print r
           
            if 'PEPLINK_TTC' in str(r):

                ssh.close()
                print 'PASS'

                Bsleep(3)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                
                Bquit()
                self.assertEqual(1,1)
           
            else:

                ssh.close()
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case023()

            else:
                self.assertEqual(1,0)

    
    def test_case024(self):

        "Case_1371 DHCP - Extended DHCP Option support"
        
        a = 0        
        try:
            Config_File_Upload('hd2hw4_720_test_case024.conf')
            time.sleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(5)
            os.system('nmcli device connect ens18')
            time.sleep(5)

            r = os.popen('nmcli device show |grep IP4.DOMAIN').read()
            print r
           
            if 'PEPLINK_TTC' in str(r):

                ssh.close()
                print 'PASS'
                #UIRestD()
                #time.sleep(32)

                Bsleep(3)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                
                Bquit()
                self.assertEqual(1,1)
           
            else:

                ssh.close()
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case024()

            else:
                self.assertEqual(1,0)


    
    def test_case025(self):

        "Case_1381 WINS Server & WINS Clients"
        try:
            a = 0        
            Config_File_Upload('hd2hw4_720_test_case025.conf')
            time.sleep(AppWait)
            os.system('nmcli device disconnect ens18')
            time.sleep(5)
            os.system('nmcli device connect ens18')
            time.sleep(5)

            r = os.popen('nmcli device show |grep WINS').read()
            print r
            
            if '3.3.3.3' in str(r):

                a += 1

            if '4.4.4.4' in str(r):

                a += 1

            if a == 2:

                print ("PASS")
                ssh.close()
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                
                self.assertEqual(1,1)


            else:

                ssh.close()
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            ssh.close()
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case025()

            else:
                self.assertEqual(1,0)

                
                
    def test_case026(self):

        "Case_1115 DNS Proxy Enable / Disable"
        a = 0

        try:
            
            driver = Bopen()
            UIsLogin(pepurl)
            Bquit()
            result1 = []
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(6)
            stdin, stdout, stderr = ssh.exec_command("nslookup www.peplink.com 192.168.50.1")
            time.sleep(6)
            for std in stdout.readlines():
              result1.append(std)

            print (str(result1))
            if '104.25.106.21' in str(result1):

                a += 1

            driver = Bopen()
            UIsLogin(pepurl)
            #DNS_Proxy_Disable()
            Config_File_Upload('hd2hw4_720_test_case026.conf')
            time.sleep(AppWait)
            
            result2 = []
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(6)
            stdin, stdout, stderr = ssh.exec_command("nslookup www.peplink.com 192.168.50.1")
            time.sleep(6)
            for std in stdout.readlines():
              result2.append(std)

            print (str(result2))
            if 'no servers could be reached' in str(result2):

                a += 1

            if a == 2:

                ssh.close()
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                
                self.assertEqual(1,1)

            else:

                ssh.close()
                Bquit()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            ssh.close()
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case026()

            else:
                self.assertEqual(1,0)


    
    def test_case027(self):

        "Case_1120 Local DNS Records"
        try:
            Config_File_Upload('hd2hw4_720_test_case027.conf')
            time.sleep(30)
            
            result1 = []
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(6)
            stdin, stdout, stderr = ssh.exec_command('nslookup pepttc.test.com 192.168.50.1')
            time.sleep(6)
            for std in stdout.readlines():
                result1.append(std)

            print (str(result1))
            
            if '210.1.1.10' in str(result1):

                
                print ("PASS")
                ssh.close()
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(AppWait)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                
                self.assertEqual(1,1)

            else:

                ssh.close()
                Bquit()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
  
            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(6)
            os.system('nmcli device connect ens18')
            time.sleep(6)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(6)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(6)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(8)
            
            if count <3:
                count+=1
                self.test_case027()

            else:
                self.assertEqual(1,0)

    def test_case028(self):
        
        "Case_1376 Bandwidth Allowance Link Disconnect"
        try:
            Config_File_Upload('hd2hw4_720_test_case028.conf')
            #time.sleep(AppWait)
            Bsleep(30)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            Bsleep(6)
            ssh.exec_command('iperf -c 10.88.80.11 -u -b 100m -i 2 -t 20')
            Bsleep(6)
            ssh.close()
            
            time.sleep(60)
            driver = Bopen()
            UIsLogin(pepurl)
            time.sleep(3)
            Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=main')
            time.sleep(6)
            
            if Btext('Hit'):
                print 'PASS'
                self.assertEqual(1,1)
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(6)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(6)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(6)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)

            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(6)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(6)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(6)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
   
            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(6)
            os.system('nmcli device connect ens18')
            time.sleep(5)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(6)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(6)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case028()

            else:
                self.assertEqual(1,0)


    def test_case029(self):

        "Case_1412 CLI - LAN/WAN Test"

        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case029.conf')
            time.sleep(AppWait)

            result1 = []
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            Bsleep(6)
            cmd = "sshpass -p admin ssh -o StrictHostKeyChecking=no admin@192.168.50.1 -p 8822 'get system;get cpu;'"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(6)
            for std in stdout.readlines():
                    
                result1.append(std)

            print (str(result1))

            if "Router Name" in str(result1):
                    
                a += 1


            result2 = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            Bsleep(6)
            cmd = "sshpass -p admin ssh -o StrictHostKeyChecking=no admin@10.88.81.1 -p 8822 'get system;get cpu;'"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(6)
            for std in stdout.readlines():
                    
                result2.append(std)

            print (str(result2))

            if "Router Name" in str(result2):
                    
                a += 1

            if a == 2:

                self.assertEqual(1,1)
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(AppWait)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                
            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case029()

            else:
                self.assertEqual(1,0)



    def test_case030(self):

        "Case_1108 DDNS Support no-ip.org"
        
        a = 0        
        try:
            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.50.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"')
            
            Bsleep(3)
            os.system('ping -c 4 '+HOST)
            time.sleep(6)
            tn = telnetlib.Telnet(HOST)
            Bsleep(6)
            tn.read_until("User:")
            Bsleep(6)
            tn.write("admin\r\n")
            Bsleep(6)
            tn.read_until("Password:")
            Bsleep(6)
            tn.write ('\r\n')
            Bsleep(6)
            tn.write("enable\r\n")
            Bsleep(6)        
            tn.write("config\r\n")
            Bsleep(6)
            tn.write("interface 0/"+PORT+"\r\n")
            Bsleep(6)
            tn.write("vlan participation include 3002\r\n")
            Bsleep(6)
            tn.write("vlan pvid 3002\r\n")
            Bsleep(6)
            tn.write("exit\r\n")
            tn.close
            print "test final"

            Config_File_Upload('hd2hw4_720_test_case030.conf')
            time.sleep(120)
            
            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(6)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            Bsleep(6)
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    WAN1IP=std
                    break
            ssh.close()
            
            WAN1IPA,WAN1IPB=WAN1IP.split(" : ")
            print "WAN1IPB ="+WAN1IPB
            WANIP=WAN1IPB
            print 'WANIP = '+WANIP
            time.sleep(2)
            ssh.connect('10.88.80.11' , port=22 ,username='peplink' , password='peplink')
            Bsleep(6)
            stdin, stdout, stderr = ssh.exec_command('nslookup -type=a tweric.no-ip.org 8.8.8.8 |grep Address')
            time.sleep(6)
            p=1
            for std in stdout.readlines():
                if ('Address' in std) and (p==2):
                    print std,
                    CheckIP=std
                    break
                p+=1
            ssh.close()
            CheckIPA,CheckIPB=CheckIP.split(": ")
            rIP=CheckIPB
            print 'NSLOOKUP result = '+rIP
            
            if rIP == WANIP:
                self.assertEqual(1,1)
                print "PASS"
                #UIRestD()
                #time.sleep(32)
                os.system('ping -c 4 '+HOST)
                time.sleep(2)
                tn = telnetlib.Telnet(HOST)
                time.sleep(6)        
                tn.read_until("User:")
                time.sleep(6)
                tn.write("admin\r\n")
                time.sleep(6)
                tn.read_until("Password:")
                time.sleep(6)
                tn.write ('\r\n')
                time.sleep(6)
                tn.write("enable\r\n")
                time.sleep(6)
                tn.write("config\r\n")
                time.sleep(6)
                tn.write("interface 0/"+PORT+"\r\n")
                time.sleep(6)
                tn.write("vlan pvid "+VID+"\r\n")
                time.sleep(6)
                tn.write("vlan participation auto 3002\r\n")
                time.sleep(6)
                tn.write("exit\r\n")
                print "port assign untag "+VID
                time.sleep(6)
                tn.close
                
                os.system('nmcli device disconnect ens19') 
                time.sleep(6)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(6)
                os.system('nmcli connection up "dhcp-ens18"')  
                Bsleep(8)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
            else:
                
                self.assertEqual(1,0)
                print "FAIL"
                #UIRestD()
                #time.sleep(32)
                os.system('ping -c 4 '+HOST)
                time.sleep(2)
                tn = telnetlib.Telnet(HOST)
                time.sleep(6)        
                tn.read_until("User:")
                time.sleep(6)
                tn.write("admin\r\n")
                time.sleep(6)
                tn.read_until("Password:")
                time.sleep(6)
                tn.write ('\r\n')
                time.sleep(6)
                tn.write("enable\r\n")
                time.sleep(6)
                tn.write("config\r\n")
                time.sleep(6)
                tn.write("interface 0/"+PORT+"\r\n")
                time.sleep(6)
                tn.write("vlan pvid "+VID+"\r\n")
                time.sleep(6)
                tn.write("vlan participation auto 3002\r\n")
                time.sleep(6)
                tn.write("exit\r\n")
                print "port assign untag "+VID
                time.sleep(6)
                tn.close
                
                os.system('nmcli device disconnect ens19') 
                time.sleep(6)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(6)
                os.system('nmcli connection up "dhcp-ens18"')  
                Bsleep(8)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            ssh.close()
            #UIRestD()
            #time.sleep(32)
            os.system('ping -c 4 '+HOST)
            time.sleep(2)
            tn = telnetlib.Telnet(HOST)
            time.sleep(6)        
            tn.read_until("User:")
            time.sleep(6)
            tn.write("admin\r\n")
            time.sleep(6)
            tn.read_until("Password:")
            time.sleep(6)
            tn.write ('\r\n')
            time.sleep(6)
            tn.write("enable\r\n")
            time.sleep(6)
            tn.write("config\r\n")
            time.sleep(6)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(6)
            tn.write("vlan pvid "+VID+"\r\n")
            time.sleep(6)
            tn.write("vlan participation auto 3002\r\n")
            time.sleep(6)
            tn.write("exit\r\n")
            print "port assign untag "+VID
            time.sleep(2)
            tn.close
            os.system('nmcli device disconnect ens19') 
            time.sleep(6)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(6)
            os.system('nmcli connection up "dhcp-ens18"')
            Bsleep(8)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            time.sleep(30)
            if count <3:
                count+=1
                self.test_case030()

            else:
                self.assertEqual(1,0)

    def test_case031(self):
        "Case_1113 DDNS Support changeip.com"

        
        a = 0
        try:
            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.50.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"')
            
            tn = telnetlib.Telnet(HOST)
            time.sleep(6)
            tn.read_until("User:")
            time.sleep(6)
            tn.write("admin\r\n")
            time.sleep(6)
            tn.read_until("Password:")
            time.sleep(6)
            tn.write ('\r\n')
            time.sleep(6)
            tn.write("enable\r\n")
            time.sleep(6)        
            tn.write("config\r\n")
            time.sleep(6)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(6)
            tn.write("vlan participation include 3002\r\n")
            time.sleep(6)
            tn.write("vlan pvid 3002\r\n")
            time.sleep(6)
            tn.write("exit\r\n")
            tn.close
            print "test final"

            Config_File_Upload('hd2hw4_720_test_case031.conf')
            Bsleep(120)

            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(6)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            Bsleep(6)
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    WAN1IP=std
                    break
            ssh.close()
            
            WAN1IPA,WAN1IPB=WAN1IP.split(" : ")
            print "WAN1IPB ="+WAN1IPB
            WANIP=WAN1IPB
            print 'WANIP = '+WANIP
            time.sleep(2)

            CheckIP = subprocess.check_output('dig @8.8.8.8 +noall +answer andersonw.changeip.org', shell=True)
            Bsleep(6)
            print 'CheckIP = '
            print CheckIP
            CheckIPA,CheckIPB=CheckIP.split("A	")
            rIP=CheckIPB
            print 'NSLOOKUP result:andersonw.changeip.org = '+rIP
            Bsleep(20)
            
            if rIP == WANIP:
                a += 1

            if a == 1:

                self.assertEqual(1,1)
                print ("PASS")
                #UIRestD()
                #time.sleep(32)
                os.system('ping -c 4 '+HOST)
                time.sleep(2)
                tn = telnetlib.Telnet(HOST)
                time.sleep(2)        
                tn.read_until("User:")
                time.sleep(2)
                tn.write("admin\r\n")
                time.sleep(2)
                tn.read_until("Password:")
                time.sleep(2)
                tn.write ('\r\n')
                time.sleep(2)
                tn.write("enable\r\n")
                time.sleep(2)
                tn.write("config\r\n")
                time.sleep(2)
                tn.write("interface 0/"+PORT+"\r\n")
                time.sleep(2)
                tn.write("vlan pvid "+VID+"\r\n")
                time.sleep(2)
                tn.write("vlan participation auto 3002\r\n")
                time.sleep(2)
                tn.write("exit\r\n")
                print "port assign untag "+VID
                time.sleep(2)
                tn.close
                Bsleep(6)
                os.system('nmcli device disconnect ens19') 
                time.sleep(6)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(6)
                os.system('nmcli connection up "dhcp-ens18"')  
                Bsleep(8)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)

            else:

                ssh.close()
                Bquit()
                self.assertEqual(1,0)
                print ("FAIL")
                #UIRestD()
                #time.sleep(32)
                os.system('ping -c 4 '+HOST)
                time.sleep(2)
                tn = telnetlib.Telnet(HOST)
                time.sleep(2)        
                tn.read_until("User:")
                time.sleep(2)
                tn.write("admin\r\n")
                time.sleep(2)
                tn.read_until("Password:")
                time.sleep(2)
                tn.write ('\r\n')
                time.sleep(2)
                tn.write("enable\r\n")
                time.sleep(2)
                tn.write("config\r\n")
                time.sleep(2)
                tn.write("interface 0/"+PORT+"\r\n")
                time.sleep(2)
                tn.write("vlan pvid "+VID+"\r\n")
                time.sleep(2)
                tn.write("vlan participation auto 3002\r\n")
                time.sleep(2)
                tn.write("exit\r\n")
                print "port assign untag "+VID
                time.sleep(2)
                tn.close
                Bsleep(6)
                os.system('nmcli device disconnect ens19') 
                time.sleep(6)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(6)
                os.system('nmcli connection up "dhcp-ens18"')  
                Bsleep(8)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
        except:

            global count
            try:
                Bquit()

            except:
                a=0
            ssh.close()
            #UIRestD()
            #time.sleep(32)
            tn = telnetlib.Telnet(HOST)
            time.sleep(2)        
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan pvid "+VID+"\r\n")
            time.sleep(2)
            tn.write("vlan participation auto 3002\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            print "port assign untag "+VID
            time.sleep(2)
            tn.close
            os.system('nmcli device disconnect ens19') 
            time.sleep(6)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(6)
            os.system('nmcli connection up "dhcp-ens18"')  
            Bsleep(8)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            if count <3:
                count+=1
                self.test_case031()

            else:
                self.assertEqual(1,0)



    def test_case032(self):

        "Case_1112 DDNS Two host support"
        
        a = 0
        try:
            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.50.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"')
            time.sleep(8)
            os.system('ping -c 4 '+HOST)
            time.sleep(2)
            tn = telnetlib.Telnet(HOST)
            time.sleep(6)
            tn.read_until("User:")
            time.sleep(6)
            tn.write("admin\r\n")
            time.sleep(6)
            tn.read_until("Password:")
            time.sleep(6)
            tn.write ('\r\n')
            time.sleep(6)
            tn.write("enable\r\n")
            time.sleep(6)        
            tn.write("config\r\n")
            time.sleep(6)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(6)
            tn.write("vlan participation include 3002\r\n")
            time.sleep(6)
            tn.write("vlan pvid 3002\r\n")
            time.sleep(6)
            tn.write("exit\r\n")
            tn.close
            print "test final"

            Config_File_Upload('hd2hw4_720_test_case032.conf')
            time.sleep(AppWait)
            Bsleep(120)

            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(6)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            Bsleep(6)
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    WAN1IP=std
                    break
            ssh.close()
            
            WAN1IPA,WAN1IPB=WAN1IP.split(" : ")
            print "WAN1IPB ="+WAN1IPB
            WANIP=WAN1IPB
            print 'WANIP = '+WANIP
            time.sleep(2)
            CheckIP = subprocess.check_output('dig @8.8.8.8 +noall +answer andersonw.changeip.org', shell=True)
            Bsleep(6)
            print 'CheckIP = '
            print CheckIP
            CheckIPA,CheckIPB=CheckIP.split("A	")
            rIP=CheckIPB
            print 'NSLOOKUP result:andersonw.changeip.org = '+rIP
            Bsleep(20)
            CheckIP2 = subprocess.check_output('dig @8.8.8.8 +noall +answer andersonw1.changeip.org', shell=True)
            time.sleep(10)
            print 'CheckIP2 = '
            print CheckIP2
            CheckIP2A,CheckIP2B=CheckIP2.split("A	")
            rIP2=CheckIP2B
            result2=rIP2
            print 'WANIP = '+WANIP
            print 'NSLOOKUP result:andersonw1.changeip.org = '+rIP2
            Bsleep(6)
            
            if rIP == WANIP:
                a += 1

            if rIP2 == WANIP:
                a += 1

            if a == 2:

                self.assertEqual(1,1)
                print ("PASS")
                tn = telnetlib.Telnet(HOST)
                time.sleep(2)        
                tn.read_until("User:")
                time.sleep(2)
                tn.write("admin\r\n")
                time.sleep(2)
                tn.read_until("Password:")
                time.sleep(2)
                tn.write ('\r\n')
                time.sleep(2)
                tn.write("enable\r\n")
                time.sleep(2)
                tn.write("config\r\n")
                time.sleep(2)
                tn.write("interface 0/"+PORT+"\r\n")
                time.sleep(2)
                tn.write("vlan pvid "+VID+"\r\n")
                time.sleep(2)
                tn.write("vlan participation auto 3002\r\n")
                time.sleep(2)
                tn.write("exit\r\n")
                print "port assign untag "+VID
                time.sleep(2)
                tn.close
                os.system('nmcli device disconnect ens19') 
                time.sleep(6)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(6)
                os.system('nmcli connection up "dhcp-ens18"')  
                Bsleep(8)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
            else:
                ssh.close()
                Bquit()
                self.assertEqual(1,0)
                print 'FAIL'
                tn = telnetlib.Telnet(HOST)
                time.sleep(2)        
                tn.read_until("User:")
                time.sleep(2)
                tn.write("admin\r\n")
                time.sleep(2)
                tn.read_until("Password:")
                time.sleep(2)
                tn.write ('\r\n')
                time.sleep(2)
                tn.write("enable\r\n")
                time.sleep(2)
                tn.write("config\r\n")
                time.sleep(2)
                tn.write("interface 0/"+PORT+"\r\n")
                time.sleep(2)
                tn.write("vlan pvid "+VID+"\r\n")
                time.sleep(2)
                tn.write("vlan participation auto 3002\r\n")
                time.sleep(2)
                tn.write("exit\r\n")
                print "port assign untag "+VID
                time.sleep(2)
                tn.close
                os.system('nmcli device disconnect ens19') 
                time.sleep(6)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(6)
                os.system('nmcli connection up "dhcp-ens18"')  
                Bsleep(8)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
        except:

            global count
            try:
                Bquit()

            except:
                a=0
            ssh.close()
            tn = telnetlib.Telnet(HOST)
            time.sleep(2)        
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan pvid "+VID+"\r\n")
            time.sleep(2)
            tn.write("vlan participation auto 3002\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            print "port assign untag "+VID
            time.sleep(2)
            tn.close
            os.system('nmcli device disconnect ens19') 
            time.sleep(6)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(6)
            os.system('nmcli connection up "dhcp-ens18"')  
            Bsleep(8)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            if count <3:
                count+=1
                self.test_case032()

            else:
                self.assertEqual(1,0)


    def test_case033(self):

        "Case_1113 DDNS Update status regularly"

        a = 0
        try:
            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.50.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"')
            time.sleep(8)
            os.system('ping -c 4 '+HOST)
            time.sleep(2)
            tn = telnetlib.Telnet(HOST)
            time.sleep(2)
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)        
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan participation include 3002\r\n")
            time.sleep(2)
            tn.write("vlan pvid 3002\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            tn.close
            print "test final"

            Config_File_Upload('hd2hw4_720_test_case033.conf')
            time.sleep(AppWait)
            Bsleep(120)

            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            Bsleep(6)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            Bsleep(6)
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    WAN1IP=std
                    break
            ssh.close()
            
            WAN1IPA,WAN1IPB=WAN1IP.split(" : ")
            print "WAN1IPB ="+WAN1IPB
            WANIP=WAN1IPB
            print 'WANIP = '+WANIP
            Bsleep(6)
            CheckIP = subprocess.check_output('dig @8.8.8.8 +noall +answer andersonw1.no-ip.org', shell=True)
            time.sleep(6)
            CheckIPA,CheckIPB=CheckIP.split("A	")
            rIP=CheckIPB
            print 'NSLOOKUP result = '+rIP
            result = rIP
            Bsleep(10)
            
            if result == WANIP:
                a+=1
                
            if a ==1:
                self.assertEqual(1,1)
                print ("PASS")
                ssh.close()
                Bquit()
                
                tn = telnetlib.Telnet(HOST)
                time.sleep(2)        
                tn.read_until("User:")
                time.sleep(2)
                tn.write("admin\r\n")
                time.sleep(2)
                tn.read_until("Password:")
                time.sleep(2)
                tn.write ('\r\n')
                time.sleep(2)
                tn.write("enable\r\n")
                time.sleep(2)
                tn.write("config\r\n")
                time.sleep(2)
                tn.write("interface 0/"+PORT+"\r\n")
                time.sleep(2)
                tn.write("vlan pvid "+VID+"\r\n")
                time.sleep(2)
                tn.write("vlan participation auto 3002\r\n")
                time.sleep(2)
                tn.write("exit\r\n")
                print "port assign untag "+VID
                time.sleep(2)
                tn.close
                os.system('nmcli device disconnect ens19') 
                time.sleep(6)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(6)
                os.system('nmcli connection up "dhcp-ens18"')  
                Bsleep(8)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
            else:
                #ssh.close()
                #Bquit()
                self.assertEqual(1,0)
                print 'FAIL'
                tn = telnetlib.Telnet(HOST)
                time.sleep(2)        
                tn.read_until("User:")
                time.sleep(2)
                tn.write("admin\r\n")
                time.sleep(2)
                tn.read_until("Password:")
                time.sleep(2)
                tn.write ('\r\n')
                time.sleep(2)
                tn.write("enable\r\n")
                time.sleep(2)
                tn.write("config\r\n")
                time.sleep(2)
                tn.write("interface 0/"+PORT+"\r\n")
                time.sleep(2)
                tn.write("vlan pvid "+VID+"\r\n")
                time.sleep(2)
                tn.write("vlan participation auto 3002\r\n")
                time.sleep(2)
                tn.write("exit\r\n")
                print "port assign untag "+VID
                time.sleep(2)
                tn.close
                os.system('nmcli device disconnect ens19') 
                time.sleep(6)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(6)
                os.system('nmcli connection up "dhcp-ens18"')  
                Bsleep(8)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            ssh.close()
            #UIRestD()
            #time.sleep(32)
            tn = telnetlib.Telnet(HOST)
            time.sleep(2)        
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan pvid "+VID+"\r\n")
            time.sleep(2)
            tn.write("vlan participation auto 3002\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            print "port assign untag "+VID
            time.sleep(2)
            tn.close
            os.system('nmcli device disconnect ens19') 
            time.sleep(6)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(6)
            os.system('nmcli connection up "dhcp-ens18"')  
            Bsleep(8)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            if count <3:
                count+=1
                self.test_case033()

            else:
                self.assertEqual(1,0)


    def test_case034(self):

        "Case_1114 DDNS Link IP Change"
        
        a = 0
        try:
            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.50.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"')
            time.sleep(8)
            os.system('ping -c 4 '+HOST)
            time.sleep(2)
            driver = Bopen()
            UIsLogin(pepurl)

            tn = telnetlib.Telnet(HOST)
            time.sleep(2)
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)        
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan participation include 3002\r\n")
            time.sleep(2)
            tn.write("vlan pvid 3002\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            tn.close
            print "test final"

            time.sleep(2)
            Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
            time.sleep(2)
            Bclick('.conn_method_action > option:nth-child(4)')
            time.sleep(2)
            Bfill('.pppoe_panel > tr:nth-child(2) > td:nth-child(2) > input:nth-child(1)', 'T1170871')
            time.sleep(2)
            Bfill('.pppoe_panel > tr:nth-child(3) > td:nth-child(2) > input:nth-child(1)', 'fn6xp8td')
            time.sleep(2)
            Bfill('.pppoe_panel > tr:nth-child(4) > td:nth-child(2) > input:nth-child(1)', 'fn6xp8td')
            time.sleep(2)
            Bclick('.ddns_action > option:nth-child(4)')
            time.sleep(2)
            Bfill('tr.ddns_default_panel:nth-child(3) > td:nth-child(2) > input:nth-child(1)', 'erich@peplink.com')
            time.sleep(2)
            Bfill('tr.ddns_default_panel:nth-child(4) > td:nth-child(2) > input:nth-child(1)', '09!@#$')
            time.sleep(2)
            Bfill('tr.ddns_default_panel:nth-child(5) > td:nth-child(2) > input:nth-child(1)', '09!@#$')
            time.sleep(2)
            Bfill('.ddns_host_panel > td:nth-child(2) > textarea:nth-child(1)', 'tweric.no-ip.org')
            time.sleep(2)
            BclickT('Save')
            time.sleep(2)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bclick('li.pt__item:nth-child(2) > div:nth-child(1) > span:nth-child(3) > span:nth-child(2) > button:nth-child(1)')
            OldIP = re.findall(r'<span class="ipaddr">(.*?)</span>',driver.page_source)
            #OldIP = re.findall(r'<span id="conn_status_ip_1">(.*?)</span>',driver.page_source)

            time.sleep(5)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
            time.sleep(2)
            Bncheck('#enable_display > td:nth-child(2) > input:nth-child(1)')
            #BclickT('Disconnect')
            time.sleep(6)
            Bclick('.save_action')
            time.sleep(2)
            UIsApply(pepurl)
            #Bclick("#conn_button_disconnect_1")
            time.sleep(2)
            #BclickT("OK")
            time.sleep(20)
            
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
            time.sleep(2)
            Bcheck('#enable_display > td:nth-child(2) > input:nth-child(1)')
            time.sleep(6)
            Bclick('.save_action')
            time.sleep(2)
            UIsApply(pepurl)
            #Bclick("#conn_button_connect_1")
            time.sleep(120)
            Bclick('li.pt__item:nth-child(2) > div:nth-child(1) > span:nth-child(3) > span:nth-child(2) > button:nth-child(1)')
            NewIP = re.findall(r'<span class="ipaddr">(.*?)</span>',driver.page_source)
            print 'NewIP = '
            print NewIP
            #NewIP = re.findall(r'<span id="conn_status_ip_1">(.*?)</span>',driver.page_source)
                        
            if str(NewIP[0]) != "(none)" and OldIP[0] != NewIP[0]:

                ssh.connect('10.88.80.11' , port=22 ,username='peplink' , password='peplink')
                Bsleep(6)
                stdin, stdout, stderr = ssh.exec_command('nslookup -type=a tweric.no-ip.org 8.8.8.8')
                time.sleep(6)

                CheckIP = stdout.read()
                result = re.findall(r'Address: (.*)',CheckIP)

                if result == NewIP:

                    self.assertEqual(1,1)
                    print ("PASS")
                    ssh.close()
                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    
                    tn = telnetlib.Telnet(HOST)
                    time.sleep(2)        
                    tn.read_until("User:")
                    time.sleep(2)
                    tn.write("admin\r\n")
                    time.sleep(2)
                    tn.read_until("Password:")
                    time.sleep(2)
                    tn.write ('\r\n')
                    time.sleep(2)
                    tn.write("enable\r\n")
                    time.sleep(2)
                    tn.write("config\r\n")
                    time.sleep(2)
                    tn.write("interface 0/"+PORT+"\r\n")
                    time.sleep(2)
                    tn.write("vlan pvid "+VID+"\r\n")
                    time.sleep(2)
                    tn.write("vlan participation auto 3002\r\n")
                    time.sleep(2)
                    tn.write("exit\r\n")
                    print "port assign untag "+VID
                    time.sleep(2)
                    tn.close
                    os.system('nmcli device disconnect ens19') 
                    time.sleep(6)
                    os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                    time.sleep(6)
                    os.system('nmcli connection up "dhcp-ens18"')  
                    Bsleep(8)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                else:

                    ssh.close()
                    Bquit()
                    self.assertEqual(1,0)
                    print 'FAIL'
                    tn = telnetlib.Telnet(HOST)
                    time.sleep(2)        
                    tn.read_until("User:")
                    time.sleep(2)
                    tn.write("admin\r\n")
                    time.sleep(2)
                    tn.read_until("Password:")
                    time.sleep(2)
                    tn.write ('\r\n')
                    time.sleep(2)
                    tn.write("enable\r\n")
                    time.sleep(2)
                    tn.write("config\r\n")
                    time.sleep(2)
                    tn.write("interface 0/"+PORT+"\r\n")
                    time.sleep(2)
                    tn.write("vlan pvid "+VID+"\r\n")
                    time.sleep(2)
                    tn.write("vlan participation auto 3002\r\n")
                    time.sleep(2)
                    tn.write("exit\r\n")
                    print "port assign untag "+VID
                    time.sleep(2)
                    tn.close
                    os.system('nmcli device disconnect ens19') 
                    time.sleep(6)
                    os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                    time.sleep(6)
                    os.system('nmcli connection up "dhcp-ens18"')  
                    Bsleep(8)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
        except:

            global count
            try:
                Bquit()

            except:
                a=0
            ssh.close()
            #UIRestD()
            #time.sleep(32)
            tn = telnetlib.Telnet(HOST)
            time.sleep(2)        
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan pvid "+VID+"\r\n")
            time.sleep(2)
            tn.write("vlan participation auto 3002\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            print "port assign untag "+VID
            time.sleep(2)
            tn.close
            os.system('nmcli device disconnect ens19') 
            time.sleep(6)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(6)
            os.system('nmcli connection up "dhcp-ens18"')  
            Bsleep(8)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            if count <3:
                count+=1
                self.test_case034()

            else:
                self.assertEqual(1,0)

    def test_case035(self):

        "Case_1328 DDNS password support !#"
        
        a = 0
        try:
            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.50.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"')
            time.sleep(8)
            os.system('ping -c 4 '+HOST)
            time.sleep(2)
            tn = telnetlib.Telnet(HOST)
            time.sleep(2)
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)        
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan participation include 3002\r\n")
            time.sleep(2)
            tn.write("vlan pvid 3002\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            tn.close
            print "test final"

            Config_File_Upload('hd2hw4_720_test_case035.conf')
            Bsleep(120)
            
            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(6)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            Bsleep(6)
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    WAN1IP=std
                    break
            ssh.close()
            WAN1IPA,WAN1IPB=WAN1IP.split(" : ")
            print "WAN1IPB ="+WAN1IPB
            WANIP=WAN1IPB
            print 'WANIP = '+WANIP
            time.sleep(2)
            CheckIP = subprocess.check_output('dig @8.8.8.8 +noall +answer tweric.no-ip.org', shell=True)
            time.sleep(6)
            CheckIPA,CheckIPB=CheckIP.split("A	")
            rIP=CheckIPB
            print 'NSLOOKUP result = '+rIP
            result = rIP

            if result == WANIP:

                self.assertEqual(1,1)
                print ("PASS")
                ssh.close()
                Bquit()
                #UIRestD()
                #time.sleep(32)
                
                print result[0]
                print WANIP[0]
                
                tn = telnetlib.Telnet(HOST)
                time.sleep(2)        
                tn.read_until("User:")
                time.sleep(2)
                tn.write("admin\r\n")
                time.sleep(2)
                tn.read_until("Password:")
                time.sleep(2)
                tn.write ('\r\n')
                time.sleep(2)
                tn.write("enable\r\n")
                time.sleep(2)
                tn.write("config\r\n")
                time.sleep(2)
                tn.write("interface 0/"+PORT+"\r\n")
                time.sleep(2)
                tn.write("vlan pvid "+VID+"\r\n")
                time.sleep(2)
                tn.write("vlan participation auto 3002\r\n")
                time.sleep(2)
                tn.write("exit\r\n")
                print "port assign untag "+VID
                time.sleep(2)
                tn.close
                Bsleep(3)
                os.system('nmcli device disconnect ens19') 
                time.sleep(6)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(6)
                os.system('nmcli connection up "dhcp-ens18"')  
                Bsleep(8)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
            else:

                ssh.close()
                Bquit()
                self.assertEqual(1,0)
                print 'FAIL'
                tn = telnetlib.Telnet(HOST)
                time.sleep(2)        
                tn.read_until("User:")
                time.sleep(2)
                tn.write("admin\r\n")
                time.sleep(2)
                tn.read_until("Password:")
                time.sleep(2)
                tn.write ('\r\n')
                time.sleep(2)
                tn.write("enable\r\n")
                time.sleep(2)
                tn.write("config\r\n")
                time.sleep(2)
                tn.write("interface 0/"+PORT+"\r\n")
                time.sleep(2)
                tn.write("vlan pvid "+VID+"\r\n")
                time.sleep(2)
                tn.write("vlan participation auto 3002\r\n")
                time.sleep(2)
                tn.write("exit\r\n")
                print "port assign untag "+VID
                time.sleep(2)
                tn.close
                Bsleep(3)
                os.system('nmcli device disconnect ens19') 
                time.sleep(6)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(6)
                os.system('nmcli connection up "dhcp-ens18"')  
                Bsleep(8)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
        except:

            global count
            try:
                Bquit()

            except:
                a=0
            ssh.close()
            #UIRestD()
            #time.sleep(32)
            tn = telnetlib.Telnet(HOST)
            time.sleep(2)        
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan pvid "+VID+"\r\n")
            time.sleep(2)
            tn.write("vlan participation auto 3002\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            print "port assign untag "+VID
            time.sleep(2)
            tn.close
            Bsleep(3)
            os.system('nmcli device disconnect ens19') 
            time.sleep(6)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(6)
            os.system('nmcli connection up "dhcp-ens18"')  
            Bsleep(8)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            if count <3:
                count+=1
                self.test_case035()

            else:
                self.assertEqual(1,0)

    def test_case036(self):

        "Case_1397-Firewall - Inbound Allow /default deny"
        try:
            Config_File_Upload('hd2hw4_720_test_case036.conf')
            time.sleep(AppWait)
            Bsleep(30)
            #clear log
            driver = Bopen()
            UIsLogin(pepurl)
            Bsleep(3)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(2)
            BclickT("Clear Log")
            time.sleep(10)
            Bquit()
            ssh.connect('192.168.50.9' , username="peplink" , password="peplink")
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            #print 'Log folder Clear!!'
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            #print 'Python Task Clear!!'
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 80 &> log/T80.tmp&')
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 21 &> log/T21.tmp&')
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 110 &> log/T110.tmp&')
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 25 &> log/T25.tmp&')
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 U 666 &> log/U666.tmp&')
            Bsleep(6)

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")                
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            #print 'Log folder Clear!!'
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            #print 'Python Task Clear!!'
            #print 'Test Running Wait...' 
            Bsleep(6)
            stdin, stdout, stderr = ssh.exec_command("echo peplink | sudo -S python PogoU64.py W1 10.88.81.1 60")
            Bsleep(6)
            for std in stdout.readlines():               
                print std

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")  
            Bsleep(6)
            apath = 'log'
            apattern ='"*.log"'
            rawcommand = 'find {path} -name {pattern}'
            command = rawcommand.format(path=apath, pattern=apattern)

            stdin, stdout, stderr = ssh.exec_command(command)
            Bsleep(6)
            filelist = stdout.read().splitlines()

            #print filelist

            sftp = ssh.open_sftp()
            for afile in filelist:
                (head, filename) = os.path.split(afile)
                print(filename)
                stdin, stdout, stderr = ssh.exec_command('cat ' + afile)
                r1 = stdout.read()
            
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            Bsleep(6)
            if ('Allowed CONN'):

                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(20)
                
                ssh.close()
                self.assertEqual(1,1)
                
            else:
                Bquit()
                ssh.close()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
       
            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            time.sleep(20)
            
            if count <3:
                count+=1
                self.test_case036()

            else:
                self.assertEqual(1,0)

    
    def test_case037(self):

        "Case_1398-Firewall - Inbound deny /default Allow"

        try:
            Config_File_Upload('hd2hw4_720_test_case037.conf')
            Bsleep(30)
            #clear log
            driver = Bopen()
            UIsLogin(pepurl)
            Bsleep(3)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(2)
            BclickT("Clear Log")
            time.sleep(10)
            Bquit()
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            Bsleep(6)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.81.1')
            t = stdout.read()

            if '0 received' in str(t):
                driver = Bopen()
                UIsLogin(pepurl)
                Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                time.sleep(6)
                
                if Btext('Denied CONN'):

                    print ("PASS")
                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(40)
                    self.assertEqual(1,1)

                else:
                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    time.sleep(40)
                    self.assertEqual(1,0)
                    
            else:
                
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(40)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
 
            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            time.sleep(40)
            
            if count <3:
                count+=1
                self.test_case037()

            else:
                self.assertEqual(1,0)


    def test_case038(self):

        "Case_1399-Firewall - Outbound deny /default Allow"

        try:
            #clear log
            driver = Bopen()
            UIsLogin(pepurl)
            Bsleep(3)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(2)
            BclickT("Clear Log")
            time.sleep(10)
            Bquit()
            
            driver = Bopen()
            UIsLogin(pepurl)
            print '==1=='
            Wan_set(1)
            print '==2=='
            NAT_Mapping()
            FireWallRlue1399()
            UIsApply(pepurl)
            time.sleep(AppWait)
            
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(6)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.80.11')
            Bsleep(6)
            t = stdout.read()
            print('Case_1399-Firewall \n',str(t))
            if '0 received' in str(t):

                Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                time.sleep(6)
                
                if Btext('Denied CONN'):

                    print ("PASS")
                    Bquit()
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    time.sleep(40)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)   
                    os.system('nmcli device disconnect ens19') 
                    time.sleep(2)
                    self.assertEqual(1,1)
                    
                else:
                    
                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(40)
                    os.system('nmcli device disconnect ens19') 

                    time.sleep(5)
                    self.assertEqual(1,0)

            else:
                
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(40)
                os.system('nmcli device disconnect ens19') 
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(40)
            os.system('nmcli device disconnect ens19') 

            time.sleep(5)

            if count <3:
                count+=1
                self.test_case038()

            else:
                self.assertEqual(1,0)


    def test_case039(self):

        "Case_1400-Firewall - Outbound Allow /default deny"

        try:
            #clear log
            driver = Bopen()
            UIsLogin(pepurl)
            Bsleep(3)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(2)
            BclickT("Clear Log")
            time.sleep(10)
            Bquit()
            
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1) 
            NAT_Mapping()
            FireWallRlue1400()
            UIsApply(pepurl)
            time.sleep(AppWait)

            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(6)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.80.11')
            Bsleep(6)
            t = stdout.read()

            if '4 received' in str(t):

                Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                time.sleep(2)
                
                if Btext('Allowed CONN'):

                    print ("PASS")
                    Bquit()
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(40)
                    self.assertEqual(1,1)

                else:

                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(40)
                    os.system('nmcli device disconnect ens19')
                    time.sleep(5)
                    self.assertEqual(1,0)

            else:
                
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(40)
                os.system('nmcli device disconnect ens19')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(40)
            if count <3:
                count+=1
                self.test_case039()

            else:
                self.assertEqual(1,0)



    def test_case040(self):

        "Case_1841 Firewall - OutBound Block Domain"
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case040-1.conf')
            Bsleep(40)
            #clear log
            driver = Bopen()
            UIsLogin(pepurl)
            Bsleep(3)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(2)
            BclickT("Clear Log")
            time.sleep(10)
            Bquit()
            
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(6)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 lo.pepttc.com')
            Bsleep(6)
            t = stdout.read()

            if '4 received' in str(t):
                a += 1
            Bsleep(6)

            Config_File_Upload('hd2hw4_720_test_case040-2.conf')
            Bsleep(40)

            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(6)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 lo.pepttc.com')
            t = stdout.read()

            if '0 received' in str(t):
                a += 1
            
            Bsleep(6)
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(6)
            
            if Btext('Denied CONN=lan MAC='):

                a += 1


            if a == 3:
                print 'PASS'
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(40)
                self.assertEqual(1,1)
            else:
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(40)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            time.sleep(40)
            if count <3:
                count+=1
                self.test_case040()

            else:
                self.assertEqual(1,0)
                
    def test_case041(self):
          
        "Case_1842 Firewall - OutBound Allow Domain"
        a = 0
        try:
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            time.sleep(2)
            UIsApply(pepurl)
            time.sleep(AppWait)
            
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 lo.pepttc.com')
            t = stdout.read()

            if '4 received' in str(t):
                a += 1

            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=firewall')
            time.sleep(2)
            Bclick('#firewall_settings > table:nth-child(2) > tfoot > tr:nth-child(2) > td > button')
            time.sleep(2)
            Bfill('tr.tablecontent2:nth-child(2) > td:nth-child(2) > input:nth-child(1)','Firewall By Domain')
            time.sleep(2)
            Bclick('tr.tablecontent2:nth-child(8) > td:nth-child(2) > div:nth-child(1) > select:nth-child(1) > option:nth-child(4)')
            time.sleep(2)
            Bfill('.domain > input:nth-child(1)','lo.pepttc.com')
            time.sleep(2)
            Bcheck('tr.tablecontent2:nth-child(10) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
            time.sleep(2)
            SBclickT('Save')
            time.sleep(5)
            UIsApply(pepurl)
            time.sleep(30)

            #clear log
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(2)
            BclickT("Clear Log")
            time.sleep(10)
            
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 lo.pepttc.com')
            t = stdout.read()

            if '4 received' in str(t):

                a += 1

            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(2)
            
            if Btext('Allowed CONN=lan'):

                a += 1

            if a == 3:
                print 'PASS'
                Bquit()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(40)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                self.assertEqual(1,1)

            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(40)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            time.sleep(40)
            if count <3:
                count+=1
                self.test_case041()

            else:
                self.assertEqual(1,0)


    def test_case042(self):

        "Case_1264 - NAT Mapping"
        try:
            a = 0
            b = 0
            Config_File_Upload('hd2hw4_720_test_case042.conf')
            time.sleep(AppWait)
            Bsleep(30)

            ssh.connect('192.168.50.9' , username="peplink" , password="peplink")
            Bsleep(5)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            #print 'Log folder Clear!!'
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            #print 'Python Task Clear!!'
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 80 &> log/T80.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 21 &> log/T21.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 110 &> log/T110.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 25 &> log/T25.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 U 666 &> log/U666.tmp&')
            Bsleep(3)
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            #print 'Log folder Clear!!'
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            #print 'Python Task Clear!!'
            #print 'Test Running Wait...'
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command("echo peplink | sudo -S python PogoU64.py W1 10.88.81.1 60")
            Bsleep(3)
            for std in stdout.readlines():
                print std
            Bsleep(3)
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            Bsleep(3)
            apath = 'log'
            apattern ='"*.log"'
            rawcommand = 'find {path} -name {pattern}'
            command = rawcommand.format(path=apath, pattern=apattern)
            stdin, stdout, stderr = ssh.exec_command(command)
            Bsleep(3)
            filelist = stdout.read().splitlines()

            #print filelist

            sftp = ssh.open_sftp()
            Bsleep(3)
            for afile in filelist:
                (head, filename) = os.path.split(afile)
                print(filename)
                stdin, stdout, stderr = ssh.exec_command('cat ' + afile)
                r1 = stdout.read()

            if "Ping Test: Pass" in (str(r1)):
                a += 1

            if "TCP 80 Test: Pass" in (str(r1)):
                a += 1

            if "TCP 21 Test: Pass" in (str(r1)):
                a += 1

            if "TCP 110 Test: Pass" in (str(r1)):
                a += 1

            if "TCP 25 Test: Pass" in (str(r1)):
                a += 1

            if "UDP 666 Test: Pass" in (str(r1)):
                a += 1

            ssh.close()

            ssh.connect('192.168.50.9' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            #print 'Log folder Clear!!'
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            #print 'Python Task Clear!!'
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 80 &> log/T80.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 21 &> log/T21.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 110 &> log/T110.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 25 &> log/T25.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 U 666 &> log/U666.tmp&')
            Bsleep(3)
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            #print 'Log folder Clear!!'
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            #print 'Python Task Clear!!'
            #print 'Test Running Wait...' 
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command("echo peplink | sudo -S python PogoU64.py W1 10.88.81.51 60")
            Bsleep(3)
            for std in stdout.readlines():
                print std
            Bsleep(3)
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")  
            Bsleep(3)
            apath = 'log'
            apattern ='"*.log"'
            rawcommand = 'find {path} -name {pattern}'
            command = rawcommand.format(path=apath, pattern=apattern)

            stdin, stdout, stderr = ssh.exec_command(command)
            Bsleep(3)
            filelist = stdout.read().splitlines()

            #print filelist

            sftp = ssh.open_sftp()
            Bsleep(3)
            for afile in filelist:
                (head, filename) = os.path.split(afile)
                print(filename)
                stdin, stdout, stderr = ssh.exec_command('cat ' + afile)
                r2 = stdout.read()

            if "Ping Test: Pass" in (str(r2)):
                b += 1

            if "TCP 80 Test: Pass" in (str(r2)):
                b += 1

            if "TCP 21 Test: Pass" in (str(r2)):
                b += 1

            if "TCP 110 Test: Pass" in (str(r2)):
                b += 1

            if "TCP 25 Test: Pass" in (str(r2)):
                b += 1

            if "UDP 666 Test: Pass" in (str(r2)):
                b += 1            

            ssh.close()

            print a
            print b
            if a + b == 12:
                
                self.assertEqual(1,1)
                print ("PASS")
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
            else:
                ssh.close()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case042()

            else:
                self.assertEqual(1,0)


    def test_case043(self):

        "Case_1209 Inbound Access with Additional Public IP Enalbe(Default IP)"
        try:
            a = 0
            Config_File_Upload('hd2hw4_720_test_case043.conf')
            time.sleep(AppWait)
            Bsleep(30)

            ssh.connect('192.168.50.9' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            #print 'Log folder Clear!!'
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            #print 'Python Task Clear!!'
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 80 &> log/T80.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 21 &> log/T21.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 110 &> log/T110.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 25 &> log/T25.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 U 666 &> log/U666.tmp&')
            Bsleep(3)
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            #print 'Log folder Clear!!'
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            #print 'Python Task Clear!!'
            #print 'Test Running Wait...'
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command("echo peplink | sudo -S python PogoU64.py W1 10.88.81.1 60")
            Bsleep(3)
            for std in stdout.readlines():
                print std

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")  
            Bsleep(3)
            apath = 'log'
            apattern ='"*.log"'
            rawcommand = 'find {path} -name {pattern}'
            command = rawcommand.format(path=apath, pattern=apattern)

            stdin, stdout, stderr = ssh.exec_command(command)
            Bsleep(3)
            filelist = stdout.read().splitlines()
            sftp = ssh.open_sftp()
            for afile in filelist:
                (head, filename) = os.path.split(afile)
                print(filename)
                stdin, stdout, stderr = ssh.exec_command('cat ' + afile)
                r1 = stdout.read()

            if "Ping Test: Pass" in (str(r1)):
                a += 1

            if "TCP 80 Test: Pass" in (str(r1)):
                a += 1

            if "TCP 21 Test: Pass" in (str(r1)):
                a += 1

            if "TCP 110 Test: Pass" in (str(r1)):
                a += 1

            if "TCP 25 Test: Pass" in (str(r1)):
                a += 1

            if "UDP 666 Test: Pass" in (str(r1)):
                a += 1            

            ssh.close()
                  
            if a == 6:

                print ("PASS")
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,1)

            else:
                ssh.close()
                #Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case043()

            else:
                self.assertEqual(1,0)


    def test_case044(self):

        "Case_1210 Inbound Access with Additional Public IP Enalbe(Additional IP)"
        try:
            b = 0
            Config_File_Upload('hd2hw4_720_test_case044.conf')
            time.sleep(AppWait)
            Bsleep(30)

            ssh.connect('192.168.50.9' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            #print 'Log folder Clear!!'
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            #print 'Python Task Clear!!'
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 80 &> log/T80.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 21 &> log/T21.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 110 &> log/T110.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 25 &> log/T25.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 U 666 &> log/U666.tmp&')
            Bsleep(3)
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            #print 'Log folder Clear!!'
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            #print 'Python Task Clear!!'
            #print 'Test Running Wait...' 
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command("echo peplink | sudo -S python PogoU64.py W1 10.88.81.51 60")
            Bsleep(3)
            for std in stdout.readlines():
                print std
            Bsleep(3)
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")  
            Bsleep(3)
            apath = 'log'
            apattern ='"*.log"'
            rawcommand = 'find {path} -name {pattern}'
            command = rawcommand.format(path=apath, pattern=apattern)

            stdin, stdout, stderr = ssh.exec_command(command)
            Bsleep(3)
            filelist = stdout.read().splitlines()
            sftp = ssh.open_sftp()
            for afile in filelist:
                (head, filename) = os.path.split(afile)
                print(filename)
                stdin, stdout, stderr = ssh.exec_command('cat ' + afile)
                r2 = stdout.read()

            if "Ping Test: Pass" in (str(r2)):
                b += 1

            if "TCP 80 Test: Pass" in (str(r2)):
                b += 1

            if "TCP 21 Test: Pass" in (str(r2)):
                b += 1

            if "TCP 110 Test: Pass" in (str(r2)):
                b += 1

            if "TCP 25 Test: Pass" in (str(r2)):
                b += 1

            if "UDP 666 Test: Pass" in (str(r2)):
                b += 1
            ssh.close()
            
            if b == 6:

                print ("PASS")
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,1)

            else:
                
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case044()

            else:
                self.assertEqual(1,0)


    def test_case045(self):
          
        "Case_1211-Outbound Policy Custom Outbound Traffic Rules(Auto)"
        try:
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(2)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()
            ssh.connect('10.88.81.254' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S tc qdisc add dev ens21 root netem delay 30ms 10ms loss 0.3')
            time.sleep(10)
            
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            ssh.exec_command("echo peplink | sudo -S nohup python PogoU64.py W2 10000 10.88.81.1 10.88.82.1 10.88.83.1 10.88.84.1 10.88.85.1 10.88.86.1 10.88.87.1 10.88.88.1 &> log/out.tmp&")
            Bsleep(3)
            ssh.connect('192.168.50.9' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L2 10.88.80.11 10000 1000')
            Bsleep(3)
            for std in stdout.readlines():
                r = std,

            ssh.connect('10.88.81.254' , username="peplink" , password="peplink")    
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S tc qdisc del dev ens21 root netem delay 30ms 10ms loss 0.3')
            Bsleep(3)
            ssh.close()

            if "WAN1 1000" in str(r):
                print r
                print 'PASS'
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                #UIRestD()
                #time.sleep(32)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,1)

            else:

                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case045()

            else:
                self.assertEqual(1,0)


    def test_case046(self):

        "Case_1232-Custom Rules Priority Any proto"
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case046.conf')
            time.sleep(AppWait)
            Bsleep(30)

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            ssh.exec_command("echo peplink | sudo -S nohup python PogoU64.py W2 10000 10.88.81.1 10.88.82.1 10.88.83.1 10.88.84.1 10.88.85.1 10.88.86.1 10.88.87.1 10.88.88.1 &> log/out.tmp&")
            Bsleep(3)
            ssh.connect('192.168.50.9' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L2 10.88.80.11 10000 1000')
            Bsleep(3)
            for std in stdout.readlines():
                r = std,
            print r
            ssh.close()

            w1 = re.findall(r'WAN1 (.*?) ',str(r))
            w2 = re.findall(r'WAN2 (.*?) ',str(r))

            if w1[0] >= 830 and w1[0] >= 840:
                print w1[0]
                a += 1

            if w2[0] >= 160 and w2[0] >= 170:
                print w2[0]
                a += 1

            if a ==2 :
                print ("PASS")
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                self.assertEqual(1,1)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
            else:

                #Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
    
            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case046()

            else:
                self.assertEqual(1,0)


    def test_case047(self):

        "Case_1232 - Custom Rules Weighed by MAC address"
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case047.conf')
            time.sleep(AppWait)
            Bsleep(30)


            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            ssh.exec_command("echo peplink | sudo -S nohup python PogoU64.py W2 10000 10.88.81.1 10.88.82.1 10.88.83.1 10.88.84.1 10.88.85.1 10.88.86.1 10.88.87.1 10.88.88.1 &> log/out.tmp&")
            Bsleep(3)
            ssh.connect('192.168.50.9' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L2 10.88.80.11 10000 1000')
            Bsleep(3)
            for std in stdout.readlines():
                r = std,
            print r
            ssh.close()

            r1 = re.findall(r'WAN1 (.*?) |',std)
            r2 = re.findall(r'WAN2 (.*?) |',std)

            print r1[0]
            print r2[10]

            if int(r1[0]) >= 832 and int(r1[0]) <= 834:
                
                a += 1 

            else:
                a += -1

            if int(r2[10]) >= 165 and int(r2[10]) <= 167:
                
                a += 1 

            else:
                a += -1

            if int(r1[0]) + int(r2[10]) == 1000:
                a += 1 

            else:
                a += -1

            if a == 3:
                print 'PASS'
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                self.assertEqual(1,1)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case047()

            else:
                self.assertEqual(1,0)


    def test_case048(self):
          
        "Case_1233-Custom Rules Least Used by Source IP Network"
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case048.conf')
            time.sleep(AppWait)
            Bsleep(30)

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            ssh.exec_command("echo peplink | sudo -S nohup python PogoU64.py W2 10000 10.88.81.1 10.88.82.1 10.88.83.1 10.88.84.1 10.88.85.1 10.88.86.1 10.88.87.1 10.88.88.1 &> log/out.tmp&")
            Bsleep(3)
            ssh.connect('192.168.50.9' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L2 10.88.80.11 10000 1000')
            Bsleep(3)
            for std in stdout.readlines():
                r = std,
            print r
            ssh.close()

            if "WAN1 1000" in str(r):

                #UIRestD()
                #time.sleep(32)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                print 'PASS'
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                self.assertEqual(1,1)
            else:

                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case048()

            else:
                self.assertEqual(1,0)



    def test_case049(self):

        "Case_1405-Outbound Policy Expert Mode"
        try:
            #clear log
            driver = Bopen()
            UIsLogin(pepurl)
            Bsleep(3)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(2)
            BclickT("Clear Log")
            time.sleep(6)
            Bquit()
            time.sleep(3)
            Config_File_Upload('hd2hw4_720_test_case049-1.conf')
            time.sleep(150)
            driver = Bopen()
            UIsLogin(pepurl)
            time.sleep(3)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(5)

            if Btext('connected to To_FH1_Test'):
                ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
                Bsleep(3)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.11')
                Bsleep(3)
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):

                    Config_File_Upload('hd2hw4_720_test_case049-2.conf')
                    time.sleep(30)
                    ssh.connect("192.168.50.9" , username="peplink" , password="peplink")

                    stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.11')
                    Bsleep(3)
                    t = stdout.read()
                    print('t',str(t))
                    ssh.close()

                    if '0 received' in str(t):

                        print ("PASS")
                        #clear log
                        driver = Bopen()
                        UIsLogin(pepurl)
                        Bsleep(3)
                        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                        time.sleep(2)
                        BclickT("Clear Log")
                        time.sleep(2)
                        Bquit()
                        Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                        time.sleep(30)
                        #UIRestD()
                        #time.sleep(32)
                        os.system('nmcli device disconnect ens18')
                        time.sleep(2)
                        os.system('nmcli device connect ens18')
                        time.sleep(5)
                        self.assertEqual(1,1)

                    else:
                        print 'FAIL'
                        #UIRestD()
                        #time.sleep(32)
                        #clear log
                        driver = Bopen()
                        UIsLogin(pepurl)
                        Bsleep(3)
                        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                        time.sleep(2)
                        BclickT("Clear Log")
                        time.sleep(2)
                        Bquit()
                        Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                        time.sleep(30)
                        os.system('nmcli device disconnect ens18')
                        time.sleep(2)
                        os.system('nmcli device connect ens18')
                        time.sleep(5)
                        self.assertEqual(1,0)
                else:
                    print 'FAIL'
                    #UIRestD()
                    #time.sleep(32)
                    #clear log
                    driver = Bopen()
                    UIsLogin(pepurl)
                    Bsleep(3)
                    Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                    time.sleep(2)
                    BclickT("Clear Log")
                    time.sleep(2)
                    Bquit()
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    time.sleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,0)
                    
            else:
                print 'FAIL'
                print 'cannot find log'
                #UIRestD()
                #time.sleep(32)
                #clear log
                driver = Bopen()
                UIsLogin(pepurl)
                Bsleep(3)
                Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                time.sleep(2)
                BclickT("Clear Log")
                time.sleep(2)
                Bquit()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case049()

            else:
                self.assertEqual(1,0)


    def test_case050(self):

        "Out Bound Policy By Domain"

        try:
            Config_File_Upload('hd2hw4_720_test_case050.conf')
            time.sleep(AppWait)
            Bsleep(30)

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            ssh.exec_command("echo peplink | sudo -S nohup python PogoU64.py W2 10000 10.88.81.1 10.88.82.1 10.88.83.1 10.88.84.1 10.88.85.1 10.88.86.1 10.88.87.1 10.88.88.1 &> log/out.tmp&")
            Bsleep(3)
            ssh.connect('192.168.50.9' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L2 lo.pepttc.com 10000 1000')
            Bsleep(3)
            for std in stdout.readlines():
                r = std,
            print r
            ssh.close()
            Bquit()

            if "WAN2 1000" in str(r):
                print 'PASS'
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,1)

            else:

                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case050()

            else:
                self.assertEqual(1,0)

    def test_case051(self):

        "Case_1090 Multiple Static route"

        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case051.conf')
            time.sleep(AppWait)
            Bsleep(30)
            
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.201')
            Bsleep(3)
            t = stdout.read()
            print('t',str(t))
            ssh.close()

            if '4 received' in str(t):
                
                a += 1
                ssh.close()

            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.3.201')
            Bsleep(3)
            t = stdout.read()
            print('t',str(t))
            ssh.close()

            if '4 received' in str(t):
                
                a += 1
                ssh.close()

            if a == 2:

                self.assertEqual(1,1)
                print 'PASS'
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
            else:
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)
            
        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case051()

            else:
                self.assertEqual(1,0)


                
    def test_case052(self):

        "Case_2204 OSPF authencation None"
        try:
            ssh.connect('192.168.50.201' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup cp /etc/quagga/ospfd.conf.none /etc/quagga/ospfd.conf')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup /etc/init.d/quagga restart')
            Bsleep(10) 
            ssh.close()
            #set OSPF 
            Config_File_Upload('hd2hw4_720_test_case052.conf')
            time.sleep(AppWait)
            Bsleep(30)
            
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospfstatus')
            result = driver.page_source
            print driver.page_source
            Bquit()

            if '192.168.2.0/24 192.168.3.0/24' in result:
                
                ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
                Bsleep(3)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.201')
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):
                    print 'PASS'
                    self.assertEqual(1,1)
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                else:

                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,0)

            else:

                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case052()

            else:
                self.assertEqual(1,0)


    def test_case053(self):

        "Case_2205 OSPF authencation Text"
        try:
            ssh.connect('192.168.50.201' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup cp /etc/quagga/ospfd.conf.text /etc/quagga/ospfd.conf')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup /etc/init.d/quagga restart')
            Bsleep(10) 
            ssh.close()
            
            Config_File_Upload('hd2hw4_720_test_case053.conf')
            time.sleep(AppWait)
            Bsleep(30)
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospfstatus')
            result = driver.page_source
            print driver.page_source
            Bquit()

            if '192.168.2.0/24 192.168.3.0/24' in result:
                
                ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
                time.sleep(3)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.201')
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):
                    
                    print "PASS"
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                else:

                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,0)

            else:

                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case053()

            else:
                self.assertEqual(1,0)


    def test_case054(self):

        "Case_2206 OSPF authencation MD5"
        try:
            ssh.connect('192.168.50.201' , username="peplink" , password="peplink")
            time.sleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup cp /etc/quagga/ospfd.conf.md5 /etc/quagga/ospfd.conf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S nohup /etc/init.d/quagga restart')
            time.sleep(10) 
            ssh.close()
            Config_File_Upload('hd2hw4_720_test_case054.conf')
            time.sleep(AppWait)
            Bsleep(30)
            
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospfstatus')
            result = driver.page_source
            print driver.page_source
            Bquit()

            if '192.168.2.0/24 192.168.3.0/24' in result:
                
                ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
                time.sleep(3)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.201')
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):

                    self.assertEqual(1,1)
                    print 'PASS'
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                else:
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,0)

            else:
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case054()

            else:
                self.assertEqual(1,0)


    def test_case055(self):

        "Case_2043 RIPv2 authencation None"
        try:
            ssh.connect('192.168.50.201' , username="peplink" , password="peplink")
            time.sleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup cp /etc/quagga/ripd.conf.none /etc/quagga/ripd.conf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S nohup /etc/init.d/quagga restart')
            time.sleep(10)
            ssh.close()
            Config_File_Upload('hd2hw4_720_test_case055.conf')
            time.sleep(AppWait)
            Bsleep(30)

            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospfstatus')
            result = driver.page_source
            print driver.page_source
            Bquit()

            if '192.168.2.0/24 192.168.3.0/24' in result:
                
                ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
                time.sleep(3)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.201')
                Bsleep(3)
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):
                    
                    self.assertEqual(1,1)
                    print 'PASS'
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                else:

                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,0)

            else:

                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)
 
        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case055()

            else:
                self.assertEqual(1,0)


    def test_case056(self):

        "Case_2044 RIPv2 authencation Text"
        try:
            ssh.connect('192.168.50.201' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup cp /etc/quagga/ripd.conf.text /etc/quagga/ripd.conf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S nohup /etc/init.d/quagga restart')
            time.sleep(10) 
            ssh.close()
            Config_File_Upload('hd2hw4_720_test_case056.conf')
            time.sleep(AppWait)
            Bsleep(30)
            
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospfstatus')
            result = driver.page_source
            print driver.page_source
            Bquit()

            if '192.168.2.0/24 192.168.3.0/24' in result:
                
                ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
                Bsleep(3)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.201')
                Bsleep(3)
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):
                    
                    self.assertEqual(1,1)
                    print 'PASS'
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                else:
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,0)
            else:

                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case056()

            else:
                self.assertEqual(1,0)
           

    
    def test_case057(self):

        "Case_2045 RIPv2 authencation MD5"
        try:
            ssh.connect('192.168.50.201' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup cp /etc/quagga/ripd.conf.md5 /etc/quagga/ripd.conf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S nohup /etc/init.d/quagga restart')
            time.sleep(10)
            ssh.close()
            Config_File_Upload('hd2hw4_720_test_case057.conf')
            time.sleep(AppWait)
            Bsleep(30)
            
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospfstatus')
            Bsleep(5)
            result = driver.page_source
            print driver.page_source
            Bquit()

            if '192.168.2.0/24 192.168.3.0/24' in result:
                
                ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
                Bsleep(3)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.201')
                Bsleep(3)
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):
                    print 'PASS'
                    self.assertEqual(1,1)
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                else:
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,0)

            else:
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                 Bquit()
                
            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case057()

            else:
                self.assertEqual(1,0)


    def test_case058(self):

        "Case_1749-IPSec VPN-Mode-Main,Aggressive Mode"

        try:
            Config_File_Upload('hd2hw4_720_test_case058.conf')
            time.sleep(AppWait)
            Bsleep(30)
            
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.11')
            Bsleep(3)
            t = stdout.read()
            print('t',str(t))
            ssh.close()

            if '4 received' in str(t):

                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                self.assertEqual(1,1)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case058()

            else:
                self.assertEqual(1,0)


    def test_case059(self):

        "Case_1410-IPSec VPN-Preshared key Authencation"

        try:
            Config_File_Upload('hd2hw4_720_test_case059.conf')
            time.sleep(AppWait)
            Bsleep(30)
            
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.11')
            Bsleep(3)
            t = stdout.read()
            print('t',str(t))
            ssh.close()

            if '4 received' in str(t):

                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                self.assertEqual(1,1)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case059()

            else:
                self.assertEqual(1,0)

    
    def test_case060(self):

        "Case_1761-IPSec VPN-Event Log"
        try:
            Config_File_Upload('hd2hw4_720_test_case060.conf')
            time.sleep(AppWait)
            Bsleep(30)
            
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog#ipsec_log')
            time.sleep(5)
            if Btext('IPsec: toFusionHubIPSec/1x1 - Connected'):
                print ("PASS")
                Bquit()
                #UIRestD
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,1)
            else:
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case060()

            else:
                self.assertEqual(1,0)

    def test_case061(self):

        "Case_1762-Status -> IPSec VPN"
        try:
            Config_File_Upload('hd2hw4_720_test_case061.conf')
            Bsleep(5)
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=ipsecstatus')
            time.sleep(5)
            if Btext('192.168.50.0/24 &lt;-&gt; 192.168.2.0/24'):

                print ("PASS")
                Bquit()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                self.assertEqual(1,1)

            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(5)

            if count <3:
                count+=1
                self.test_case061()

            else:
                self.assertEqual(1,0)


    def test_case062(self):

        "Case_1767-Dashboard IPSec VPN"
        try:
            Config_File_Upload('hd2hw4_720_test_case062.conf')
            Bsleep(5)
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=main')
            time.sleep(5)
            if Btext('toFusionHubIPSec') and Btext('Established'):

                print ("PASS")
                Bquit()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                self.assertEqual(1,1)

            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case062()

            else:
                self.assertEqual(1,0)


    def test_case063(self):

        "Case_1411-IPSec VPN - X.509 Certificate Authencation"

        try:
            UIRestD()
            time.sleep(62)
            
            #Add certificate in certificate manager
            driver = Bopen()
            UIsLogin(pepurl)
            Bsleep(3)
            Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=x509')
            time.sleep(2)
            Bclick ('#mainContent > div.smart_content > table.form_table.sep.cert_mgr > tbody.summary > tr:nth-child(1) > td:nth-child(3) > button.icon.fa.editIcon.edit_action')
            time.sleep(2)
            Bfill('#ui-id-3 > form > table > tbody > tr:nth-child(1) > td:nth-child(2) > textarea', PrivateKey)
            time.sleep(2)
            Bfill('#ui-id-3 > form > table > tbody > tr:nth-child(2) > td:nth-child(2) > textarea', PublicKey)
            time.sleep(2)
            SBclickT('Save and Apply')
            time.sleep(5)
            SBclickT('OK')
            time.sleep(20)
            Bquit()
            
            Config_File_Upload('hd2hw4_720_test_case063.conf')
            Bsleep(60)
            
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.3.11')
            t = stdout.read()
            print('t',str(t))
            ssh.close()

            if '4 received' in str(t):

                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                self.assertEqual(1,1)

            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case063()

            else:
                self.assertEqual(1,0)


    def test_case064(self):

        "Case_1099-SpeedFusion VPN Role endpoint /Hub mode"
        try:
            Config_File_Upload('hd2hw4_720_test_case064.conf')
            Bsleep(120)
            driver = Bopen()
            UIsLogin(pepurl)
            Bsleep(3)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            Bsleep(5)

            if Btext('connected to To_FH1_Test'):
                Bquit()
                time.sleep(5)
                ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.11')
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):

                    print ("PASS")
                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                else:
                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,0)
            else:
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case064()

            else:
                self.assertEqual(1,0)


    def test_case065(self):

        "Case_1100-SpeedFusion Link fail over, Link fail back"
        a = 0
        try:
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            time.sleep(5)
            SF_toLoFH1()
            time.sleep(60)
            WAN1_Disable()
            time.sleep(20)
            UIsApply(pepurl)
            time.sleep(5)
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.11')
            Bsleep(3)
            t = stdout.read()
            print('t',str(t))
            ssh.close()

            if '0 received' in str(t):
                a += 1
            else:
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                self.assertEqual(1,0)

            WAN1_Enable()
            UIsApply(pepurl)
            time.sleep(30)
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.11')
            Bsleep(3)
            t = stdout.read()
            print('t',str(t))
            ssh.close()

            if '4 received' in str(t):
                a += 1
            else:
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

            if a == 2:
                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,1)
            else:
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case065()

            else:
                self.assertEqual(1,0)


    def test_case066(self):

        "Case_1313-SpeedFusion Site-to-Site VPN in hub-and-spoke"
        try:
            Config_File_Upload('hd2hw4_720_test_case066.conf')
            Bsleep(120)
            ssh.connect("192.168.2.11" , username="peplink" , password="peplink")
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.3.11')
            Bsleep(3)
            t = stdout.read()
            print('t',str(t))
            ssh.close()

            if '4 received' in str(t):

                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,1)
            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case066()
            else:
                self.assertEqual(1,0)


    def test_case067(self):

        "Case_1357 - individual Bandwidth Limits - staff"
        global qos
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case067.conf')
            Bsleep(45)
            os.system('ping -c 4 10.88.80.11')
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(6)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            result1 = []
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            Bsleep(6)
            cmd = "echo peplink | sudo -S iperf -c 10.88.80.11 -t60 -P4"
            Bsleep(6)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(6)
            for std in stdout.readlines():
                result1.append(std)

            c = re.findall(r'MBytes(.*?)Mbits/sec',str(result1))
            print 'c[-1] ='
            print (c[-1])

            if float(c[-1]) > 19 and float(c[-1]) < 20:

                a += 1
                ssh.close()

            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(6)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            Bsleep(6)
            result2 = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            Bsleep(6)
            cmd = "echo peplink | sudo -S iperf -c 10.88.81.1 -t60 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(6)
            for std in stdout.readlines():
                result2.append(std)

            s = re.findall(r'MBytes(.*?)Mbits/sec',str(result2))
            print 's[-1] ='
            print (s[-1])

            if float(s[-1]) > 19 and float(s[-1]) < 20:

                a += 1
                ssh.close()

            if a == 2:

                path = "Test_Result/case067_temp.txt"
                txt = open(path,mode="w")
                txt.write("067=pass")
                txt.close()
                self.assertEqual(1,1)
                Bquit()
                #UIRestD()
                #time.sleep(32)
                
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(8)

            else:

                path = "Test_Result/case067_temp.txt"
                txt = open(path,mode="w")
                txt.write("067=fail")
                txt.close()
                self.assertEqual(1,0)
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(8)
                
        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            time.sleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(5)
            
            
            if count <5:
                count+=1
                time.sleep(30)
                self.test_case067()

            else:
                self.assertEqual(1,0)


    def test_case068(self):

        "Case_1358 - individual Bandwidth Limits - Guest"
        global qos
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case068.conf')
            Bsleep(45)
            os.system('ping -c 4 10.88.80.11')
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(3)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            Bsleep(3)
            result1 = []
            os.system('ping -c 4 192.168.50.9')
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            Bsleep(3)
            cmd = "echo peplink | sudo -S iperf -c 10.88.80.11 -t60 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(3)
            for std in stdout.readlines():
                result1.append(std)

            c = re.findall(r'MBytes(.*?)Mbits/sec',str(result1))
            print 'c[-1] = '
            print (c[-1])
            
            if float(c[-1]) > 9 and float(c[-1]) < 11:

                a += 1
                ssh.close()

            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            Bsleep(3)
            result2 = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            Bsleep(3)
            cmd = "echo peplink | sudo -S iperf -c 10.88.81.1 -t60 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(3)
            for std in stdout.readlines():
                result2.append(std)

            s = re.findall(r'MBytes(.*?)Mbits/sec',str(result2))
            print 's[-1] = '
            print (s[-1])

            if float(s[-1]) > 9 and float(s[-1]) < 11:

                a += 1
                ssh.close()

            if a == 2:
                print 'PASS'
                path = "Test_Result/case068_temp.txt"
                txt = open(path,mode="w")
                Bsleep(3)
                txt.write("068=pass")
                Bsleep(3)
                txt.close()
                self.assertEqual(1,1)
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(8)
            else:
                path = "Test_Result/case068_temp.txt"
                txt = open(path,mode="w")
                Bsleep(3)
                txt.write("068=fail")
                Bsleep(3)
                txt.close()
                self.assertEqual(1,0)
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            time.sleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <5:
                count+=1
                time.sleep(30)
                self.test_case068()

            else:
                self.assertEqual(1,0)


    def test_case069(self):

        "Case_1356 - Modify Group Reserved Bandwidth"
        time.sleep(B20Wait)
        r=0
        path = "Test_Result/case067_temp.txt"
        txt1 = open(path,mode="r")
        Bsleep(3)
        a = txt1.read()
        
        if "067=pass" in str(a):
            r += 1
            txt1.close()

        path = "Test_Result/case068_temp.txt"
        txt2 = open(path,mode="r")
        Bsleep(3)
        b = txt2.read()

        if "068=pass" in str(b):
            r += 1
            txt2.close()

        if r == 2:
            self.assertEqual(1,1)

        else:
            self.assertEqual(1,0)


    def test_case070(self):
        "Case_1354 - QOS - Bandwidth disabled- Default"
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case070.conf')
            Bsleep(45)
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            Bsleep(3)
            result1 = []
            os.system('ping -c 4 192.168.50.9')
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            Bsleep(3)
            cmd = "echo peplink | sudo -S iperf -c 10.88.80.11 -t10 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(3)
            for std in stdout.readlines():
                result1.append(std)

            c = re.findall(r'Bytes(.*?)Mbits/sec',str(result1))
            print 'c[-1] = '
            print c[-1]
            if float(c[-1]) > 10:

                a += 1
                ssh.close()

            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(3)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            Bsleep(3)
            result2 = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            Bsleep(3)
            cmd = "echo peplink | sudo -S iperf -c 10.88.81.1 -t10 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(3)
            for std in stdout.readlines():
                result2.append(std)

            s = re.findall(r'Bytes(.*?)Mbits/sec',str(result2))
            print 's[-1] = '
            print s[-1]
            if float(s[-1]) > 60:
                
                a += 1
                ssh.close()

            if a == 2:

                Bquit()
                print 'PASS'
                self.assertEqual(1,1)
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
            else:
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            time.sleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <5:
                count+=1
                time.sleep(30)
                self.test_case070()

            else:
                self.assertEqual(1,0)
                
    def test_case071(self):

        "Case_1354 - QOS - Bandwidth control- enable"

        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case071.conf')
            Bsleep(45)
            os.system('ping -c 4 10.88.80.11')
            time.sleep(2)
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(6)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            Bsleep(6)
            result1 = []
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            cmd = "echo peplink | sudo -S iperf -c 10.88.80.11 -t10 -P4"
            time.sleep(6)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(6)
            for std in stdout.readlines():
                result1.append(std)

            c = re.findall(r'Bytes(.*?)Mbits/sec',str(result1))
            print 'c[-1] ='
            print c[-1]
            if float(c[-1]) > 8 and float(c[-1]) < 10:
                a += 1
                ssh.close()
            
            os.system('ping -c 4 192.168.50.9')
            time.sleep(2)
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(6)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            result2 = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            cmd = "echo peplink | sudo -S iperf -c 10.88.81.1 -t10 -P4"
            time.sleep(6)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            Bsleep(6)
            for std in stdout.readlines():
                result2.append(std)

            s = re.findall(r'Bytes(.*?)Mbits/sec',str(result2))
            print 's[-1] ='
            print s[-1]
            if float(s[-1]) > 11 and float(s[-1]) < 50:
                
                a += 1
                ssh.close()
            print 'a = '
            print a
            if a == 2:
                print 'PASS'
                self.assertEqual(1,1)
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                Bsleep(6)
            else:
                
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)
                
        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            
            if count <5:
                count+=1
                time.sleep(30)
                self.test_case071()

            else:
                self.assertEqual(1,0)
                

    def test_case072(self):

        "Case_1915 LAN VLAN InterVLAN routing option support"

        try:
            # Check Switch telnet port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  #1 Second Timeout
            for i in range(30):
                result = sock.connect_ex(('10.88.1.102',23))
                if result == 0:
                    print 'Switch port 23 OPEN'
                    # add vlan 60
                    tn = telnetlib.Telnet('10.88.1.102')
                    Bsleep(2)
                    tn.read_until("User:")
                    Bsleep(2)
                    tn.write("admin\r\n")
                    Bsleep(2)
                    tn.read_until("Password:")
                    Bsleep(2)
                    tn.write ('\r\n')
                    Bsleep(2)
                    tn.write("enable\r\n")
                    Bsleep(2)        
                    tn.write("config\r\n")
                    Bsleep(2)
                    tn.write("interface 0/"+LAN_PORT+"\r\n")
                    Bsleep(2)
                    tn.write("vlan participation include 60\r\n")
                    Bsleep(2)
                    tn.write("vlan tag 60\r\n")
                    Bsleep(2)
                    tn.write("exit\r\n")
                    Bsleep(2)
                    tn.close
                else:
                    print 'Switch port 23 cannot connect, try again'
                i +=1
            
            Config_File_Upload('hd2hw4_720_test_case072-1.conf')
            Bsleep(30)
            os.system('ping -c 4 192.168.50.9')
            time.sleep(2)
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.60.1')
            result1 = stdout.read()
            print('result1',str(result1))
            ssh.close()

            if '4 received' in str(result1):
                Config_File_Upload('hd2hw4_720_test_case072-2.conf')
                Bsleep(30)
                ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.60.1')
                result2 = stdout.read()
                print('result2',str(result2))
                ssh.close()

                if '0 received' in str(result2):
                    print ('PASSED')
                    self.assertEqual(1,1)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    for i in range(30):
                        result = sock.connect_ex(('10.88.1.102',23))
                        if result == 0:
                            print 'Switch port 23 OPEN'
                            # del vlan 60
                            tn = telnetlib.Telnet('10.88.1.102')
                            Bsleep(2)        
                            tn.read_until("User:")
                            Bsleep(2)
                            tn.write("admin\r\n")
                            Bsleep(2)
                            tn.read_until("Password:")
                            Bsleep(2)
                            tn.write ('\r\n')
                            Bsleep(2)
                            tn.write("enable\r\n")
                            Bsleep(2)
                            tn.write("config\r\n")
                            Bsleep(2)
                            tn.write("interface 0/"+LAN_PORT+"\r\n")
                            Bsleep(2)
                            tn.write("no vlan tagging 60\r\n")
                            Bsleep(2)
                            tn.write("vlan participation auto 60\r\n")
                            Bsleep(2)
                            tn.write("exit\r\n")
                            Bsleep(2)
                            tn.close
                        else:
                            print 'Switch port 23 cannot connect, try again'
                        i +=1
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                else:
                    print ('Failed')
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,0)
            else:
                print ('Failed')
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)
        except:

            global count
            try:
                Bquit()

            except:
                a=0
            for i in range(30):
                result = sock.connect_ex(('10.88.1.102',23))
                if result == 0:
                    print 'Switch port 23 OPEN'
                    # del vlan 60
                    tn = telnetlib.Telnet('10.88.1.102')
                    Bsleep(2)        
                    tn.read_until("User:")
                    Bsleep(2)
                    tn.write("admin\r\n")
                    Bsleep(2)
                    tn.read_until("Password:")
                    Bsleep(2)
                    tn.write ('\r\n')
                    Bsleep(2)
                    tn.write("enable\r\n")
                    Bsleep(2)
                    tn.write("config\r\n")
                    Bsleep(2)
                    tn.write("interface 0/"+LAN_PORT+"\r\n")
                    Bsleep(2)
                    tn.write("no vlan tagging 60\r\n")
                    Bsleep(2)
                    tn.write("vlan participation auto 60\r\n")
                    Bsleep(2)
                    tn.write("exit\r\n")
                    Bsleep(2)
                    tn.close
                else:
                    print 'Switch port 23 cannot connect, try again'
                i +=1
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case072()

            else:
                self.assertEqual(1,0)


    def test_case073(self):

        "Case_1055 Logging - Link Down/Up, Health Check fail Logging"

        try:
            a = 0
            #time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            UIsApply(pepurl)
            #time.sleep(AppWait)
            time.sleep(20)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
            time.sleep(3)
            Bncheck('#enable_display > td:nth-child(2) > input:nth-child(1)')
            time.sleep(2)
            Bclick('.save_action')
            time.sleep(3)
            UIsApply(pepurl)
            time.sleep(26)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
            time.sleep(3)
            Bcheck('#enable_display > td:nth-child(2) > input:nth-child(1)')
            time.sleep(2)
            Bclick('.save_action')
            time.sleep(3)
            UIsApply(pepurl)
            time.sleep(30)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(10)
            if Bwait_text("WAN: WAN 1 disconnected"):
                a += 1

            if Bwait_text("WAN: WAN 1 connected (10.88.81.1)"):
                a += 1

            if Bwait_text("WAN: WAN 1 disconnected (Disabled)"):
                a += 1

            if Bwait_text("WAN: WAN 1 connected (10.88.81.1)"):
                a += 1

            if a == 4:

                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                
            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case073()

            else:
                self.assertEqual(1,0)



    def test_case074(self):

        "Case_1057 Logging - DDNS fail, success logging"

        try:

            a = 0
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            UIsApply(pepurl)
            time.sleep(AppWait)
            time.sleep(2)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/support.cgi')
            time.sleep(2)
            Bclick('#hcfs_panel > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)')
            time.sleep(60)
            Bclick('#hcfs_panel > tr:nth-child(1) > td:nth-child(2) > input:nth-child(2)')
            time.sleep(60)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')

            if Bwait_text("WAN: WAN 1 connected (10.88.81.1)"):
                a += 1

            if Bwait_text("WAN: WAN 1 disconnected (WAN failed DNS test)"):
                a += 1

            if a == 2:
                
                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                
            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case074()

            else:
                self.assertEqual(1,0)


    
    def test_case075(self):

        "Case_1058-Logging - automatic refresh, Clear Log"

        try:

            Config_File_Upload('hd2hw4_720_test_case075.conf')
            Bsleep(30)
            driver = Bopen()
            UIsLogin(pepurl)
            Bsleep(3)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(2)
            BclickT("Clear Log")
            time.sleep(2)

            if not Btext('WAN: WAN 1 connected'):

                ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.80.11')
                t = stdout.read()
                time.sleep(30)
                
                if Btext('Denied CONN=lan'):
                    
                    print ("PASS")
                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,1)

                else:
                    
                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,0)

            else:
            
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)

            if count <3:
                count+=1
                self.test_case075()

            else:
                self.assertEqual(1,0)


    def test_case076(self):

        "Case_1281-Firewall - Firewall rules with space character logging"

        try:
            Config_File_Upload('hd2hw4_720_test_case076.conf')
            Bsleep(30)
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(6)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.80.11')
            t = stdout.read()

            if '4 received' in str(t):
                driver = Bopen()
                UIsLogin(pepurl)
                Bsleep(3)
                Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                time.sleep(2)
                
                if Btext('Allowed CONN'):

                    print ("PASS")
                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)

                else:

                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)

                    self.assertEqual(1,0)

            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case076()

            else:
                self.assertEqual(1,0)


    def test_case077(self):

        "Case_1073-Remote Assistance access from LAN/WAN side w/o password"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            EnableRA()
            Bquit()
            time.sleep(AppWait)
            AddkeytoDevice = RA (SN,'addkeyto')
            time.sleep(5)
            RAtoLocal = RA ('192.168.50.1','/GetHwInfo')
                
            if 'serial number: '+SN in RAtoLocal:

                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                
            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case077()

            else:
                self.assertEqual(1,0)


    def test_case078(self):

        "Case_1074-Remote Assistance access from LAN/WAN side with password"

        try:
            driver = Bopen()
            UIsLogin(pepurl)
            time.sleep(6)
            EnableRA()
            time.sleep(6)
            Bquit()
            time.sleep(15)
            RAtoRemote = RA (SN,'/GetHwInfo')
            print '(RAtoRemote) = '
            print (RAtoRemote)
            if 'serial number: '+SN in RAtoRemote:

                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,1)
                
            else:
                
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(60)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(8)
                
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case078()

            else:
                self.assertEqual(1,0)


    def test_case080(self):

        "Case_1415 Web Blocking - Default Web Blocking (All Users)"

        try:
            Config_File_Upload('hd2hw4_720_test_case080.conf')
            Bsleep(30)
            driver = Bopen()
            driver.delete_all_cookies()
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            Bquit()
            time.sleep(AppWait)

            driver = webdriver.Chrome()
            driver.get('http://www.peplink.com')
            time.sleep(10)
            
            if 'blocked due to content' in str(driver.page_source):
                print ("PASS")
                self.assertEqual(1,1)
                driver.quit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                
            else:
                
                Bquit()
                driver.quit()
                self.assertEqual(1,0)

        except:

            global count
            try:
                driver.quit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case080()

            else:
                self.assertEqual(1,0)

    def test_case081(self):

        "Case_1061 Intrusion Detection and Dos Prevention - Sync Flood Protection"

        try:
            Config_File_Upload('hd2hw4_720_test_case081.conf')
            Bsleep(30)
            a = 0
            driver = Bopen()
            time.sleep(2)
            UIsLogin(pepurl)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            EnableRA()
            Bquit()
            Bsleep(30)
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S hping3 -i u1000 -S 10.88.81.1 -p 10000 -c 1000")
            time.sleep(2)
            ssh.close()
            time.sleep(5)

            AddkeytoDevice = RA (SN,'addkeyto')
            time.sleep(5)
            RAtoLocal = RA ('192.168.50.1','/test_case081')
            time.sleep(5)
            i = re.findall(r'[0-9]+',RAtoLocal)
            print i
            print i[6]
            print i[15]
            print i[23]
            print i[42]
            print i[59]

            if int(i[15]) == 1000:
                a += 1

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S hping3 -i u12500 -S 10.88.81.1 -p 10000 -c 1000")
            time.sleep(2)
            ssh.close()
            time.sleep(2)

            RAtoLocal = RA ('192.168.50.1','/test_case081')
            #print (RAtoLocal)

            i = re.findall(r'[0-9]+',RAtoLocal)
            print i

            print i[6]
            print i[15]
            print i[23]
            print i[42]
            print i[59]

            if int(i[15]) >= 2000:
                a += 1


            if a == 2:

                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                self.assertEqual(1,1)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                
            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                IpAdd = '192.168.50.1'
                
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(5)
            IpAdd = '192.168.50.1'
                
            if count <3:
                count+=1
                self.test_case081()

            else:
                self.assertEqual(1,0)
                
    def test_case082(self):

        "Case_1062 Intrusion Detection and Dos Prevention - Port Scan Protection"

        try:
            a = 0
            Config_File_Upload('hd2hw4_720_test_case082.conf')
            Bsleep(30)
            
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            stdin, stdout, stderr = ssh.exec_command("echo peplink | sudo -S nmap -v -sS -A 10.88.81.1")
            result = []
            for std in stdout.readlines():               
                result.append(std)

            ssh.close()
            print 'result[-9]='
            print result[-9]
            if result[-9] == u'TRACEROUTE (using proto 1/icmp)\n':

                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                self.assertEqual(1,1)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   

            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                IpAdd = '192.168.50.1'
                
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
    
            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case082()

            else:
                self.assertEqual(1,0)

                
    def test_case083(self):

        "Case_1063 Intrusion Detection and Dos Prevention - Ping Flood Protection"

        try:
            Config_File_Upload('hd2hw4_720_test_case083.conf')
            Bsleep(30)
            a = 0
            time.sleep(B20Wait)
            driver = Bopen()
            time.sleep(2)
            UIsLogin(pepurl)
            time.sleep(2)
            EnableRA()
            Bquit()
            Bsleep(30)
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(6)
            ssh.exec_command("echo peplink | sudo -S hping3 -i u1000 10.88.81.1 --icmp -p 10000 -c 1000")
            Bsleep(6)
            ssh.close()
            time.sleep(5)

            AddkeytoDevice = RA (SN,'addkeyto')
            time.sleep(5)

            RAtoLocal = RA ('192.168.50.1','/test_case083')
            print 'RAtoLocal = '
            print (RAtoLocal)

            i = re.findall(r'[0-9]+',RAtoLocal)
            print i
            print i[6]
            print i[7]
            print i[15]
            print i[16]
            if int(i[15]) > 50 and int(i[16]) > 1800:

                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                self.assertEqual(1,1)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                time.sleep(5)
                IpAdd = '192.168.50.1'
                
                self.assertEqual(1,0)


        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(5)
            IpAdd = '192.168.50.1'
            
            if count <3:
                count+=1
                self.test_case083()

            else:
                self.assertEqual(1,0)


    def test_case084(self):

        "Case_1064 Intrusion Detection and Dos Prevention - Intrusion Detection and DoS Prevention ON/OFF"

        try:
            a = 'RAHost:192.168.50.1RAPort:2222iptables-tmangle-nvLIDS_ICMPChainIDS_ICMP(2references)pktsbytestargetprotoptinoutsourcedestination~#'
            a1 = 'RAHost:192.168.50.1RAPort:2222~#iptables-tmangle-nvLIDS_ICMPChainIDS_ICMP(2references)pktsbytestargetprotoptinoutsourcedestination~#'
            a2 = "RAHost:192.168.50.1RAPort:2222BusyBoxv1.12.4(2019-01-0303:28:26HKT)built-inshell(ash)Enter'help'foralistofbuilt-incommands.~#~#iptables-tmangle-nvLIDS_ICMPChainIDS_ICMP(2references)pktsbytestargetprotoptinoutsourcedestination~#"
            a3 = "RAHost:192.168.50.1RAPort:2222BusyBoxv1.12.4"
            a4 = "built-inshell(ash)Enter'help'foralistofbuilt-incommands.~#~#iptables-tmangle-nvLIDS_ICMPChainIDS_ICMP(2references)pktsbytestargetprotoptinoutsourcedestination~#"
            Config_File_Upload('hd2hw4_720_test_case084.conf')
            Bsleep(30)
            driver = Bopen()
            time.sleep(2)
            UIsLogin(pepurl)
            time.sleep(2)
            EnableRA()
            Bquit()
            Bsleep(30)
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            Bsleep(6)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            Bsleep(6)
            ssh.exec_command("echo peplink | sudo -S hping3 -i u1000 10.88.81.1 --icmp -p 10000 -c 1000")
            Bsleep(10)
            ssh.close()

            time.sleep(15)

            AddkeytoDevice = RA (SN,'addkeyto')
            time.sleep(10)

            RAtoLocal = RA ('192.168.50.1','/test_case083')
            Bsleep(10)
            print 'RAtoLocal = '
            print RAtoLocal
            i = re.findall(r'[0-9]+',RAtoLocal)
            print 'Result = '
            print i[6]
            print i[7]
            print i[15]
            print i[16]
            time.sleep(6)
            
            if int(i[15]) > 50 and int(i[16]) > 1800:
                print ' turn on is OK'
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                driver = Bopen()
                time.sleep(2)
                UIsLogin(pepurl)
                time.sleep(2)
                EnableRA()
                Bquit()
                Bsleep(30)
                RAtoLocal = RA ('192.168.50.1','/test_case083')
                x = "".join(RAtoLocal.split())
                #print 'a ='+a
                print 'a3 ='+a3
                print 'a4 ='+a4
                print 'x ='+x
                
                if (a3 in x) and (a4 in x):

                    print ("PASS")
                    print 'Turn off is OK'
                    
                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    self.assertEqual(1,1)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(6)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)

                else:

                    self.assertEqual(1,0)

            else:

                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(6)
            os.system('nmcli device connect ens18')
            time.sleep(5)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(6)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(6)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(8)
            IpAdd = '192.168.50.1'
            
            if count <3:
                count+=1
                self.test_case084()

            else:
                self.assertEqual(1,0)
                

    def test_case085(self):

        "Case-1159-Service Passthrough FTP(Port 21,PAS, PORT)"
        try:
            time.sleep(B20Wait)
            files=[]
            ftp = FTP('10.88.81.254')
            ftp.login(user='peplink',passwd= 'peplink')
            ftp.retrlines('LIST',files.append)
            ftp.close()

            if files[0] == '-rw-rw-r--    1 1000     1000       224125 Dec 15  2015 rp-pppoe-3.12.tar.gz':

                print files[0]
                print 'PASSED'
                self.assertEqual(1,1)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
            else:
                
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0

            if count <3:
                count+=1
                self.test_case085()

            else:
                self.assertEqual(1,0)

    def test_case086(self):

        "Case-1160-Service Passthrough FTP custom port"
        try:
            Config_File_Upload('hd2hw4_720_test_case086.conf')
            Bsleep(30)
            files=[]
            ftp = FTP()
            ftp.connect('10.88.80.11',2121)
            ftp.login(user='peplink',passwd= 'peplink')
            ftp.retrlines('LIST',files.append)
            ftp.close()
            
            print files[0]
            if files[0] == '-rw-rw-r--    1 1000     1000        33895 Oct 13  2017 PogoU64.py':

                print files[0]
                print 'PASSED'
                self.assertEqual(1,1)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                #UIRestD()
                #time.sleep(32)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)   
            else:

                Bquit()
                #UIRestD()
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(5)
            IpAdd = '192.168.50.1'
            
            if count <3:
                count+=1
                self.test_case086()

            else:
                self.assertEqual(1,0)


    def test_case087(self):

        "Case_1161 Service Passthrough - PPTP"

        try:
            Config_File_Upload('hd2hw4_720_test_case087.conf')
            Bsleep(30)


            print 'test start'
            result = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(6)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(6)
            ssh.exec_command("echo peplink | sudo -S pon to10_88_81_1")
            time.sleep(10)
            stdin, stdout, stderr = ssh.exec_command("ifconfig ppp0")
            time.sleep(6)
            ssh.exec_command("echo peplink | sudo -S poff to10_88_81_1")
            time.sleep(6)
            ssh.close()

            for std in stdout.readlines():
                result.append(std)
            print 'str(result[0]) = '+str(result[0])
            if str(result[0]) == u'ppp0      Link encap:Point-to-Point Protocol  \n':
                
                #print 'result[1] = '+result[1]
                print 'compare correct'
                driver = Bopen()
                UIsLogin(pepurl)
                time.sleep(3)
                Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                time.sleep(3)
                if Bwait_text("PPTP: peplink5978/10.88.80.11 connected"):
                #if Bwait_text("PPTP: 192.168.1.10 connected (pptp9)"):
                    print 'pass'
                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    self.assertEqual(1,1)
                    driver = Bopen()
                    UIsLogin(pepurl)
                    Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utconfig')
                    time.sleep(3)
                    #Bclick('#config_panel > form:nth-child(4) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > button:nth-child(1)')
                    Bclick('/html/body/div[5]/table/tbody/tr/td[2]/div[3]/div/div/div/div[2]/button')
                    time.sleep(10)
                    Bquit()
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    #UIRestD()
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    
                else:
                    print 'FAIL'
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    time.sleep(30)
                    self.assertEqual(1,0)

            else:
                print 'FAIL'
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utconfig')
            time.sleep(3)
            Bclick('/html/body/div[5]/table/tbody/tr/td[2]/div[3]/div/div/div/div[2]/button')
            time.sleep(3)
            Bquit()
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)   
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 
            time.sleep(8)
            
            if count <3:
                count+=1
                self.test_case087()

            else:
                self.assertEqual(1,0)

    def test_case088(self):

        "Case_1369 PPTP Server - Listen on Default IP (Local user)"

        try:
            Config_File_Upload('hd2hw4_720_test_case088.conf')
            Bsleep(30)


            print 'test start'
            result = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S pon to10_88_81_1")
            time.sleep(30)
            stdin, stdout, stderr = ssh.exec_command("ifconfig ppp0")
            ssh.exec_command("echo peplink | sudo -S poff to10_88_81_1")
            ssh.close()

            for std in stdout.readlines():
                result.append(std)

            if str(result[0]) == u'ppp0      Link encap:Point-to-Point Protocol  \n':

                print result[1]
                driver = Bopen()
                UIsLogin(pepurl)
                Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                if Bwait_text("PPTP: peplink5978/10.88.80.11 connected"):
                #if Bwait_text("PPTP: 192.168.1.10 connected (pptp9)"):
                    
                    print 'pass'
                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    self.assertEqual(1,1)
                    #Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    UIRestD()
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)   
                    
                else:
                    
                    Bquit()
                    UIRestD()
                    #time.sleep(32)
                    #Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,0)

            else:

                Bquit()
                UIRestD()
                #time.sleep(32)
                #Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:
            
            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()
            #time.sleep(32)
            #Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case088()

            else:
                self.assertEqual(1,0)


    def test_case089(self):

        "Case_1370 PPTP Server - Listen on Addistional public IP Address"

        try:
            Config_File_Upload('hd2hw4_720_test_case089.conf')
            Bsleep(30)

            print 'test start'
            result = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S pon to10_88_81_51")
            time.sleep(30)
            stdin, stdout, stderr = ssh.exec_command("ifconfig ppp0")
            ssh.exec_command("echo peplink | sudo -S poff to10_88_81_51")
            ssh.close()

            for std in stdout.readlines():
                result.append(std)

            if str(result[0]) == u'ppp0      Link encap:Point-to-Point Protocol  \n':

                print result[1]
                driver = Bopen()
                UIsLogin(pepurl)
                Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                if Bwait_text("PPTP: peplink5978/10.88.80.11 connected"):
                #if Bwait_text("PPTP: 192.168.1.10 connected (pptp9)"):

                    print 'pass'
                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    self.assertEqual(1,1)
                    UIRestD()
                    #Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                else:

                    self.assertEqual(1,0)

            else:

                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()
            #time.sleep(32)
            #Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case089()

            else:
                self.assertEqual(1,0)


    def test_case090(self):

        "Case_1173-Service Forwarding - Web Proxy (same port)"
        try:
            Config_File_Upload('hd2hw4_720_test_case090.conf')
            Bsleep(30)

            result1 = []
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            cmd = "echo peplink | sudo -S squidclient -h 10.88.81.254 -p 8080 https://www.peplink.com"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            for std in stdout.readlines():
                result1.append(std)

            result = re.findall(r'<p>(.*?) <a',str(result1[-10]))

            if  result[0] == 'Your cache administrator is':
                
                print ("PASSED")
                ssh.close()
                #UIRestD()
                #time.sleep(32)
                self.assertEqual(1,1)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
            else:
                ssh.close()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case090()

            else:
                self.assertEqual(1,0)
    def test_case091(self):

        "Case_1174-Service Forwarding - Web Proxy (different port)"
        try:
            Config_File_Upload('hd2hw4_720_test_case091.conf')
            Bsleep(30)
            result1 = []
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            cmd = "echo peplink | sudo -S squidclient -h 10.88.81.254 -p 8888 https://www.peplink.com"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            for std in stdout.readlines():
                result1.append(std)

            result = re.findall(r'<p>(.*?) <a',str(result1[-10]))

            if  result[0] == 'Your cache administrator is':
                
                print ("PASSED")
                ssh.close()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,1)
            else:

                ssh.close()
                #UIRestD()
                #time.sleep(32)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case091()

            else:
                self.assertEqual(1,0)


    def test_case092(self):

        "Case_1174-Service Forwarding - Disable,Enable"
        try:
            Config_File_Upload('hd2hw4_720_test_case092-1.conf')
            Bsleep(30)
            result1 = []
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            cmd = "echo peplink | sudo -S squidclient -h 10.88.81.254 -p 8888 https://www.peplink.com"
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            for std in stdout.readlines():
                result1.append(std)

            result = re.findall(r'<p>(.*?) <a',str(result1[-10]))

            if  result[0] == 'Your cache administrator is':
                print '1/2 PASS'
                Config_File_Upload('hd2hw4_720_test_case092-2.conf')
                Bsleep(30)
                result2 = []
                ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
                Bsleep(3)
                ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
                Bsleep(3)
                cmd = "echo peplink | sudo -S squidclient -h 10.88.81.254 -p 8888 https://www.peplink.com"
                stdin, stdout, stderr = ssh.exec_command(cmd)
                for std in stdout.readlines():
                    result1.append(std)

                result = re.findall(r'<p>(.*?) <a',str(result2))

                if result == []:

                    print ("2/2 PASS")
                    ssh.close()
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,1)
                else:

                    ssh.close()
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,0) 

            else:

                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            ssh.close()
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case092()

            else:
                self.assertEqual(1,0)


    def test_case094(self):

        "Case_1148 Email Notification Send Notification Email when HC faill, Link Down/UP,Disconnect/Connection manually"

        try:
            Config_File_Upload('hd2hw4_720_test_case094.conf')
            Bsleep(30)
            a = 0
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            time.sleep(2)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            Bvisit("http://192.168.50.1/cgi-bin/MANGA/support.cgi")
            Bclick('#hcfs_panel > tr:nth-child(1) > td.tablecontent2 > input[type="button"]:nth-child(1)')
            time.sleep(60)
            Bclick('#hcfs_panel > tr:nth-child(1) > td.tablecontent2 > input[type="button"]:nth-child(2)')
            time.sleep(60)
            #Bvisit("http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=main")
            Bvisit("http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1")
            time.sleep(2)
            #BclickT("Disconnect","2")
            Bncheck("#enable_display > td:nth-child(2) > input:nth-child(1)")
            time.sleep(2)
            #BclickT("OK")
            Bclick('.save_action')
            time.sleep(3)
            UIsApply(pepurl)
            time.sleep(60)
            Bvisit("http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1")
            #BclickT("Connect","2")
            Bcheck("#enable_display > td:nth-child(2) > input:nth-child(1)")
            Bclick('.save_action')
            time.sleep(3)
            UIsApply(pepurl)
            time.sleep(60)
            Bquit()

            tn = telnetlib.Telnet(HOST)
            time.sleep(2)
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)        
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("shutdown\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            time.sleep(2)
            tn.close
            time.sleep(30)
            tn = telnetlib.Telnet(HOST)
            time.sleep(2)
            tn.read_until("User:")
            time.sleep(2)
            tn.write("admin\r\n")
            time.sleep(2)
            tn.read_until("Password:")
            time.sleep(2)
            tn.write ('\r\n')
            time.sleep(2)
            tn.write("enable\r\n")
            time.sleep(2)        
            tn.write("config\r\n")
            time.sleep(2)
            tn.write("interface 0/"+PORT+"\r\n")
            time.sleep(2)
            tn.write("no shutdown\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            time.sleep(2)
            tn.close
          
            time.sleep(30)
            localtime4 = time.asctime(time.localtime(time.time()))
            time.sleep(60)

            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            time.sleep(1)
            mail.login('andersonw.peplink@gmail.com', 'andersonw751')
            time.sleep(1)
            mail.list()
            time.sleep(1)
            mail.select("inbox")
            time.sleep(1)
            result, data = mail.search(None, "ALL")
            ids = data[0]
            print 'ids = '+ids
            time.sleep(1)
            id_list = ids.split()
            
            latest_email_id = id_list[-6]
            result, data = mail.fetch(latest_email_id, "(RFC822)")
            print 'result = '+result
            #print 'data = '+data
            raw_email1 = data[0][1]
            print 'raw_email1 = '+raw_email1
            
            if "WAN 1: Disconnected (Health check failed)" in raw_email1 and SN +" running "+ FWver in raw_email1:

                a += 1

            latest_email_id = id_list[-4]
            result, data = mail.fetch(latest_email_id, "(RFC822)")
            raw_email2 = data[0][1]
            print 'raw_email2 = '+raw_email2
            
            if "WAN 1: Disconnected" in raw_email2 and SN +" running "+ FWver in raw_email2:

                a += 1

            latest_email_id = id_list[-3]
            result, data = mail.fetch(latest_email_id, "(RFC822)")
            raw_email3 = data[0][1]

            if "WAN 1: Connected" in raw_email3 and SN +" running "+ FWver in raw_email3:

                a += 1

            latest_email_id = id_list[-2]
            result, data = mail.fetch(latest_email_id, "(RFC822)")
            raw_email4 = data[0][1]

            if "WAN 1: Disconnected" in raw_email4 and SN +" running "+ FWver in raw_email4:

                a += 1

            print str(a) +"=============================================="
            if a == 4:

                print "PASSED"
                Bquit()
                
                #search and delete email
                # select which mail box to process
                mail.select("Inbox") 
                resp, data = mail.uid('search',None, "BODY", SN) # search and return Uids
                uids = data[0].split()    
                mailparser = HeaderParser()
                for uid in uids:
                    resp,data = mail.uid('fetch',uid,"(BODY[HEADER])")        
                    msg = mailparser.parsestr(data[0][1])       
                    print (msg['From'],msg['Date'],msg['Subject'])        
                    print mail.uid('STORE',uid, '+X-GM-LABELS', '(\\Trash)')
                print mail.expunge()
                mail.close() # close the mailbox
                mail.logout() # logout 
                Bsleep(5)
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,1)
            else:

                print "Failed"
                Bquit()
                #search and delete email
                # select which mail box to process
                mail.select("Inbox") 
                resp, data = mail.uid('search',None, "BODY", SN) # search and return Uids
                uids = data[0].split()    
                mailparser = HeaderParser()
                for uid in uids:
                    resp,data = mail.uid('fetch',uid,"(BODY[HEADER])")        
                    msg = mailparser.parsestr(data[0][1])       
                    print (msg['From'],msg['Date'],msg['Subject'])        
                    print mail.uid('STORE',uid, '+X-GM-LABELS', '(\\Trash)')
                print mail.expunge()
                mail.close() # close the mailbox
                mail.logout() # logout
                Bsleep(5)
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)


        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case094()

            else:
                self.assertEqual(1,0)


    def test_case096(self):

        "Case_1351 Email Notification - Multiple Email Recepient"
        try:
            Config_File_Upload('hd2hw4_720_test_case096.conf')
            Bsleep(30)
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            time.sleep(2)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP = UIStart(pepurl,driver)
            time.sleep(AppWait)
            Bvisit("http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utnotify")
            time.sleep(2)
            BclickT("Test Email Notification")
            time.sleep(2)
            BclickT("Send Test Notification")
            time.sleep(30)

            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            time.sleep(1)
            mail.login('lopeplink@gmail.com', 'peplink5978')
            time.sleep(1)
            mail.list()
            time.sleep(1)
            mail.select("inbox")
            time.sleep(1)
            result, data = mail.search(None, "ALL")
            ids = data[0]
            id_list = ids.split()

            latest_email_id = id_list[-1]
            result, data = mail.fetch(latest_email_id, "(RFC822)")
            raw_email = data[0][1]

            if "andersonw@peplink.com" in raw_email and "lopeplink@gmail.com" in raw_email and SN +" running "+ FWver in raw_email:

                print "PASS"
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                
            else:

                print "Failed"
                Bquit()
                
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case096()

            else:
                self.assertEqual(1,0)


    def test_case105(self):

        "Case_1049 Support Page Network Capture"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit("http://192.168.50.1/cgi-bin/MANGA/support.cgi")
            time.sleep(10)
            Bclick("//body/div/div[3]/li[5]/div[1]/input[2]")
            time.sleep(30)
            cmd = 'echo DNS Nslookup'

            for x in range(5):

                subprocess.Popen(cmd, shell=True)
                subprocess.call('nslookup wiki.peplink.com', shell=True)
                time.sleep(2)
                print 'nslookup wiki.peplink.com for '+ str(x)
                x =+ 1
                time.sleep(5)

            time.sleep(5)
            Bclick("//body/div/div[3]/li[5]/div[1]/input[3]")
            time.sleep(20)
            Bclick("Download")
            time.sleep(20)
            pyautogui.hotkey('Alt', 's')
            time.sleep(1)
            pyautogui.press('return')
            time.sleep(10)
            Bquit()

            os.chdir('/home/peplink/Downloads/')
            files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
            newest = files[-1]
            tar = tarfile.open("/home/peplink/Downloads/" + newest)
            tar.extractall("/home/peplink/Downloads/")
            time.sleep(10)

            WAN1_logs = []
            i = 1
            while i <=1:
                try:
                    testcap = open('/home/peplink/Downloads/network_dump/wan1.pcap', 'rb')
                    packets = rdpcap(testcap)
                    testcap.close()
                    domain = 'wiki.peplink.com'
                    print "DNS query wiki.peplink.com from WAN1 :"
                    WAN1_logs = []
                    for packet in packets:

                        if packet.haslayer(DNSQR):
                            query = packet[DNSQR].qname
                            qtype = packet[DNSQR].qtype
                            if (domain in query) and (qtype == 1) :
                                    print "WAN1 count =",i
                                    WAN1_logs.append(packet.summary())
                                    print query
                                    i+=1

                    i+=1

                except:
                    break

            result = str(WAN1_logs).count("10.8.55.99")
            print 'Result = ' + str(result) 
            if  int(result) >= 4:

                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,1)
            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case105()

            else:
                self.assertEqual(1,0)


    def test_case106(self):

        "Case_1119 DNS Proxy DNS Caching"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit("http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan")
            Bclick('#mainContent > div.smart_content > form > div.general_settings_panel > table.form_table.dns_panel > tbody.dns_general_panel > tr:nth-child(2) > td:nth-child(2) > input[type="checkbox"]')
            BclickT("Save")
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bvisit("http://192.168.50.1/cgi-bin/MANGA/support.cgi")
            time.sleep(10)
            Bclick("//body/div/div[3]/li[5]/div[1]/input[2]")
            time.sleep(30)

            cmd = 'echo DNS Nslookup'

            for x in range(5):

                subprocess.Popen(cmd, shell=True)
                subprocess.call('nslookup wiki.peplink.com', shell=True)
                print 'nslookup wiki.peplink.com for '+ str(x)
                x =+ 1
                time.sleep(5)

            time.sleep(5)
            Bclick("//body/div/div[3]/li[5]/div[1]/input[3]")
            time.sleep(20)
            Bclick("Download")
            time.sleep(10)
            pyautogui.hotkey('Alt', 's')
            time.sleep(1)
            pyautogui.press('return')
            time.sleep(10)
            Bquit()

            os.chdir('/home/peplink/Downloads/')
            files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
            newest = files[-1]
            tar = tarfile.open("/home/peplink/Downloads/" + newest)
            tar.extractall("/home/peplink/Downloads/")
            tar.close()
            time.sleep(10)

            WAN1_logs = []
            i = 1
            while i <=1:
                try:
                    testcap = open('/home/peplink/Downloads/network_dump/wan1.pcap', 'rb')
                    packets = rdpcap(testcap)
                    domain = 'wiki.peplink.com'
                    print "DNS query wiki.peplink.com from WAN1 :"
                    WAN1_logs = []
                    for packet in packets:

                        if packet.haslayer(DNSQR):
                            query = packet[DNSQR].qname
                            qtype = packet[DNSQR].qtype
                            if (domain in query) and (qtype == 1) :
                                print "WAN1 count =",i
                                WAN1_logs.append(packet.summary())
                                print query
                                i+=1

                    i+=1

                except:
                    break
                    
            testcap.close()
            result = str(WAN1_logs).count("10.8.55.99")
            print 'Result = ' + str(result) 
            if  int(result) >= 1:

                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,1)
            else:

                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_test_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case106()

            else:
                self.assertEqual(1,0)


    def test_case107(self):

        "Case_1826 Captive Portal Open Access"

        try:
            Config_File_Upload('hd2hw4_720_test_case107.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            driver = Bopen()
            time.sleep(2)
            Bvisit("https://www.peplink.com")
            Bsleep(5)
            BclickT("Agree")
            Bsleep(5)
            result = re.findall(r'def_content = "(.+)"',driver.page_source)
            print result[0]
            Bsleep(5)
            if "Continue Browsing" == str(result[0]):

                print "PASSED"
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,1)
            else:

                print "Failed"
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case107()

            else:
                self.assertEqual(1,0)


    def test_case109(self):

        "Case_1907 Captive Portal with Walled garden support"

        try:
            Config_File_Upload('hd2hw4_720_test_case109.conf')
            Bsleep(30)

            driver = Bopen()
            Bvisit("https://www.google.com")
            Bsleep(5)
            print driver.page_source
            if "Agree" in str(driver.page_source):
                Bquit()
                driver = Bopen()
                time.sleep(2)
                Bvisit("https://www.peplink.com")
                Bsleep(5)
                result = re.findall(r'<title>(.+)</title>',driver.page_source)
                print result[0]

                if "Peplink SD-WAN. Protecting Business Continuity." == str(result[0]):

                    print "PASSED"
                    Bquit()
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,1)
                else:

                    print "Failed"
                    Bquit()
                    #UIRestD()
                    
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,0)

            else:

                print "Failed"
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case109()

            else:
                self.assertEqual(1,0)

    def test_case110(self):

        "Case_1089 Drop-in Mode Static route"
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case110.conf')
            time.sleep(30)
            os.system('nmcli connection add con-name "di-static-ens18" ifname ens18 type ethernet ip4 10.88.81.11/24 gw4 10.88.81.254')
            time.sleep(2)
            os.system('nmcli connection mod "di-static-ens18" ipv4.dns "10.88.3.1 168.95.1.1"')
            time.sleep(2)
            os.system('nmcli connection up "di-static-ens18"')
            time.sleep(5)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            os.system('ping -c 4 10.88.81.202')
            #os.system('ping -c 10 192.168.2.202')
            #os.system('ping -c 10 192.168.3.202')
            
            result1 = subprocess.check_output("ping -c 4 192.168.2.202; exit 0", stderr=subprocess.STDOUT, shell=True)
            time.sleep(3)
            print 'result1 = '
            print result1
            if '4 received' in result1:
                a += 1
                print 'PASS 1/2'
            else:
                print 'FAIL 1/2'
            Bsleep(5)
            print 'a = '
            print a
            result2 = subprocess.check_output("ping -c 4 192.168.3.202; exit 0", stderr=subprocess.STDOUT, shell=True)
            print 'result2 = '
            print result2
            if '4 received' in result2:
                a += 1
                print 'PASS 2/2'
            else:
                print 'FAIL 2/2'
            print 'a = '
            print a
            if a == 2:
                print 'ALL PASS'
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(8)
                self.assertEqual(1,1)

            else:
                print 'FAIL'
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(8)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')
            time.sleep(8)

            if count <3:
                count+=1
                self.test_case110()

            else:
                self.assertEqual(1,0)
    

                
    def test_case111(self):

        "Case_1136 Drop-In Mode Outbound Access"

        try:
            Config_File_Upload('hd2hw4_720_test_case111.conf')
            Bsleep(30)
            os.system('nmcli connection add con-name "di-static-ens18" ifname ens18 type ethernet ip4 10.88.81.11/24 gw4 10.88.81.254')
            time.sleep(2)
            os.system('nmcli connection mod "di-static-ens18" ipv4.dns "10.88.3.1 168.95.1.1"')
            time.sleep(2)
            os.system('nmcli connection up "di-static-ens18"')
            time.sleep(5)
            driver = Bopen()
            time.sleep(2)
            Bvisit("https://www.peplink.com")
            Bsleep(5)
            result = re.findall(r'<title>(.+)</title>',driver.page_source)
            print result[0]

            if "Peplink SD-WAN. Protecting Business Continuity." == str(result[0]):

                print "PASSED"
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(5)
                self.assertEqual(1,1)
            else:

                print "Failed"
                Bquit()
                #UIRestD()
                
                #time.sleep(32)
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            
            #time.sleep(32)
            Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case111()

            else:
                self.assertEqual(1,0)

    def test_case112(self):

        "Case_1137 Drop-in Mode Inbound Access via WAN1"
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case112.conf')
            time.sleep(30)
            os.system('nmcli connection add con-name "di-static-ens18" ifname ens18 type ethernet ip4 10.88.81.11/24 gw4 10.88.81.254')
            time.sleep(2)
            os.system('nmcli connection mod "di-static-ens18" ipv4.dns "10.88.3.1 168.95.1.1"')
            time.sleep(2)
            os.system('nmcli connection up "di-static-ens18"')
            time.sleep(5)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            ssh.connect('10.88.81.8' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            #print 'Log folder Clear!!'
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            #print 'Python Task Clear!!'
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 80 &> log/T80.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 21 &> log/T21.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 110 &> log/T110.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 T 25 &> log/T25.tmp&')
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L1 U 666 &> log/U666.tmp&')
            Bsleep(3)
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            #print 'Log folder Clear!!'
            Bsleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            #print 'Python Task Clear!!'
            #print 'Test Running Wait...'
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command("echo peplink | sudo -S python PogoU64.py W1 10.88.81.8 60")
            Bsleep(3)
            for std in stdout.readlines():
                print std

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")  
            Bsleep(3)
            apath = 'log'
            apattern ='"*.log"'
            rawcommand = 'find {path} -name {pattern}'
            command = rawcommand.format(path=apath, pattern=apattern)

            stdin, stdout, stderr = ssh.exec_command(command)
            Bsleep(3)
            filelist = stdout.read().splitlines()
            sftp = ssh.open_sftp()
            for afile in filelist:
                (head, filename) = os.path.split(afile)
                print(filename)
                stdin, stdout, stderr = ssh.exec_command('cat ' + afile)
                r1 = stdout.read()

            if "Ping Test: Pass" in (str(r1)):
                a += 1

            if "TCP 80 Test: Pass" in (str(r1)):
                a += 1

            if "TCP 21 Test: Pass" in (str(r1)):
                a += 1

            if "TCP 110 Test: Pass" in (str(r1)):
                a += 1

            if "TCP 25 Test: Pass" in (str(r1)):
                a += 1

            if "UDP 666 Test: Pass" in (str(r1)):
                a += 1            

            ssh.close()
                  
            if a == 6:

                print ("PASS")
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(8)
                self.assertEqual(1,1)

            else:
                ssh.close()
                #Bquit()
                #UIRestD()
                #time.sleep(32)
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(8)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            time.sleep(30)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')
            time.sleep(8)
            if count <3:
                count+=1
                self.test_case112()

            else:
                self.assertEqual(1,0)


    def test_case113(self):

        "Case_1138 Drop-In Mode ICMP reply from Drop-in interface IP Address, LAN side client IP Address"
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case113.conf')
            Bsleep(30)
            os.system('nmcli connection add con-name "di-static-ens18" ifname ens18 type ethernet ip4 10.88.81.11/24 gw4 10.88.81.254')
            time.sleep(2)
            os.system('nmcli connection mod "di-static-ens18" ipv4.dns "10.88.3.1 168.95.1.1"')
            time.sleep(2)
            os.system('nmcli connection up "di-static-ens18"')
            time.sleep(5)
            
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.81.1')
            t1 = stdout.read()
            ssh.close()
            print('t1',str(t1))
            if '4 received' in str(t1):
                print 'PASS 1/2'
                a += 1
            
            print 'a = '
            print a
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.81.11')
            t2 = stdout.read()
            print('t2',str(t2))
            if '4 received' in str(t2):
                print 'PASS 2/2'
                a += 1
            
            print 'a = '
            print a
            if a == 2:
                
                print ("ALL PASS")
                ssh.close()
                self.assertEqual(1,1)
                #UIRestD()
                #time.sleep(32)
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(5)
            else:
                print 'FAIL'
                Bquit()
                print (a)
                #UIRestD()
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(5)
                self.assertEqual(1,0)
            
        except:

            global count
            try:
                ssh.close()

            except:
                a=0
            #UIRestD()
            
            #time.sleep(32)
            Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case113()

            else:
                self.assertEqual(1,0)

    def test_case114(self):

        "Case_1139 Drop-In Mode Additional Public IP"
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case114.conf')
            Bsleep(30)
            os.system('nmcli connection add con-name "di-static-ens18" ifname ens18 type ethernet ip4 10.88.81.11/24 gw4 10.88.81.254')
            time.sleep(2)
            os.system('nmcli connection mod "di-static-ens18" ipv4.dns "10.88.3.1 168.95.1.1"')
            time.sleep(2)
            os.system('nmcli connection up "di-static-ens18"')
            time.sleep(5)
            
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.81.2')
            t = stdout.read()
            ssh.close()
            print('t',str(t))
            if '4 received' in str(t):
                print 'PASS'
                self.assertEqual(1,1)
                #UIRestD()
                #time.sleep(32)
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(5)
            else:
                print 'FAIL'
                Bquit()
                print (a)
                #UIRestD()
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(5)
                self.assertEqual(1,0)
            
        except:

            global count
            try:
                ssh.close()

            except:
                a=0
            #UIRestD()
            
            #time.sleep(32)
            Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case114()

            else:
                self.assertEqual(1,0)

    def test_case115(self):

        "Case_1143 Drop-In Mode Hosts on WAN segment"
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case115.conf')
            Bsleep(30)
            os.system('nmcli connection add con-name "di-static-ens18" ifname ens18 type ethernet ip4 10.88.81.11/24 gw4 10.88.81.254')
            time.sleep(2)
            os.system('nmcli connection mod "di-static-ens18" ipv4.dns "10.88.3.1 168.95.1.1"')
            time.sleep(2)
            os.system('nmcli connection up "di-static-ens18"')
            time.sleep(5)
            
            ssh.connect("10.88.81.8" , username="peplink" , password="peplink")
            Bsleep(3)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.81.52')
            t = stdout.read()
            ssh.close()
            print('t',str(t))
            if '4 received' in str(t):
                print 'PASS'
                self.assertEqual(1,1)
                #UIRestD()
                #time.sleep(32)
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(5)
            else:
                print 'FAIL'
                Bquit()
                #print (a)
                #UIRestD()
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                time.sleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(5)
                self.assertEqual(1,0)
            
        except:

            global count
            try:
                ssh.close()

            except:
                a=0
            #UIRestD()
            
            #time.sleep(32)
            Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case115()

            else:
                self.assertEqual(1,0)


    def test_case116(self):

        "Case_1144 Drop-In Mode Access WAI from WAN side"
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case116.conf')
            Bsleep(30)
            os.system('nmcli connection add con-name "di-static-ens18" ifname ens18 type ethernet ip4 10.88.81.11/24 gw4 10.88.81.254')
            time.sleep(2)
            os.system('nmcli connection mod "di-static-ens18" ipv4.dns "10.88.3.1 168.95.1.1"')
            time.sleep(2)
            os.system('nmcli connection up "di-static-ens18"')
            time.sleep(5)
            os.system('nmcli device disconnect ens18')
            Bsleep(3)
            os.system('nmcli device connect ens19')
            Bsleep(6)
            driver = Bopen()
            Bvisit('http://10.88.81.1/cgi-bin/MANGA/index.cgi')
            Bwait_text('Login')
            Bfill('username', 'admin')
            Bsleep(1)        
            Bfill('password', 'admin')
            Bsleep(1)
            BclickTB('Login')
            Bsleep(10)
            result = re.findall(r'Connected',driver.page_source)
            if result[0] == 'Connected':
                Bquit()
                print "PASS"
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(3)
                #UIRestD()
                #time.sleep(32)
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(5)
                self.assertEqual(1,1)
            else:
                Bquit()
                print "FAIL"
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(3)
                #UIRestD()
                #time.sleep(32)
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(5)
                self.assertEqual(1,0)
        except:

            global count
            try:
                ssh.close()

            except:
                a=0
            #UIRestD()
            
            #time.sleep(32)
            Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')
            time.sleep(5)
            
            if count <3:
                count+=1
                self.test_case116()

            else:
                self.assertEqual(1,0)

    def test_case117(self):

        "Case_1279 Drop-in Mode DNS proxy"
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case117-1.conf')
            time.sleep(30)
            os.system('nmcli connection add con-name "di-static-ens18" ifname ens18 type ethernet ip4 10.88.81.11/24 gw4 10.88.81.254')
            time.sleep(2)
            os.system('nmcli connection mod "di-static-ens18" ipv4.dns "10.88.3.1 168.95.1.1"')
            time.sleep(2)
            os.system('nmcli connection up "di-static-ens18"')
            time.sleep(5)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            
            result1 = subprocess.check_output("dig @10.88.81.1 +noall +answer www.peplink.com", shell=True)
            time.sleep(3)
            print 'result1 = '
            print result1
            if '104.25.106.21' in result1:
                a += 1
            else:
                print 'FAIL 1/2'
            Di_Config_File_Upload('hd2hw4_720_test_case117-2.conf')
            Bsleep(30)
            result2 = []
            result2 = subprocess.check_output("dig @10.88.81.1 +noall +answer www.peplink.com; exit 0", stderr=subprocess.STDOUT, shell=True)
            print 'result2 = '
            print (str(result2))
            if 'no servers could be reached' in str(result2):
                a += 1
            else:
                print 'FAIL 2/2'
            ssh.close()
            print 'a = '
            print a
            if a == 2:
                print 'ALL PASS'
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(8)
                self.assertEqual(1,1)

            else:
                print 'FAIL'
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')
                time.sleep(8)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')
            time.sleep(8)

            if count <3:
                count+=1
                self.test_case117()

            else:
                self.assertEqual(1,0)
    

                
    def test_case118(self):

        "Case_1279 Drop-in(auto MTU)"

        try:
            Config_File_Upload('hd2hw4_720_test_case118.conf')
            time.sleep(30)
            os.system('nmcli connection add con-name "di-static-ens18" ifname ens18 type ethernet ip4 10.88.81.11/24 gw4 10.88.81.254')
            time.sleep(2)
            os.system('nmcli connection mod "di-static-ens18" ipv4.dns "10.88.3.1 168.95.1.1"')
            time.sleep(2)
            os.system('nmcli connection up "di-static-ens18"')
            time.sleep(5)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            
            MTU = 500
            time.sleep(10)
            try:
                while True:

                    runtest = subprocess.check_output('ping -M do -s '+ str(MTU) +' -c 1 10.88.81.254', shell = True)
                    print str(runtest)

                    if 'ms' in str(runtest):
                        MTU += 1
            except:
                print 'MTU = '
                print MTU
                if MTU + 27 == 1440:
                    print 'PASS'
                    Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                    time.sleep(2)
                    os.system('nmcli connection up "dhcp-ens18"')
                    time.sleep(8)
                    print (str(MTU + 27))
                    self.assertEqual(1,1)

                else:

                    print 'FAIL'
                    Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                    time.sleep(2)
                    os.system('nmcli connection up "dhcp-ens18"')
                    time.sleep(8)
                    print (str(MTU + 27))
                    self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')
            time.sleep(8)

            if count <3:
                count+=1
                self.test_case118()

            else:
                self.assertEqual(1,0)

    def test_case119(self):

        "Case_1814 Drop-in Mode Do not Consume IP"
        a = 0
        try:
            Config_File_Upload('hd2hw4_720_test_case119.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            Bsleep(3)
            os.system('nmcli device connect ens19')
            Bsleep(6)
            # login share ip from WAN side
            driver = Bopen()
            Bvisit('http://10.88.81.1/cgi-bin/MANGA/index.cgi')
            Bwait_text('Login')
            Bfill('username', 'admin')
            Bsleep(1)        
            Bfill('password', 'admin')
            Bsleep(1)
            BclickTB('Login')
            Bsleep(15)
            result = re.findall(r'Connected',driver.page_source)
            if result[0] == 'Connected':
                print "PASS 1/2"
                a+=1
            else:
                print "FAIL 1/2"

            Bvisit("http://10.88.81.1/cgi-bin/MANGA/support.cgi")
            time.sleep(15)
            Bclick("//body/div/div[3]/li[5]/div[1]/input[2]")
            time.sleep(30)
            #do a change and apply change to send syslog to 10.88.80.11
            Bvisit("http://10.88.81.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan")
            Bcheck(".dns_general_panel > tr:nth-child(2) > td:nth-child(2) > input:nth-child(1)")
            Bclick('.save_action')
            UIsApply(pepurl)
            time.sleep(20)
            
            Bvisit("http://10.88.81.1/cgi-bin/MANGA/support.cgi")
            time.sleep(15)
            Bclick("#network_capture_panel > div:nth-child(1) > input:nth-child(6)")
            time.sleep(30)
            Bclick("Download")
            time.sleep(20)
            pyautogui.hotkey('Alt', 's')
            time.sleep(10)
            pyautogui.press('return')
            time.sleep(10)
            Bquit()

            os.chdir('/home/peplink/Downloads/')
            files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
            newest = files[-1]
            tar = tarfile.open("/home/peplink/Downloads/" + newest)
            tar.extractall("/home/peplink/Downloads/")
            time.sleep(10)
            #check pcap file - syslog packet from 10.88.81.1 share ip
            testcap = open('/home/peplink/Downloads/network_dump/wan1.pcap', 'rb')
            packets = rdpcap(testcap)
            testcap.close()
            for packet in packets:
                if packet.haslayer('UDP'):
                    if (packet[IP].src == '10.88.81.1') and (packet[IP].dst == '10.88.80.11') :
                        print packet.show()
                        print 'PASS 2/2'
                        a+=1
            print 'a ='
            print a
            if  a == 2:
                print ("PASS")
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens19')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,1)
            else:
                print 'FAIL'
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens19')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)
        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Di_Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            time.sleep(30)
            os.system('nmcli device disconnect ens19')
            Bsleep(3)
            os.system('nmcli device connect ens18')
            Bsleep(6)
            if count <3:
                count+=1
                self.test_case119()

            else:
                self.assertEqual(1,0)


    def test_case121(self):

        "Case_2215-Outbound Policy Outbound FastestResponse LAN / WAN"
        try:
            Config_File_Upload('hd2hw4_720_test_case121.conf')
            Bsleep(30)
            ssh.connect('10.88.81.254' , username="peplink" , password="peplink")
            time.sleep(3)
            ssh.exec_command('echo peplink | sudo -S tc qdisc add dev ens21 root netem delay 30ms 10ms loss 0.3')
            time.sleep(10)

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(3)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(3)
            #ssh.exec_command("echo peplink | sudo -S nohup python PogoU64.py W7 &> log/out.tmp&")
            ssh.exec_command("echo peplink | sudo -S nohup python PogoU64.py W7 ")
            Bsleep(3)
            ssh.connect('192.168.50.9' , username="peplink" , password="peplink")
            time.sleep(3)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L7 10.88.80.11 1000')
            for std in stdout.readlines():               
                r = std,

            ssh.connect('10.88.81.254' , username="peplink" , password="peplink")
            time.sleep(3)
            ssh.exec_command('echo peplink | sudo -S tc qdisc del dev ens21 root netem delay 30ms 10ms loss 0.3')

            ssh.close()
            print r[0]
            result = r[0]
            print "ast.literal_eval(result)['10.88.81.1'] = "
            print ast.literal_eval(result)['10.88.81.1']
            if ast.literal_eval(result)['10.88.81.1'] >= 950:
                print ast.literal_eval(result)['10.88.81.1']
                print 'PASS'
                
                #UIRestD()
                self.assertEqual(1,1)
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
            else:
                print 'Fail'
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case121()

            else:
                self.assertEqual(1,0)


    def test_case122(self):

        "Case_2216-Outbound Policy Outbound FastestResponse VLAN / WAN"
        try:
            Config_File_Upload('hd2hw4_720_test_case122.conf')
            Bsleep(30)
            os.system('ping -c 4 10.88.1.102')
            time.sleep(2)
            # Check Switch telnet port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  #1 Second Timeout
            for s in range(90):
                result = sock.connect_ex(('10.88.1.102',23))
                if result == 0:
                    print 'Switch port 23 OPEN'
                    # add vlan 60
                    tn = telnetlib.Telnet('10.88.1.102')
                    Bsleep(1)
                    tn.read_until("User:")
                    Bsleep(1)
                    tn.write("admin\r\n")
                    Bsleep(1)
                    tn.read_until("Password:")
                    Bsleep(1)
                    tn.write ('\r\n')
                    Bsleep(1)
                    tn.write("enable\r\n")
                    Bsleep(1)        
                    tn.write("config\r\n")
                    Bsleep(1)
                    tn.write("interface 0/"+LAN_PORT+"\r\n")
                    Bsleep(1)
                    tn.write("vlan participation include 60\r\n")
                    Bsleep(1)
                    tn.write("vlan tagging 60\r\n")
                    Bsleep(1)
                    tn.write("exit\r\n")
                    Bsleep(1)
                    tn.close
                    print 'add vlan - tn.read_all()='
                    print(tn.read_all())
                    break
                else:
                    print str(s)+' Switch port 23 cannot connect, try again'
                s +=1

            time.sleep(3)
            ssh.connect("192.168.50.9" , username="peplink" , password="peplink")
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.60.9')
            result1 = stdout.read()
            print 'result1 ='
            print('result1',str(result1))
            ssh.close()

            if '4 received' in str(result1):
                
                ssh.connect('10.88.81.254' , username="peplink" , password="peplink")
                time.sleep(5)
                ssh.exec_command('echo peplink | sudo -S tc qdisc add dev ens21 root netem delay 30ms 10ms loss 0.3')
                time.sleep(10)
                
                ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
                time.sleep(3)
                ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
                Bsleep(3)
                ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
                Bsleep(3)
                #ssh.exec_command("echo peplink | sudo -S nohup python PogoU64.py W7 &> log/out.tmp&")
                ssh.exec_command("echo peplink | sudo -S python PogoU64.py W7 ")
                Bsleep(6)
                ssh.connect('192.168.60.9' , username="peplink" , password="peplink")
                time.sleep(3)
                ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
                Bsleep(3)
                ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
                Bsleep(3)
                stdin, stdout, stderr = ssh.exec_command('echo peplink | sudo -S python PogoU64.py L7 10.88.80.11 1000')
                Bsleep(6)
                for std in stdout.readlines():
                    r = std,

                ssh.connect('10.88.81.254' , username="peplink" , password="peplink")
                time.sleep(3)
                ssh.exec_command('echo peplink | sudo -S tc qdisc del dev ens21 root netem delay 30ms 10ms loss 0.3')
                Bsleep(3)
                os.system('ping -c 4 10.88.1.102')
                time.sleep(2)
                # Check Switch telnet port
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)  #1 Second Timeout
                for t in range(90):
                    result = sock.connect_ex(('10.88.1.102',23))
                    if result == 0:
                        print 'Switch port 23 OPEN'
                        # del vlan 60
                        tn = telnetlib.Telnet('10.88.1.102')
                        Bsleep(1)
                        tn.read_until("User:")
                        Bsleep(1)
                        tn.write("admin\r\n")
                        Bsleep(1)
                        tn.read_until("Password:")
                        Bsleep(1)
                        tn.write ('\r\n')
                        Bsleep(1)
                        tn.write("enable\r\n")
                        Bsleep(1)
                        tn.write("config\r\n")
                        Bsleep(1)
                        tn.write("interface 0/"+LAN_PORT+"\r\n")
                        Bsleep(1)
                        tn.write("no vlan tagging 60\r\n")
                        Bsleep(1)
                        tn.write("vlan participation auto 60\r\n")
                        Bsleep(1)
                        tn.write("exit\r\n")
                        Bsleep(1)
                        tn.close
                        print 'add vlan - tn.read_all()='
                        print(tn.read_all())
                        break
                    else:
                        print str(t)+' Switch port 23 cannot connect, try again'
                    t +=1

            
                ssh.close()
                print 'r[0] ='
                print r[0]
                result = r[0]
                print "ast.literal_eval(result)['10.88.81.1'] ="
                print ast.literal_eval(result)['10.88.81.1']
                if ast.literal_eval(result)['10.88.81.1'] >= 950:
                    print ('PASS')
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(7)
                    self.assertEqual(1,1)
                else:

                    print ('FAIL')
                    #UIRestD()
                    #time.sleep(32)
                    Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                    Bsleep(30)
                    os.system('nmcli device disconnect ens18')
                    time.sleep(2)
                    os.system('nmcli device connect ens18')
                    time.sleep(5)
                    self.assertEqual(1,0)
            else:
                print ('FAIL')
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
                self.assertEqual(1,0)
        except:

            global count
            try:
                Bquit()
                #UIRestD()
                #time.sleep(32)
                Config_File_Upload('hd2hw4_720_FactoryReset.conf')
                Bsleep(30)
                os.system('nmcli device disconnect ens18')
                time.sleep(2)
                os.system('nmcli device connect ens18')
                time.sleep(5)
            except:
                a=0
            os.system('ping -c 4 10.88.1.102')
            time.sleep(2)
            for t in range(90):
                result = sock.connect_ex(('10.88.1.102',23))
                if result == 0:
                    print 'Switch port 23 OPEN'
                    # del vlan 60
                    tn = telnetlib.Telnet('10.88.1.102')
                    Bsleep(2)        
                    tn.read_until("User:")
                    Bsleep(2)
                    tn.write("admin\r\n")
                    Bsleep(2)
                    tn.read_until("Password:")
                    Bsleep(2)
                    tn.write ('\r\n')
                    Bsleep(2)
                    tn.write("enable\r\n")
                    Bsleep(2)
                    tn.write("config\r\n")
                    Bsleep(2)
                    tn.write("interface 0/"+LAN_PORT+"\r\n")
                    Bsleep(2)
                    tn.write("no vlan tagging 60\r\n")
                    Bsleep(2)
                    tn.write("vlan participation auto 60\r\n")
                    Bsleep(2)
                    tn.write("exit\r\n")
                    Bsleep(2)
                    tn.close
                    break
                else:
                    print str(t)+' Switch port 23 cannot connect, try again'
                t +=1
                
            Bsleep(1)
            #UIRestD()
            #time.sleep(32)
            Config_File_Upload('hd2hw4_720_FactoryReset.conf')
            Bsleep(30)
            os.system('nmcli device disconnect ens18')
            time.sleep(2)
            os.system('nmcli device connect ens18')
            time.sleep(5)
            if count <3:
                count+=1
                self.test_case122()

            else:
                self.assertEqual(1,0)

                

if __name__ == '__main__':

    #time.sleep(7200)
    #Clear nmcli conn profiles
    os.system('nmcli conn delete di-static-ens18')
    time.sleep(5)
    os.system('nmcli conn delete static-ens18')
    time.sleep(5)
    os.system('nmcli conn delete dhcp-ens18')
    time.sleep(5)
    # renew IP　試 192.168.50.1 會不會通
    os.system('nmcli device disconnect ens19')
    time.sleep(2)
    os.system('nmcli device connect ens19')
    time.sleep(2)
    os.system('nmcli device disconnect ens18')
    time.sleep(2)
    os.system('nmcli device connect ens18')
    try:

        if subprocess.check_output( 'ping 192.168.50.1 -c 4', shell = True):

            IpAdd = '192.168.50.1'
            print IpAdd
    except:

        IpAdd = '192.168.1.1'
        
    pepurl = 'http://'+IpAdd #http:// + 設備IP
    driver = Bopen()
    HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP = UIStart(pepurl,driver)
    Bquit()

    path = "config1.py"
    txt = open(path,mode="w")
    txt.write('Mtype = "'+Mtype+'"')
    txt.write('\nHWmode = "'+HWmode+'"')
    txt.write('\nSN = "'+SN+'"')
    txt.write('\nSWver = "'+SWver+'"')
    txt.close()
    time.sleep(2)
    os.system('nmcli device disconnect ens19')
    time.sleep(2)
    os.system('nmcli device disconnect ens18')
    time.sleep(6)
    os.system('nmcli device connect ens18')
    time.sleep(8)


    a = os.popen('ifconfig ens18').read()
    time.sleep(2)
    result = re.findall(ur'(?:[0-9a-fA-F]:?){12}',a)
    PC_MAC = str.upper(result[0])
    os.system('ping -c 4 192.168.50.9')
    time.sleep(2)
    b = os.popen('arp -a |grep 192.168.50.9').read()
    global LAN_U64_MAC
    result = re.findall(ur'(?:[0-9a-fA-F]:?){12}',b)
    LAN_U64_MAC = str.upper(result[0])
    print PC_MAC
    print LAN_U64_MAC
    
    print ('HWmode is ',HWmode)

    suite = unittest.TestLoader().loadTestsFromTestCase(SmokeTest)
    i = datetime.now()
    dt = str(i.year)+str(i.month)+str(i.day)+str(i.hour)+str(i.minute)
    idt = dt.replace(":","")
    rel_path = "Report/" + HWmode + "_TestReport_" + idt + ".html"
    abs_file_path = os.path.join(script_dir, rel_path)
    outfile = open(abs_file_path,"w")
    #UIRestD()
    #time.sleep(32)
    
    os.system('nmcli device disconnect ens18')
    time.sleep(5)
    os.system('nmcli device connect ens18')
    time.sleep(8)   
    runner = HTMLTestRunner.HTMLTestRunner(stream=outfile,verbosity=2,title= SWver +' SmokeTest',description= HWmode + " " + FWver )
    runner.run(suite)
    outfile.close()

    time.sleep(10)


    while count == 0:

        if PingCheck('10.88.3.1'):
            count += 1
            SendMail()

        else:

            time.sleep(2)
            os.system('nmcli device disconnect ens18')
            time.sleep(5)
            os.system('nmcli device connect ens18')
            time.sleep(8)

    os.chdir("/home/peplink/QA/QaPythonTemp/QaAutoRunTest/U64_Smoke_Test")
    ReportSfolder = 'Report/'
    ReportDfolder = '/QAreport/SmokeTestReportAuto/'

    time.sleep(30)
    if PogoFolderUpload(ReportSfolder,ReportDfolder): # 上傳 log
        filelist = glob.glob(ReportSfolder+'*.*') #刪本地 log
        for f in filelist:
            print 'Deleting file: ' + f
            os.remove(f)