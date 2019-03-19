#-*- coding: utf-8 -*-
# 20190214001  新增自動上傳Report

from ConfigFile.T06.config import *
from SmokTestModules.LoSmokeUpdate import *
from SmokTestModules.LoSmokTest_PEPLINK import *
from SmokTestModules.modules import *

PogoUpdate1('BOne_Smoke_Test_Balance.py','/QaPythonTemp/QaAutoRunTest/U64_Smoke_Test/','')

UpdateSfolder = 'QaPythonTemp/QaAutoRunTest/U64_Smoke_Test/ConfigFile/T06'
UpdateDfolder = 'ConfigFile/T06'
PogoUpdateF(UpdateSfolder,UpdateDfolder)

B20Wait = 180
script_dir = os.path.dirname(__file__)
#logging.basicConfig(level=logging.INFO)

global Mtype

def SendMail():
    
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    import smtplib

    msg = MIMEMultipart()
    msg["Subject"] = "Smoke-Test " + HWmode + " " + FWver
    msg["From"] = "AutoQA@msa.hinet.net"
    msg["To"] = "lorancet@peplink.com,mdx121843@gmail.com"
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


class SmokeTest (unittest.TestCase):

    @classmethod

    def setUp(self):
        "Setup the test case"
        global count
        count = 0
        time.sleep(10)
    
    
    def test_case001(self):

        "Case_1037 WAI access via WAN side with NAT-Mappings enabled"
        try:
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(2)
            time.sleep(2)
            NAT_Mapping()
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
            time.sleep(2)
            Bclick('#mainContent > div.smart_content > form > table > tbody.general_settings.web_admin_access_settings > tr.tablecontent2.both.admin_access_settings > td:nth-child(2) > select:nth-child(2) > option:nth-child(2)')
            time.sleep(2)
            Bclick('#mainContent > div.smart_content > form > table > tbody.general_settings.web_admin_access_settings > tr.tablecontent2.both.admin_access_settings > td:nth-child(2) > select:nth-child(4) > option:nth-child(2)')
            time.sleep(2)
            BclickT('Save')

            #enable SSH 8822
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
            time.sleep(2)
            Bcheck('.cli_settings > tr:nth-child(1) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
            time.sleep(2)
            Bclick('.save_action')
            UIsApply(pepurl)
            print "enable SSH 8822"
            time.sleep(AppWait)
            Bquit()

            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.1.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"')

            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    break
            ssh.close()

            WAN1IP = re.findall( r'[0-9]+(?:\.[0-9]+){3}', std, )
            print WAN1IP

            if WAN1IP[0] == '10.88.81.1':

                print ("PASS")
                Bquit()
                UIRestD()

                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 

            else:
                
                Bquit()
                UIRestD()
                os.system('nmcli device disconnect ens19') 
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
            UIRestD()
            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 

            if count <3:
                count+=1
                self.test_case001()

            else:
                self.assertEqual(1,0)


    def test_case002(self):

        "Case_1374 - WAI-Read Only user support"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)

            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
            time.sleep(2) 
            Bfill('#mainContent > div.smart_content > form > table > tbody:nth-child(3) > tr:nth-child(1) > td:nth-child(2) > input','peplink')
            time.sleep(2) 
            Bfill('#mainContent > div.smart_content > form > table > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(2) > input','0912#$%^')
            time.sleep(2) 
            Bfill('#mainContent > div.smart_content > form > table > tbody:nth-child(3) > tr:nth-child(3) > td:nth-child(2) > input','0912#$%^')
            time.sleep(2) 
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()
            driver = Bopen()
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi')
            Bwait_text('Login')

            Bfill('username', 'peplink')
            time.sleep(2)        
            Bfill('password', '0912#$%^')
            time.sleep(2)
            BclickTB('Login')
            time.sleep(10)

            result = re.findall(r'You logged in as a read-only user',driver.page_source)

            if result[0] == 'You logged in as a read-only user':

                print ("PASS")
                ssh.close()
                Bquit()
                UIRestD()

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
            UIRestD()

            if count <3:
                count+=1
                self.test_case002()

            else:
                self.assertEqual(1,0)


    def test_case003(self):

        "Case_1041 WAI access from selected WAN interface(s)"

        a = 0
        try:
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(2)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
            time.sleep(2)
            Bclick('#mainContent > div.smart_content > form > table > tbody.general_settings.web_admin_access_settings > tr.tablecontent2.both.admin_access_settings > td:nth-child(2) > select:nth-child(2) > option:nth-child(2)')
            time.sleep(2)
            Bclick('#mainContent > div.smart_content > form > table > tbody.general_settings.web_admin_access_settings > tr.tablecontent2.both.admin_access_settings > td:nth-child(2) > select:nth-child(4) > option:nth-child(2)')
            time.sleep(2)
            Bclick('#mainContent > div.smart_content > form > div.access_settings > table > tbody > tr.tablecontent2.wan_ip_access_settings > td:nth-child(2) > table > tbody > tbody > tr:nth-child(1) > td:nth-child(2) > div.connlist_table_box > label:nth-child(2) > input[type="checkbox"]')
            time.sleep(2)
            Bclick('#mainContent > div.smart_content > form > div.access_settings > table > tbody > tr.tablecontent2.wan_ip_access_settings > td:nth-child(2) > table > tbody > tbody > tr:nth-child(2) > td:nth-child(2) > div.connlist_table_box > label:nth-child(2) > input[type="checkbox"]')
            time.sleep(2)
            BclickT('Save')
            #enable SSH 8822
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
            time.sleep(2)
            Bcheck('.cli_settings > tr:nth-child(1) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
            time.sleep(2)
            Bclick('.save_action')
            UIsApply(pepurl)
            print "enable SSH 8822"
            time.sleep(AppWait)
            Bquit()

            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.1.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"')

            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    break
            ssh.close()

            result1 = re.findall( r'[0-9]+(?:\.[0-9]+){3}', std, )
            print result1

            if result1[0] == '10.88.81.1':

                a += 1
                
            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    break
            ssh.close()

            result2 = re.findall( r'[0-9]+(?:\.[0-9]+){3}', std, )
            print result2

            if result2[0] == '10.88.81.1':

                a += 1

            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    break
            ssh.close()

            result3 = re.findall( r'[0-9]+(?:\.[0-9]+){3}', std, )
            print result3

            if result3[0] == '10.88.81.1':

                a += 1
                Bquit()

            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    break
            ssh.close()

            result4 = re.findall( r'[0-9]+(?:\.[0-9]+){3}', std, )
            print result4

            if result4[0] == '10.88.81.1':

                a += 1
                Bquit()

            print a

            if a == 4:

                print ("PASS")
                Bquit()
                UIRestD()
                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 

            else:
                
                Bquit()
                UIRestD()
                os.system('nmcli device disconnect ens19') 
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
            UIRestD()
            os.system('nmcli device disconnect ens19') 
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
            time.sleep(B20Wait)
            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.1.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"') 
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
            tn.write("vlan tag "+VID+"\r\n")
            time.sleep(2)
            tn.write("no vlan pvid\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            print "port assign tag "+VID
            time.sleep(2)
            tn.close
            
            Wan_set(1)
            WAN1_Tag(VID)
            NAT_Mapping()
            QosSet()
            time.sleep(10)
            UIsApply(pepurl)    
            time.sleep(AppWait)

            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S iperf -s')

            result1 = []
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "echo peplink | sudo -S iperf -c 10.88.80.11 -t60 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            for std in stdout.readlines():
                result1.append(std)

            c = re.findall(r'MBytes(.*?)Mbits/sec',str(result1))

            print (str(c[-1])+ '======================')
            
            if float(c[-1]) > 1 and float(c[-1]) < 21:

                a += 1
                ssh.close()

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            time.sleep(2)
            result2 = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "echo peplink | sudo -S iperf -c 10.88.81.1 -t60 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            for std in stdout.readlines():
                result2.append(std)

            s = re.findall(r'MBytes(.*?)Mbits/sec',str(result2))

            print (str(s[-1])+ '======================')

            if float(s[-1]) > 1 and float(s[-1]) < 21:
                print (s[-1])
                a += 1
                ssh.close()

            if a == 2:

                Bquit()
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
                UIRestD()

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
            UIRestD()

            if count <3:
                count+=1
                self.test_case004()

            else:
                self.assertEqual(1,0)

    
    def test_case005(self):

        "Case_1047- WAN interface with VLAN tagging and Static connection enabled"

        try:
            time.sleep(B20Wait)
            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.1.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"') 
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
            tn.write("vlan tag "+VID+"\r\n")
            time.sleep(2)
            tn.write("no vlan pvid\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            print "port assign tag "+VID
            time.sleep(2)
            tn.close
            Wan_set(1)         
            WAN1_Tag(VID)
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.80.11')
            time.sleep(2)
            t = stdout.read()
            print('t',str(t))
            ssh.close()
            
            if '4 received' in str(t):

                print ("PASS")
                Bquit()
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
                UIRestD()
                    
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
            UIRestD()

            if count <3:
                count+=1
                self.test_case005()

            else:
                self.assertEqual(1,0)

    def test_case006(self):

        "Case_1046- WAN interface with VLAN tagging and PPPoE enabled"

        try:
            time.sleep(B20Wait)
            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.1.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"') 

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
            tn.write("vlan tag "+VID+"\r\n")
            time.sleep(2)
            tn.write("no vlan pvid\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            print "port assign tag "+VID
            time.sleep(2)
            tn.close
            time.sleep(2)
            Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
            time.sleep(2)
            Bcheck('Enable')
            time.sleep(2)
            SBclickT('PPPoE')
            time.sleep(2)
            Bfill('pppoe_login', 'peplink')
            time.sleep(2)
            Bfill('pppoe_password', '0912#$%^')
            time.sleep(2)
            Bfill('pppoe_confirm_password', '0912#$%^')
            time.sleep(2)
            SBclickT ('Save')
            time.sleep(2)
            WAN1_Tag(VID)
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.80.11')
            time.sleep(2)
            t = stdout.read()
            print('t',str(t))
            ssh.close()
          
            if '4 received' in str(t):

                print ("PASS")
                Bquit()
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
                UIRestD()
                    
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
            UIRestD()

            if count <3:
                count+=1
                self.test_case006()

            else:
                self.assertEqual(1,0)


    
    def test_case007(self):

        "Case_1045- WAN interface with VLAN tagging and DHCP enabled"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            
            os.system('nmcli device connect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.1.50/24') 
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
         
            WAN1_Tag(VID)
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.80.11')
            time.sleep(2)
            t = stdout.read()
            print('t',str(t))
            ssh.close()
            
            if '4 received' in str(t):

                print ("PASS")
                Bquit()
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
                
                UIRestD()
                    
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
            UIRestD()

            if count <3:
                count+=1
                self.test_case007()

            else:
                self.assertEqual(1,0)


    def test_case008(self):

        "Case_1069 Static connection MTU, MSS modify manually"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
            time.sleep(2)
            Bcheck('Enable')
            time.sleep(2)
            SBclickT('Static IP') 
            time.sleep(2)
            SBfillT('IP Address', '10.88.81.1','1','0','1')
            time.sleep(2)
            SBfillT('Default Gateway', '10.88.81.254')
            time.sleep(2)
            SBfillT('DNS Server 1', '10.88.3.1')
            time.sleep(2)
            SBfillT('DNS Server 2', '168.95.1.1')
            time.sleep(2)
            Bcheck('.mode_panel > label:nth-child(2) > input:nth-child(1)')
            Bfill('input.custom','1300')
            Bcheck('div.mss > label:nth-child(2) > input:nth-child(1)')
            Bfill('div.mss > div:nth-child(3) > input:nth-child(2)','1260')
            SBclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()

            MTU = 500

            try:
                while True:

                    runtest = subprocess.check_output('ping -M do -s '+ str(MTU) +' -c 1 10.88.81.254', shell = True)
                    print str(runtest)

                    if 'ms' in str(runtest):
                        MTU += 1

            except:

                print MTU
                if MTU + 27 == 1300:

                        UIRestD()
                        print (str(MTU + 27))
                        self.assertEqual(1,1)

                else:

                        UIRestD()
                        print (str(MTU + 27))
                        self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case008()

            else:
                self.assertEqual(1,0)


    def test_case009(self):

        "Case_1070 Default connection MTU, Mss value"

        try:
            time.sleep(B20Wait)
            time.sleep(AppWait)
            driver = Bopen()
            UIsLogin(pepurl)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            Bquit()
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

                    UIRestD()
                    print (str(MTU + 27))
                    self.assertEqual(1,1)

                else:

                    UIRestD()
                    print (str(MTU + 27))
                    self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case009()

            else:
                self.assertEqual(1,0)


    def test_case010(self):

        "Case_1071 PPPoE connection MTU, MSS modify manually"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
            time.sleep(2)
            Bcheck('Enable')
            time.sleep(2)
            SBclickT('PPPoE') 
            time.sleep(2)
            Bfill('pppoe_login', 'peplink')
            time.sleep(2)
            Bfill('pppoe_password', '0912#$%^')
            time.sleep(2)
            Bfill('pppoe_confirm_password', '0912#$%^')
            time.sleep(2)
            Bcheck('.mode_panel > label:nth-child(2) > input:nth-child(1)')
            Bfill('input.custom','1200')
            Bcheck('div.mss > label:nth-child(2) > input:nth-child(1)')
            Bfill('div.mss > div:nth-child(3) > input:nth-child(2)','1160')  
            SBclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()

            MTU = 500

            try:
                while True:

                    runtest = subprocess.check_output('ping -M do -s '+ str(MTU) +' -c 1 10.88.81.254', shell = True)
                    print str(runtest)

                    if 'ms' in str(runtest):
                        MTU += 1
            except:

                print MTU
                if MTU + 27 == 1200:

                    UIRestD()
                    print (str(MTU + 27))
                    self.assertEqual(1,1)


                else:

                    UIRestD()
                    print (str(MTU + 27))
                    self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case010()

            else:
                self.assertEqual(1,0)


    def test_case011(self):

        "Case_1190- Reply ICMP Ping Requests Disable / Enable"
        
        a = 0
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            ICMP_Disable()
            time.sleep(10)
            UIsApply(pepurl)
            Bquit()
            time.sleep(AppWait)
            
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.81.1')
            time.sleep(2)
            t1 = stdout.read()
            print('t1',str(t1))
            if '0 received' in str(t1):

                a += 1

            else:
                
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

            driver = Bopen()
            UIsLogin(pepurl)
            ICMP_Enable()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(30)
            
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.81.1')
            time.sleep(2)
            t2 = stdout.read()
            print('t2',str(t2))
            if '4 received' in str(t2):

                a += 1

            if a == 2:
                
                print ("PASS")
                Bquit()
                UIRestD()
                    
            else:
                
                Bquit()
                print (a)
                UIRestD()
                self.assertEqual(1,0)

        except:
                 
            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case011()

            else:
                self.assertEqual(1,0)


    def test_case012(self):

        "Case_1234 WAN Backup w/o Priority"
        try:

            driver = Bopen()
            UIsLogin(pepurl)
            #enable SSH 8822
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
            time.sleep(2)
            Bcheck('.cli_settings > tr:nth-child(1) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
            time.sleep(2)
            Bclick('.save_action')
            UIsApply(pepurl)
            time.sleep(10)
            Bquit()
            print "enable SSH 8822"
            time.sleep(AppWait)

            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('get wan')

            status = []
            for std in stdout.readlines():
                if 'Connection Status' in std:
                    status.append(std)

            ssh.close()

            WAN1 = str(status[0][37:])
            WAN2 = str(status[1][37:])

            if 'Connected' in WAN1 and 'Connected' in WAN2:

                driver = Bopen()
                UIsLogin(pepurl)
                Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
                time.sleep(2)
                SBclickT('Backup')
                SBclickT('Save')
                time.sleep(10)
                UIsApply(pepurl)
                time.sleep(AppWait)

                ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
                time.sleep(3)
                stdin, stdout, stderr = ssh.exec_command('get wan')

                status = []
                for std in stdout.readlines():
                    if 'Connection Status' in std:
                        status.append(std)

                WAN1 = str(status[0][37:])
                WAN2 = str(status[1][37:])

                ssh.close()

                if 'Cold Standby' in WAN1 and 'Connected' in WAN2:
                    print 'pass'
                    Bquit()
                    UIRestD()

                else:
                    Bquit()
                    UIRestD()
                    self.assertEqual(1,0)
            else:
                Bquit()
                UIRestD()
                self.assertEqual(1,0)
        
        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case012()

            else:
                self.assertEqual(1,0)
                      


    def test_case013(self):

        "Case_1235 WAN Backup with Priority"
        try:
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
            time.sleep(2)
            SBclickT('Backup')
            SBclickT('Save')
            time.sleep(10)
            #enable SSH 8822
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
            time.sleep(2)
            Bcheck('.cli_settings > tr:nth-child(1) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
            time.sleep(10)
            Bclick('.save_action')
            UIsApply(pepurl)
            Bquit()
            print "enable SSH 8822"
            time.sleep(AppWait)

            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('get wan')

            status = []
            for std in stdout.readlines():
                if 'Connection Status' in std:
                    status.append(std)

            WAN1 = str(status[0][37:])
            WAN2 = str(status[1][37:])

            ssh.close()

            if 'Cold Standby' in WAN1 and 'Connected' in WAN2:

                driver = Bopen()
                UIsLogin(pepurl)
                Bclick('#mainContent > div.smart_content > div.conn_info_panel > table > tbody:nth-child(2) > tr:nth-child(2) > td > div.status_button > button.icon.conn_button_disconnect.disconnect_action')
                SBclickT('OK')
                time.sleep(AppWait)

                ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
                time.sleep(3)
                stdin, stdout, stderr = ssh.exec_command('get wan')

                status = []
                for std in stdout.readlines():
                    if 'Connection Status' in std:
                        status.append(std)

                WAN1 = str(status[0][37:])
                WAN2 = str(status[1][37:])

                ssh.close()

                if 'Connected' in WAN1 and 'Disconnected (Manual)' in WAN2:

                    print 'pass'
                    Bquit()
                    UIRestD()
                else:
                
                    Bquit()
                    UIRestD()
                    self.assertEqual(1,0)
            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)
        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case013()

            else:
                self.assertEqual(1,0)


    def test_case014(self):

        "Case_1050 - Active Session"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1) 
            NAT_Mapping()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)

            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=sessionv3')
            result1 = re.findall(r'<tr class="tablecontent2 zb2">(.*?)</tr>',driver.page_source)
            Total_Sessions1 = re.findall(r'<td>(.*?)</td>',str(result1))

            ssh.connect('192.168.1.9' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
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
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command("echo peplink | sudo -S python PogoU64.py W1 10.88.81.1 60")
            time.sleep(2)
            for std in stdout.readlines():
                print std

            time.sleep(10)
            SBclickT('Refresh')
            time.sleep(10)
            result2 = re.findall(r'<tr class="tablecontent2 zb2">(.*?)</tr>',driver.page_source)
            Total_Sessions2 = re.findall(r'<td>(.*?)</td>',str(result2))
            Bquit()

            if int(Total_Sessions1[-1]) < int(Total_Sessions2[-1]):

                print ("PASS")
                Bquit()
                UIRestD()

            else:

                ssh.close()
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            ssh.close()
            UIRestD()

            if count <3:
                count+=1
                self.test_case014()

            else:
                self.assertEqual(1,0)


    
    def test_case015(self):

        "Case_1297-SNMP v1 v2"
        a = 0        
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            SMNP_Set()
            UIsApply(pepurl)
            time.sleep(10)
            time.sleep(AppWait)
            
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "snmpwalk -v 1 -c public 192.168.1.1"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            
            r1 = stdout.read()
            print (r1)
            
            if 'support@peplink.com' in str(r1):

                a += 1
                
            else:
                
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "snmpwalk -v 2c -c public 192.168.1.1"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            r2 = stdout.read()
            print (r2)

            if 'support@peplink.com' in str(r2):

               a += 1
                    
            else:
                
                Bquit()
                UIRestD()
                self.assertEqual(1,0)


            if a == 2:
            
                Result = "pass"
                print ("PASS")
                Bquit()
                UIRestD()


        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case015()

            else:
                self.assertEqual(1,0)


    def test_case016(self):

        "Case_1298-SNMP Peplink Info"
        a = 0        
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            SMNP_Set()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "snmpwalk -v 1 -c public 192.168.1.1"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            
            r1 = stdout.read()
            print (r1)
            
            if 'Peplink' or 'Pepwave' in str(r):

                print ("PASS")
                Bquit()
                UIRestD()
                self.assertEqual(1,1)
                    
            else:
                
                Bquit()
                UIRestD()
                self.assertEqual(1,0)


        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case016()

            else:
                self.assertEqual(1,0)


    def test_case017(self):

        "Case_1300-SNMP v3 MD5"
        a = 0        
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            SMNP_Set()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = 'snmpwalk -v 3 -u md5 -a MD5 -A peplink5978 -l authNoPriv 192.168.1.1'
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            
            r = stdout.read()
            print (r)
            
            if 'support@peplink.com' in str(r):

                print ("PASS")
                Bquit()
                UIRestD()
                ssh.close()
                self.assertEqual(1,1)
                    
            else:
                
                Bquit()
                UIRestD()
                ssh.close()
                self.assertEqual(1,0)


        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case017()

            else:
                self.assertEqual(1,0)


    def test_case018(self):

        "Case_1301-SNMP v3 SHA"
        a = 0        
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            SMNP_Set()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = 'snmpwalk -v 3 -u sha -a SHA -A peplink5978 -l authNoPriv 192.168.1.1'
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            
            r = stdout.read()
            print (r)
            
            if 'support@peplink.com' in str(r):

                print ("PASS")
                Bquit()
                UIRestD()
                ssh.close()
                self.assertEqual(1,1)
                    
            else:
                
                Bquit()
                UIRestD()
                ssh.close()
                self.assertEqual(1,0)


        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case018()

            else:
                self.assertEqual(1,0)



    def test_case019(self):

        "Case_1974 SNMP - SNMP trap"
        try:
            time.sleep(B20Wait)
            a = 0
            driver = Bopen()
            UIsLogin(pepurl)
            SMNP_Set()
            time.sleep(10)
            UIsApply(pepurl)
            Bquit()
            time.sleep(AppWait)
            time.sleep(AppWait)

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S snmptrapd -m all -Lf /tmp/traptest -d")
            time.sleep(2)
            ssh.close()
            time.sleep(120)
            driver = Bopen()
            UIsLogin(pepurl)
            BclickT('Disconnect')
            time.sleep(2)
            BclickT('OK')
            time.sleep(60)
            BclickT('Connect')
            time.sleep(60)
            Bquit()
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command("cat /tmp/traptest |grep onn")
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S killall snmptrapd")
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S rm /tmp/traptest")
            time.sleep(2)
            ssh.close()

            result = []
            for std in stdout.readlines():
                result.append(std)

            print result


            if ' onnected' in str(result):
                a += 1


            if 'sconnected' in str(result):
                a += 1

            if a == 2:

                print 'pass'
                UIRestD()

            else:
                UIRestD()
                self.assertEqual(1,0)


        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case019()

            else:
                self.assertEqual(1,0)


    def test_case020(self):

        "Case_1051 Customer DHCP Server Lease Time, IP Range, DHCP Client List, Subnet Mask"

        a = 0        
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan')
            time.sleep(2)
            BclickT('Untagged LAN')
            time.sleep(2)
            BfillT('IP Range', '192.168.1.10','1','1','1')
            time.sleep(2)
            BfillT('IP Range', '192.168.1.100','2','1','1')
            time.sleep(2)
            BfillT('Lease Time', '6','2','1','1')
            time.sleep(2)
            BclickT('Assign DNS server automatically')
            time.sleep(2)
            BfillT('DHCP Reservation', 'Lo-U64','1','0','1')
            time.sleep(2)
            BfillT('DHCP Reservation', PC_MAC,'2','0','1')
            time.sleep(2)
            BfillT('DHCP Reservation', '192.168.1.200','3','0','1')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            Bquit()
            time.sleep(AppWait)
                         
            os.system('nmcli device disconnect ens18')
            time.sleep(10)
            os.system('nmcli device connect ens18')
            time.sleep(10)

            r = os.popen('nmcli device show |grep IP4').read()
            print r

            if '192.168.1.200/24' in str(r):

                print ("PASS")
                ssh.close()
                Bquit()
                UIRestD()

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
            UIRestD()

            if count <3:
                count+=1
                self.test_case020()

            else:
                self.assertEqual(1,0)


    def test_case021(self):

        "Case_1052 Assign Custom DNS Servers"
        
        a = 0
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan')
            time.sleep(2)
            BclickT('Untagged LAN')
            time.sleep(2)
            BclickT('Assign DNS server automatically')
            time.sleep(2)
            BfillT('DNS Server 1:','1.1.1.1')
            time.sleep(2)
            BfillT('DNS Server 2:','2.2.2.2')
            time.sleep(2)
            BclickT('Assign WINS server')
            time.sleep(2)
            BfillT('WINS Server 1:','3.3.3.3')
            time.sleep(2)
            BfillT('WINS Server 2:','4.4.4.4')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            Bquit()
            time.sleep(AppWait)

            os.system('nmcli device disconnect ens18')
            time.sleep(10)
            os.system('nmcli device connect ens18')
            time.sleep(10)

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
                UIRestD()

            else:

                ssh.close()
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:
         
            global count
            try:
                Bquit()
                
            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case021()

            else:
                self.assertEqual(1,0)


    
    def test_case022(self):

        "Case_1053 DHCP Reservation"
        
        a = 0        
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            b = random.randrange(100,150)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan')
            time.sleep(2)
            BclickT('Untagged LAN')
            time.sleep(2)
            BfillT('DHCP Reservation', 'Lo-U64','1','0','1')
            time.sleep(2)
            BfillT('DHCP Reservation',PC_MAC,'2','0','1')        
            time.sleep(2)
            BfillT('DHCP Reservation', '192.168.1.'+str(b),'3','0','1')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            Bquit()
            time.sleep(AppWait)
                         
            os.system('nmcli device disconnect ens18')
            time.sleep(10)
            os.system('nmcli device connect ens18')
            time.sleep(10)

            r = os.popen('nmcli device show |grep IP4').read()
            print r
            
            print '192.168.1.'+str(b)+'/24'
            if '192.168.1.'+str(b)+'/24' in str(r):

                self.assertEqual(1,1)
                print ("PASS")
                ssh.close()
                Bquit()
                UIRestD()
                
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
            UIRestD()

            if count <3:
                count+=1
                self.test_case022()

            else:
                self.assertEqual(1,0)


    def test_case023(self):

        "Case_1345 Extended DHCP Option"
        
        a = 0        
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan')
            time.sleep(2)
            BclickT('Untagged LAN')
            time.sleep(2)
            BclickT('Add')
            time.sleep(2)
            BclickT('15. DNS Domain Name')
            time.sleep(2)
            BfillT('Add Extended DHCP Option','PEPLINK_TTC')
            time.sleep(2)
            Bclick('button.ui-button:nth-child(1)')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            Bquit()
            time.sleep(AppWait)
            os.system('nmcli device disconnect ens18')
            time.sleep(10)
            os.system('nmcli device connect ens18')
            time.sleep(10)

            r = os.popen('nmcli device show |grep IP4.DOMAIN').read()
            print r
           
            if 'PEPLINK_TTC' in str(r):

                ssh.close()
                UIRestD()
                Bquit()
                self.assertEqual(1,1)
           
            else:

                ssh.close()
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case023()

            else:
                self.assertEqual(1,0)

    
    def test_case024(self):

        "Case_1371 DHCP - Extended DHCP Option support"
        
        a = 0        
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan')
            time.sleep(2)
            BclickT('Untagged LAN')
            time.sleep(2)
            BclickT('Add')
            time.sleep(2)
            BclickT('15. DNS Domain Name')
            time.sleep(2)
            BfillT('Add Extended DHCP Option','PEPLINK_TTC')
            time.sleep(2)
            Bclick('button.ui-button:nth-child(1)')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            Bquit()
            time.sleep(AppWait)
            os.system('nmcli device disconnect ens18')
            time.sleep(10)
            os.system('nmcli device connect ens18')
            time.sleep(10)

            r = os.popen('nmcli device show |grep IP4.DOMAIN').read()
            print r
           
            if 'PEPLINK_TTC' in str(r):

                ssh.close()
                UIRestD()
                Bquit()
                self.assertEqual(1,1)
           
            else:

                ssh.close()
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case024()

            else:
                self.assertEqual(1,0)


    
    def test_case025(self):

        "Case_1381 WINS Server & WINS Clients"
        try:
            time.sleep(B20Wait)
            a = 0        
            driver = Bopen()
            UIsLogin(pepurl)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan')
            time.sleep(2)
            BclickT('Untagged LAN')
            time.sleep(2)
            BclickT('Assign DNS server automatically')
            time.sleep(2)
            BfillT('DNS Server 1:','1.1.1.1')
            time.sleep(2)
            BfillT('DNS Server 2:','2.2.2.2')
            time.sleep(2)
            BclickT('Assign WINS server')
            time.sleep(2)
            BfillT('WINS Server 1:','3.3.3.3')
            time.sleep(2)
            BfillT('WINS Server 2:','4.4.4.4')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            Bquit()
            time.sleep(AppWait)
            os.system('nmcli device disconnect ens18')
            time.sleep(10)
            os.system('nmcli device connect ens18')
            time.sleep(10)

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
                UIRestD()
                self.assertEqual(1,1)


            else:

                ssh.close()
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            ssh.close()
            UIRestD()

            if count <3:
                count+=1
                self.test_case025()

            else:
                self.assertEqual(1,0)

 
    
    def test_case026(self):

        "Case_1115 DNS Proxy Enable / Disable"
        a = 0

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Bquit()
            result1 = []
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command("nslookup www.peplink.com 192.168.1.1")
            time.sleep(2)
            for std in stdout.readlines():
              result1.append(std)

            print (str(result1))
            if '104.25.106.21' in str(result1):

                a += 1

            driver = Bopen()
            UIsLogin(pepurl)
            DNS_Proxy_Disable()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            
            result2 = []
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command("nslookup www.peplink.com 192.168.1.1")
            time.sleep(2)
            for std in stdout.readlines():
              result2.append(std)

            print (str(result2))
            if 'no servers could be reached' in str(result2):

                a += 1

            if a == 2:

                ssh.close()
                Bquit()
                UIRestD()
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
            UIRestD()

            if count <3:
                count+=1
                self.test_case026()

            else:
                self.assertEqual(1,0)


    
    def test_case027(self):

        "Case_1120 Local DNS Records"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            DNS_Proxy_Enable()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            
            result1 = []
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('nslookup pepttc.test.com 192.168.1.1')
            time.sleep(2)
            for std in stdout.readlines():
                result1.append(std)

            print (str(result1))
            
            if '210.1.1.10' in str(result1):

                
                print ("PASS")
                ssh.close()
                Bquit()
                UIRestD()
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
            UIRestD()

            if count <3:
                count+=1
                self.test_case027()

            else:
                self.assertEqual(1,0)



    def test_case028(self):
        
        "Case_1376 Bandwidth Allowance Link Disconnect"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            
            BandwidthAllowance()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command('iperf -c 10.88.80.11 -u -b 100m -i 2 -t 20')
            time.sleep(2)
            ssh.close()
            
            time.sleep(60)           
            Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=main')
            time.sleep(2)
           
            if Btext('Hit'):

                self.assertEqual(1,1)
                Bquit()
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
   
            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case028()

            else:
                self.assertEqual(1,0)


    def test_case029(self):

        "Case_1412 CLI - LAN/WAN Test"

        a = 0
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            time.sleep(2)       
            Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
            time.sleep(2)
            BcheckT('CLI SSH & Console')
            time.sleep(2)    
            BclickT('LAN / WAN','1')
            time.sleep(2)
            BclickT ('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()

            result1 = []
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "sshpass -p admin ssh -o StrictHostKeyChecking=no admin@192.168.1.1 -p 8822 'get system;get cpu;'"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            for std in stdout.readlines():
                    
                result1.append(std)

            print (str(result1))

            if "Router Name" in str(result1):
                    
                a += 1


            result2 = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "sshpass -p admin ssh -o StrictHostKeyChecking=no admin@10.88.81.1 -p 8822 'get system;get cpu;'"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            for std in stdout.readlines():
                    
                result2.append(std)

            print (str(result2))

            if "Router Name" in str(result2):
                    
                a += 1

            if a == 2:

                self.assertEqual(1,1)
                Bquit()
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

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
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.1.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"') 

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
            Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
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
            time.sleep(10)
            #enable SSH 8822
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
            time.sleep(2)
            Bcheck('.cli_settings > tr:nth-child(1) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
            time.sleep(2)
            Bclick('.save_action')
            UIsApply(pepurl)
            print "enable SSH 8822"
            time.sleep(AppWait)

            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    break
            ssh.close()

            WANIP = re.findall( r'[0-9]+(?:\.[0-9]+){3}', std, )

            ssh.connect('10.88.80.11' , port=22 ,username='peplink' , password='peplink')
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('nslookup -type=a tweric.no-ip.org 8.8.8.8')
            time.sleep(2)

            CheckIP = stdout.read()
            result = re.findall(r'Address: (.*)',CheckIP)

            print WANIP [0]
            print result[0] 
            
            if result[0] == WANIP[0]:
                self.assertEqual(1,1)
                print ("PASS")
                ssh.close()
                Bquit()
                UIRestD()
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

                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')  

            else:

                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            ssh.close()
            UIRestD()
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
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')

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
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.1.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"')

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
            Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
            time.sleep(2)
            Bclick('.conn_method_action > option:nth-child(4)')
            time.sleep(2)
            Bfill('.pppoe_panel > tr:nth-child(2) > td:nth-child(2) > input:nth-child(1)', 'T1170871')
            time.sleep(2)
            Bfill('.pppoe_panel > tr:nth-child(3) > td:nth-child(2) > input:nth-child(1)', 'fn6xp8td')
            time.sleep(2)
            Bfill('.pppoe_panel > tr:nth-child(4) > td:nth-child(2) > input:nth-child(1)', 'fn6xp8td')
            time.sleep(2)
            Bclick('#dynamic_dns_panel > tr.tablecontent2.ddns_main_panel.ddns_panel > td:nth-child(2) > select > option:nth-child(2)')
            time.sleep(2)
            Bfill('tr.ddns_default_panel:nth-child(3) > td:nth-child(2) > input:nth-child(1)', 'lorancet@peplink.com')
            time.sleep(2)
            Bfill('tr.ddns_default_panel:nth-child(4) > td:nth-child(2) > input:nth-child(1)', '09!@#$')
            time.sleep(2)
            Bfill('tr.ddns_default_panel:nth-child(5) > td:nth-child(2) > input:nth-child(1)', '09!@#$')
            time.sleep(2)
            Bfill('.ddns_host_panel > td:nth-child(2) > textarea:nth-child(1)', 'pepttc01.changeip.co')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            #enable SSH 8822
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
            time.sleep(2)
            Bcheck('.cli_settings > tr:nth-child(1) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
            time.sleep(2)
            Bclick('.save_action')
            UIsApply(pepurl)
            print "enable SSH 8822"
            time.sleep(AppWait)

            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    break
            ssh.close()

            WANIP = re.findall( r'[0-9]+(?:\.[0-9]+){3}', std, )

            ssh.connect('10.88.80.11' , port=22 ,username='peplink' , password='peplink')
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('nslookup -type=a pepttc01.changeip.co 8.8.8.8')
            time.sleep(2)

            CheckIP = stdout.read()
            result = re.findall(r'Address: (.*)',CheckIP)

            if result == WANIP:

                print ("PASS")
                self.assertEqual(1,1)
                print ("PASS")
                ssh.close()
                Bquit()
                UIRestD()
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

                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')  
                

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
            UIRestD()
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
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')  

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
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.1.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"')

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
            Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
            time.sleep(2)
            Bclick('.conn_method_action > option:nth-child(4)')
            time.sleep(2)
            Bfill('.pppoe_panel > tr:nth-child(2) > td:nth-child(2) > input:nth-child(1)', 'T1170871')
            time.sleep(2)
            Bfill('.pppoe_panel > tr:nth-child(3) > td:nth-child(2) > input:nth-child(1)', 'fn6xp8td')
            time.sleep(2)
            Bfill('.pppoe_panel > tr:nth-child(4) > td:nth-child(2) > input:nth-child(1)', 'fn6xp8td')
            time.sleep(2)
            Bclick('#dynamic_dns_panel > tr.tablecontent2.ddns_main_panel.ddns_panel > td:nth-child(2) > select > option:nth-child(2)')
            time.sleep(2)
            Bfill('tr.ddns_default_panel:nth-child(3) > td:nth-child(2) > input:nth-child(1)', 'lorancet@peplink.com')
            time.sleep(2)
            Bfill('tr.ddns_default_panel:nth-child(4) > td:nth-child(2) > input:nth-child(1)', '09!@#$')
            time.sleep(2)
            Bfill('tr.ddns_default_panel:nth-child(5) > td:nth-child(2) > input:nth-child(1)', '09!@#$')
            time.sleep(2)
            Bfill('.ddns_host_panel > td:nth-child(2) > textarea:nth-child(1)', 'pepttc01.changeip.co,pepttc02.changeip.co')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            #enable SSH 8822

            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
            time.sleep(2)
            Bcheck('.cli_settings > tr:nth-child(1) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
            time.sleep(2)
            Bclick('.save_action')
            UIsApply(pepurl)
            print "enable SSH 8822"
            time.sleep(AppWait)

            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    break
            ssh.close()

            WANIP = re.findall( r'[0-9]+(?:\.[0-9]+){3}', std, )

            ssh.connect('10.88.80.11' , port=22 ,username='peplink' , password='peplink')
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('nslookup -type=a pepttc01.changeip.co 8.8.8.8')
            time.sleep(2)

            CheckIP1 = stdout.read()
            result1 = re.findall(r'Address: (.*)',CheckIP1)

            ssh.connect('10.88.80.11' , port=22 ,username='peplink' , password='peplink')
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('nslookup -type=a pepttc02.changeip.co 8.8.8.8')
            time.sleep(2)

            CheckIP2 = stdout.read()
            result2 = re.findall(r'Address: (.*)',CheckIP2)

            if result1 == WANIP:
                a += 1

            if result2 == WANIP:
                a += 1

            if a == 2:

                self.assertEqual(1,1)
                print ("PASS")
                ssh.close()
                Bquit()
                UIRestD()
                print result1[0]
                print result2[0]
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

                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')

            else:

                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            ssh.close()
            UIRestD()
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
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')  


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
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.1.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"')
            
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
            Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
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
            time.sleep(10)
            #enable SSH 8822
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
            time.sleep(2)
            Bcheck('.cli_settings > tr:nth-child(1) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
            time.sleep(2)
            Bclick('.save_action')
            UIsApply(pepurl)
            print "enable SSH 8822"
            time.sleep(AppWait)
            
            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    break
            ssh.close()

            WANIP = re.findall( r'[0-9]+(?:\.[0-9]+){3}', std, )

            ssh.connect('10.88.80.11' , port=22 ,username='peplink' , password='peplink')
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('nslookup -type=a tweric.no-ip.org 8.8.8.8')
            time.sleep(2)

            CheckIP = stdout.read()
            result = re.findall(r'Address: (.*)',CheckIP)

            if result == WANIP:

                self.assertEqual(1,1)
                print ("PASS")
                ssh.close()
                Bquit()
                UIRestD()
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

                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"')  

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
            UIRestD()
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
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')  

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
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.1.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"') 

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
            Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
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
            time.sleep(10)
            #enable SSH 8822
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
            time.sleep(2)
            Bcheck('.cli_settings > tr:nth-child(1) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
            time.sleep(2)
            Bclick('.save_action')
            UIsApply(pepurl)
            print "enable SSH 8822"
            time.sleep(AppWait)


            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    break
            ssh.close()

            OldIP = re.findall( r'[0-9]+(?:\.[0-9]+){3}', std, )

            time.sleep(10)
            Bclick("#mainContent > div.smart_content > div.conn_info_panel > table > tbody:nth-child(1) > tr:nth-child(2) > td > div.status_button > button.icon.conn_button_disconnect.disconnect_action")
            time.sleep(2)
            BclickT("OK")
            time.sleep(20)
            Bclick("#mainContent > div.smart_content > div.conn_info_panel > table > tbody:nth-child(1) > tr:nth-child(2) > td > div.status_button > button.icon.conn_button_connect.connect_action")
            time.sleep(120)

            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    break
            ssh.close()

            NewIP = re.findall( r'[0-9]+(?:\.[0-9]+){3}', std, )

            if str(NewIP[0]) != "(none)" and OldIP[0] != NewIP[0]:

                ssh.connect('10.88.80.11' , port=22 ,username='peplink' , password='peplink')
                time.sleep(2)
                stdin, stdout, stderr = ssh.exec_command('nslookup -type=a tweric.no-ip.org 8.8.8.8')
                time.sleep(2)

                CheckIP = stdout.read()
                result = re.findall(r'Address: (.*)',CheckIP)

                if result == NewIP:

                    self.assertEqual(1,1)
                    print ("PASS")
                    ssh.close()
                    Bquit()
                    UIRestD()
                    print result[0]
                    print NewIP[0]
                    
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
                    time.sleep(2)
                    os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                    time.sleep(2)
                    os.system('nmcli connection up "dhcp-ens18"')  

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
            UIRestD()
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
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"')  

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
            os.system('nmcli connection add con-name "static-ens18" ifname ens18 type ethernet ip4 192.168.1.50/24') 
            time.sleep(2)
            os.system('nmcli connection up "static-ens18"') 

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
            Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
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
            time.sleep(10)
            #enable SSH 8822
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=admin')
            time.sleep(2)
            Bcheck('.cli_settings > tr:nth-child(1) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
            time.sleep(2)
            Bclick('.save_action')
            UIsApply(pepurl)
            print "enable SSH 8822"
            time.sleep(AppWait)


            ssh.connect(IpAdd , port=8822 ,username='admin' , password='admin')
            time.sleep(3)
            stdin, stdout, stderr = ssh.exec_command('get wan')
            for std in stdout.readlines():
                if 'IP Address' in std:
                    print std,
                    break
            ssh.close()

            WANIP = re.findall( r'[0-9]+(?:\.[0-9]+){3}', std, )

            ssh.connect('10.88.80.11' , port=22 ,username='peplink' , password='peplink')
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('nslookup -type=a tweric.no-ip.org 8.8.8.8')
            time.sleep(2)

            CheckIP = stdout.read()
            result = re.findall(r'Address: (.*)',CheckIP)

            if result == WANIP:

                self.assertEqual(1,1)
                print ("PASS")
                ssh.close()
                Bquit()
                UIRestD()
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

                os.system('nmcli device disconnect ens19') 
                time.sleep(2)
                os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
                time.sleep(2)
                os.system('nmcli connection up "dhcp-ens18"') 
                
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
            UIRestD()
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
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 

            if count <3:
                count+=1
                self.test_case035()

            else:
                self.assertEqual(1,0)


    def test_case036(self):

        "Case_1397-Firewall - Inbound Allow /default deny"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            NAT_Mapping()
            FireWallRlue1397()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)

            os.system('nmcli device disconnect ens19') 
            time.sleep(2)
            os.system('nmcli connection add con-name "dhcp-ens18" ifname ens18 type ethernet') 
            time.sleep(2)
            os.system('nmcli connection up "dhcp-ens18"') 

            ssh.connect('192.168.1.9' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
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
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command("echo peplink | sudo -S python PogoU64.py W1 10.88.81.1 60")
            time.sleep(2)
            
            for std in stdout.readlines():
                print std

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            apath = 'log'
            apattern ='"*.log"'
            rawcommand = 'find {path} -name {pattern}'
            command = rawcommand.format(path=apath, pattern=apattern)

            stdin, stdout, stderr = ssh.exec_command(command)
            time.sleep(2)
            filelist = stdout.read().splitlines()

            #print filelist

            sftp = ssh.open_sftp()
            for afile in filelist:
                (head, filename) = os.path.split(afile)
                print(filename)
                stdin, stdout, stderr = ssh.exec_command('cat ' + afile)
                r1 = stdout.read()

            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')

            if ('Allowed CONN'):

                print ("PASS")
                Bquit()
                UIRestD()
                ssh.close()

            else:

                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
       
            except:
                a=0
            UIRestD()
            ssh.close()

            if count <3:
                count+=1
                self.test_case036()

            else:
                self.assertEqual(1,0)


    def test_case037(self):

        "Case_1398-Firewall - Inbound deny /default Allow"

        try:
            time.sleep(AppWait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1) 
            NAT_Mapping()
            FireWallRlue1398()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)

            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.81.1')
            time.sleep(2)
            t = stdout.read()

            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')

            time.sleep(2)

            if Btext('Denied CONN'):

                print ("PASS")
                Bquit()
                UIRestD()
            else:

                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
 
            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case037()

            else:
                self.assertEqual(1,0)


    def test_case038(self):

        "Case_1399-Firewall - Outbound deny /default Allow"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            NAT_Mapping()
            FireWallRlue1399()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.80.11')
            time.sleep(2)
            t = stdout.read()
            print('Case_1399-Firewall \n',str(t))
            if '0 received' in str(t):

                Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                time.sleep(2)
                
                if Btext('Denied CONN'):

                    print ("PASS")
                    Bquit()
                    UIRestD()
                    self.assertEqual(1,1)
                    
                else:
                    
                    Bquit()
                    UIRestD()
                    self.assertEqual(1,0)

            else:
                
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case038()

            else:
                self.assertEqual(1,0)


    def test_case039(self):

        "Case_1400-Firewall - Outbound Allow /default deny"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1) 
            NAT_Mapping()
            FireWallRlue1400()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.80.11')
            time.sleep(2)
            t = stdout.read()

            if '4 received' in str(t):

                Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                time.sleep(2)
                
                if Btext('Allowed CONN'):

                    print ("PASS")
                    Bquit()
                    UIRestD()
                    self.assertEqual(1,1)

                else:

                    Bquit()
                    UIRestD()
                    self.assertEqual(1,0)

            else:
                
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case039()

            else:
                self.assertEqual(1,0)



    def test_case040(self):

        "Case_1841 Firewall - OutBound Block Domain"
        a = 0
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 lo.pepttc.com')
            time.sleep(2)
            t = stdout.read()

            if '4 received' in str(t):
                a += 1

            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=firewall')
            time.sleep(2)
            Bclick('#firewall_settings > table:nth-child(2) > tfoot > tr:nth-child(2) > td > button')
            time.sleep(2)
            Bfill('tr.tablecontent2:nth-child(2) > td:nth-child(2) > input:nth-child(1)','Firewall By Domain')
            time.sleep(2)
            Bclick('tr.tablecontent2:nth-child(8) > td:nth-child(2) > div:nth-child(1) > select:nth-child(1) > option:nth-child(4)')
            time.sleep(2)
            Bfill('.domain > input:nth-child(1)','lo.pepttc.com')
            time.sleep(2)
            Bcheck('tr.tablecontent2:nth-child(9) > td:nth-child(2) > label:nth-child(2) > input:nth-child(1)')
            time.sleep(2)
            Bcheck('tr.tablecontent2:nth-child(10) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
            time.sleep(2)
            SBclickT('Save') 
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(30)

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 lo.pepttc.com')
            time.sleep(2)
            t = stdout.read()

            if '0 received' in str(t):

                a += 1

            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(2)
            
            if Btext('Denied CONN=lan MAC='):

                a += 1


            if a == 3:
                
                Bquit()
                UIRestD()
                self.assertEqual(1,1)
                    
            else:
                
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case040()

            else:
                self.assertEqual(1,0)


    def test_case041(self):
          
        "Case_1842 Firewall - OutBound Allow Domain"
        a = 0
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 lo.pepttc.com')
            time.sleep(2)
            t = stdout.read()

            if '4 received' in str(t):
                a += 1

            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=firewall')
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
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(30)

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 lo.pepttc.com')
            time.sleep(2)
            t = stdout.read()

            if '4 received' in str(t):

                a += 1

            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(2)
            
            if Btext('Allowed CONN=lan'):

                a += 1

            if a == 3:
                
                Bquit()
                UIRestD()
                self.assertEqual(1,1)

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case041()

            else:
                self.assertEqual(1,0)


    def test_case042(self):

        "Case_1264 - NAT Mapping"
        try:
            time.sleep(B20Wait)
            a = 0
            b = 0

            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1) 
            NAT_Mapping()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)

            ssh.connect('192.168.1.9' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
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
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command("echo peplink | sudo -S python PogoU64.py W1 10.88.81.1 60")

            for std in stdout.readlines():
                print std

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            apath = 'log'
            apattern ='"*.log"'
            rawcommand = 'find {path} -name {pattern}'
            command = rawcommand.format(path=apath, pattern=apattern)
            stdin, stdout, stderr = ssh.exec_command(command)
            time.sleep(2)
            filelist = stdout.read().splitlines()

            #print filelist

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

            ssh.connect('192.168.1.9' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
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
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command("echo peplink | sudo -S python PogoU64.py W1 10.88.81.51 60")

            for std in stdout.readlines():
                print std

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            apath = 'log'
            apattern ='"*.log"'
            rawcommand = 'find {path} -name {pattern}'
            command = rawcommand.format(path=apath, pattern=apattern)
            stdin, stdout, stderr = ssh.exec_command(command)
            time.sleep(2)
            filelist = stdout.read().splitlines()

            #print filelist

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

            print a
            print b
            if a + b == 12:
                
                self.assertEqual(1,1)
                print ("PASS")
                Bquit()
                UIRestD()

            else:
                    
                ssh.close()
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case042()

            else:
                self.assertEqual(1,0)


    def test_case043(self):

        "Case_1209 Inbound Access with Additional Public IP Enalbe(Default IP)"
        try:
            time.sleep(B20Wait)
            a = 0
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1) 
            Inboun_access_20('192.168.1.9')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)

            ssh.connect('192.168.1.9' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
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
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command("echo peplink | sudo -S python PogoU64.py W1 10.88.81.1 60")
            time.sleep(2)
            for std in stdout.readlines():
                print std

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            apath = 'log'
            apattern ='"*.log"'
            rawcommand = 'find {path} -name {pattern}'
            command = rawcommand.format(path=apath, pattern=apattern)
            stdin, stdout, stderr = ssh.exec_command(command)
            time.sleep(2)
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
                Bquit()
                UIRestD()
                self.assertEqual(1,1)

            else:
                    
                ssh.close()
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case043()

            else:
                self.assertEqual(1,0)


    def test_case044(self):

        "Case_1210 Inbound Access with Additional Public IP Enalbe(Additional IP)"
        try:
            time.sleep(B20Wait)
            b = 0
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1) 
            Inboun_access_20('192.168.1.9')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)

            ssh.connect('192.168.1.9' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
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
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command("echo peplink | sudo -S python PogoU64.py W1 10.88.81.51 60")

            for std in stdout.readlines():
                print std

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            apath = 'log'
            apattern ='"*.log"'
            rawcommand = 'find {path} -name {pattern}'
            command = rawcommand.format(path=apath, pattern=apattern)
            stdin, stdout, stderr = ssh.exec_command(command)
            time.sleep(2)
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
                Bquit()
                UIRestD()
                self.assertEqual(1,1)

            else:
                
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case044()

            else:
                self.assertEqual(1,0)


    def test_case045(self):
          
        "Case_1211-Outbound Policy Custom Outbound Traffic Rules(Auto)"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(2)
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()
            ssh.connect('10.88.81.254' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S tc qdisc add dev ens21 root netem delay 30ms 10ms loss 0.3')
            time.sleep(10)
            
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S nohup python PogoU64.py W2 10000 10.88.81.1 10.88.82.1 10.88.83.1 10.88.84.1 10.88.85.1 10.88.86.1 10.88.87.1 10.88.88.1 &> log/out.tmp&")
            time.sleep(2)
            ssh.connect('192.168.1.9' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L2 10.88.80.11 10000 1000')
            time.sleep(2)
            for std in stdout.readlines():
                r = std,

            ssh.connect('10.88.81.254' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S tc qdisc del dev ens21 root netem delay 30ms 10ms loss 0.3')
            time.sleep(2)
            ssh.close()

            if "WAN1 1000" in str(r):
                print r
                UIRestD()
                self.assertEqual(1,1)

            else:

                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case045()

            else:
                self.assertEqual(1,0)


    def test_case046(self):

        "Case_1232-Custom Rules Priority Any proto"
        a = 0
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(2)
            time.sleep(2)       
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
            time.sleep(2)
            Bclick('.add_action')
            time.sleep(2)
            Bfill('rulename', 'Test Case 1232')

            time.sleep(2)
            Bclick('tr.tablecontent2:nth-child(3) > td:nth-child(2) > div:nth-child(1) > select:nth-child(1) > option:nth-child(5)')
            time.sleep(2)
            Bfill('tr.tablecontent2:nth-child(3) > td:nth-child(2) > div:nth-child(1) > input:nth-child(4)', LAN_U64_MAC )
            time.sleep(2)
            Bclick('tr.tablecontent2:nth-child(4) > td:nth-child(2) > div:nth-child(1) > select:nth-child(1) > option:nth-child(1)')
            time.sleep(2)
            Bclick('.algo_action > option:nth-child(1)')
            time.sleep(2)
            Bdrop_offset('div.conn_1:nth-child(2) > span:nth-child(1)',-130,0)
            time.sleep(2)
            Bdrop_offset('div.slider_conn:nth-child(2) > div:nth-child(2) > span:nth-child(1)',-270,0)
            time.sleep(2)
            Bdrop_offset('div.slider_conn:nth-child(3) > div:nth-child(2) > span:nth-child(1)',-275,0)
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S nohup python PogoU64.py W2 10000 10.88.81.1 10.88.82.1 10.88.83.1 10.88.84.1 10.88.85.1 10.88.86.1 10.88.87.1 10.88.88.1 &> log/out.tmp&")
            time.sleep(2)
            ssh.connect('192.168.1.9' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L2 10.88.80.11 10000 1000')
            time.sleep(2)
            for std in stdout.readlines():
                r = std,
            print r
            time.sleep(2)
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
                Bquit()
                UIRestD()
                    
            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
    
            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case046()

            else:
                self.assertEqual(1,0)


    def test_case047(self):

        "Case_1232 - Custom Rules Weighed by MAC address"
        a = 0
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(2)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
            time.sleep(2)
            BclickT('Add Rule')
            time.sleep(2)
            Bfill('rulename', 'Test Case 1232')
            time.sleep(2)
            Bclick('tr.tablecontent2:nth-child(3) > td:nth-child(2) > div:nth-child(1) > select:nth-child(1) > option:nth-child(5)')
            time.sleep(2)
            Bfill('tr.tablecontent2:nth-child(3) > td:nth-child(2) > div:nth-child(1) > input:nth-child(4)', LAN_U64_MAC )
            time.sleep(2)
            Bclick('tr.tablecontent2:nth-child(4) > td:nth-child(2) > div:nth-child(1) > select:nth-child(1) > option:nth-child(1)')
            time.sleep(2)
            Bdrop_offset('div.conn_1:nth-child(2) > span:nth-child(1)',-130,0)
            time.sleep(2)
            Bdrop_offset('div.slider_conn:nth-child(2) > div:nth-child(2) > span:nth-child(1)',-270,0)
            time.sleep(2)
            Bdrop_offset('div.slider_conn:nth-child(3) > div:nth-child(2) > span:nth-child(1)',-275,0)
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()


            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S nohup python PogoU64.py W2 10000 10.88.81.1 10.88.82.1 10.88.83.1 10.88.84.1 10.88.85.1 10.88.86.1 10.88.87.1 10.88.88.1 &> log/out.tmp&")
            time.sleep(2)
            ssh.connect('192.168.1.9' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L2 10.88.80.11 10000 1000')
            time.sleep(2)
            for std in stdout.readlines():
                r = std,
            print r
            time.sleep(2)
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
                
                self.assertEqual(1,1)
                Bquit()
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case047()

            else:
                self.assertEqual(1,0)


    def test_case048(self):
          
        "Case_1233-Custom Rules Least Used by Source IP Network"
        a = 0
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(2)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
            time.sleep(2)
            Bclick('.add_action')
            time.sleep(2)
            Bfill('rulename', 'Test Case 1233')
            time.sleep(2)
            Bclick('tr.tablecontent2:nth-child(3) > td:nth-child(2) > div:nth-child(1) > select:nth-child(1) > option:nth-child(3)')
            time.sleep(2)
            Bfill('tr.tablecontent2:nth-child(3) > td:nth-child(2) > div:nth-child(1) > input:nth-child(2)','192.168.1.0')
            Bclick('tr.tablecontent2:nth-child(4) > td:nth-child(2) > div:nth-child(1) > select:nth-child(1) > option:nth-child(1)')
            time.sleep(2)
            Bclick('.algo_action > option:nth-child(6)')
            time.sleep(2)
            Bclick('.chkbox_panel > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            Bquit()
            time.sleep(AppWait)
            
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S nohup python PogoU64.py W2 10000 10.88.81.1 10.88.82.1 10.88.83.1 10.88.84.1 10.88.85.1 10.88.86.1 10.88.87.1 10.88.88.1 &> log/out.tmp&")
            time.sleep(2)
            ssh.connect('192.168.1.9' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L2 10.88.80.11 10000 1000')
            time.sleep(2)
            for std in stdout.readlines():
                r = std,
            print r
            time.sleep(2)
            ssh.close()

            if "WAN1 1000" in str(r):

                UIRestD()
                self.assertEqual(1,1)

            else:

                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case048()

            else:
                self.assertEqual(1,0)


    def test_case049(self):

        "Case_1405-Outbound Policy Expert Mode"
        try:
            
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
            SF_toLoFH1()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(10)

            if Btext('connected to To_FH1_Test'):
                ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
                time.sleep(2)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.11')
                time.sleep(2)
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):

                    Enable_ExperMode()

                    time.sleep(2)

                    Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
                    time.sleep(2)
                    Bclick('.add_action')
                    time.sleep(2)
                    Bfill('rulename', 'Expert Mode Test')
                    time.sleep(2)
                    Bfill('dstip', '192.168.2.0')
                    time.sleep(2)
                    Bclick('.algo_action > option:nth-child(4)')
                    time.sleep(2)
                    SBclickT('Save')
                    time.sleep(2)
                    Bdrop_offset('tr.sort_item:nth-child(2) > td:nth-child(1) > div:nth-child(2)',0,-50)
                    time.sleep(10)
                    UIsApply(pepurl)
                    time.sleep(AppWait)
                    Bquit()
                    ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
                    time.sleep(2)
                    stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.11')
                    time.sleep(2)
                    t = stdout.read()
                    print('t',str(t))
                    ssh.close()

                    if '0 received' in str(t):

                        print ("PASS")
                        UIRestD()
                        self.assertEqual(1,1)

                    else:

                        UIRestD()
                        self.assertEqual(1,0)
                else:

                    UIRestD()
                    self.assertEqual(1,0)

            else:

                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case049()

            else:
                self.assertEqual(1,0)



    def test_case050(self):

        "Out Bound Policy By Domain"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(2)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
            time.sleep(2)
            Bclick('.add_action')
            time.sleep(2)
            Bfill('rulename', 'Outbound By Domain')
            time.sleep(2)
            Bclick('#ui-id-3 > table > tbody.custom > tr:nth-child(4) > td:nth-child(2) > div > select > option:nth-child(4)')
            time.sleep(2)
            Bfill('tr.tablecontent2:nth-child(4) > td:nth-child(2) > div:nth-child(1) > input:nth-child(5)','lo.pepttc.com')
            time.sleep(2)
            Bclick('.algo_action > option:nth-child(3)')
            time.sleep(2)
            Bcheck('option.conn:nth-child(2)')
            time.sleep(2)
            SBclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            
            time.sleep(AppWait)
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S nohup python PogoU64.py W2 10000 10.88.81.1 10.88.82.1 10.88.83.1 10.88.84.1 10.88.85.1 10.88.86.1 10.88.87.1 10.88.88.1 &> log/out.tmp&")
            time.sleep(2)
            ssh.connect('192.168.1.9' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L2 lo.pepttc.com 10000 1000')
            time.sleep(2)
            for std in stdout.readlines():
                r = std,
            print r
            time.sleep(2)
            ssh.close()
            Bquit()

            if "WAN2 1000" in str(r):

                UIRestD()
                self.assertEqual(1,1)

            else:

                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case050()

            else:
                self.assertEqual(1,0)


    def test_case051(self):

        "Case_1090 Multiple Static route"

        a = 0
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            #set static route
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan')
            time.sleep(2)
            #BclickT('Untagged LAN')
            time.sleep(2)
            Bfill('#mainContent > div.smart_content > form > div.general_settings_panel > table.form_table.static_route_panel > tbody > tr.tablecontent2 > td:nth-child(2) > table > tbody.matrix_row > tr > td:nth-child(1) > input','192.168.2.0')
            time.sleep(2)
            Bfill('#mainContent > div.smart_content > form > div.general_settings_panel > table.form_table.static_route_panel > tbody > tr.tablecontent2 > td:nth-child(2) > table > tbody.matrix_row > tr > td:nth-child(3) > input','192.168.1.201')
            time.sleep(2)
            Bclick('#mainContent > div.smart_content > form > div.general_settings_panel > table.form_table.static_route_panel > tbody > tr.tablecontent2 > td:nth-child(2) > table > tbody.matrix_row > tr > td.matrix_btn_col > button')
            time.sleep(2)
            Bfill('#mainContent > div.smart_content > form > div.general_settings_panel > table.form_table.static_route_panel > tbody > tr.tablecontent2 > td:nth-child(2) > table > tbody:nth-child(3) > tr > td:nth-child(1) > input','192.168.3.0')
            time.sleep(2)
            Bfill('#mainContent > div.smart_content > form > div.general_settings_panel > table.form_table.static_route_panel > tbody > tr.tablecontent2 > td:nth-child(2) > table > tbody:nth-child(3) > tr > td:nth-child(3) > input','192.168.1.201')
            SBclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.201')
            time.sleep(2)
            t = stdout.read()
            print('t',str(t))
            ssh.close()

            if '4 received' in str(t):
                
                a += 1
                ssh.close()

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.3.201')
            time.sleep(2)
            t = stdout.read()
            print('t',str(t))
            ssh.close()

            if '4 received' in str(t):
                
                a += 1
                ssh.close()

            if a == 2:

                self.assertEqual(1,1)
                UIRestD()

            else:

                UIRestD()
                self.assertEqual(1,0)
            
        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case051()

            else:
                self.assertEqual(1,0)


    def test_case052(self):

        "Case_2204 OSPF authencation None"
        try:
            time.sleep(B20Wait)
            #set OSPF 
            driver = Bopen()
            UIsLogin(pepurl)
            ssh.connect('192.168.1.201' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S cp /etc/quagga/ospfd.conf.none /etc/quagga/ospfd.conf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S /etc/init.d/quagga restart')
            time.sleep(10) 
            ssh.close()
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospf')
            time.sleep(2)
            SBclickT('Add')
            time.sleep(2)
            #Bfill('#ospf_dialog > form > table > tbody.ospf_dialog_ospf_panel > tr:nth-child(1) > td:nth-child(2) > input','0')
            Bfill('#ui-id-3 > table > tbody.ospf_dialog_ospf_panel > tr:nth-child(3) > td:nth-child(2) > input','0')
            time.sleep(2)
            #Bclick('#ospf_dialog > form > table > tbody:nth-child(2) > tr:nth-child(2) > td.ospf_interface_panel.no_cost > div:nth-child(2) > div.interface_col > label > input[type="checkbox"]')
            Bclick('#ui-id-3 > table > tbody:nth-child(2) > tr:nth-child(2) > td.ospf_interface_panel.no_cost > div:nth-child(2) > div.interface_col > label > input')
            time.sleep(2)
            SBclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospfstatus')
            result = driver.page_source
            print driver.page_source
            Bquit()

            if '192.168.2.0/24 192.168.3.0/24' in result:
                
                ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
                time.sleep(2)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.201')
                time.sleep(2)
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):

                    self.assertEqual(1,1)
                    UIRestD()
                else:

                    UIRestD()
                    self.assertEqual(1,0)

            else:

                UIRestD()
                self.assertEqual(1,0)
 
        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            UIRestD()
               
            if count <3:
                count+=1
                self.test_case052()

            else:
                self.assertEqual(1,0)


    def test_case053(self):

        "Case_2205 OSPF authencation Text"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            ssh.connect('192.168.1.201' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S cp /etc/quagga/ospfd.conf.text /etc/quagga/ospfd.conf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S /etc/init.d/quagga restart')
            time.sleep(10) 
            ssh.close()
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospf')
            time.sleep(2)
            SBclickT('Add')
            time.sleep(2)
            Bfill('#ui-id-3 > table > tbody.ospf_dialog_ospf_panel > tr:nth-child(3) > td:nth-child(2) > input','0')
            time.sleep(2)
            Bclick('#ui-id-3 > table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > select > option:nth-child(2)')
            time.sleep(2)
            Bfill('#ui-id-3 > table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > input','ci$c0')
            time.sleep(2)
            Bclick('#ui-id-3 > table > tbody:nth-child(2) > tr:nth-child(2) > td.ospf_interface_panel.no_cost > div:nth-child(2) > div.interface_col > label > input')
            time.sleep(2)
            SBclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()

            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospfstatus')
            result = driver.page_source
            print driver.page_source
            Bquit()

            if '192.168.2.0/24 192.168.3.0/24' in result:
                
                ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
                time.sleep(2)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.201')
                time.sleep(2)
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):
                    
                    print "Passed"
                    UIRestD()
                else:

                    UIRestD()
                    self.assertEqual(1,0)

            else:

                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()    

            if count <3:
                count+=1
                self.test_case053()

            else:
                self.assertEqual(1,0)


    def test_case054(self):

        "Case_2206 OSPF authencation MD5"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            ssh.connect('192.168.1.201' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S cp /etc/quagga/ospfd.conf.md5 /etc/quagga/ospfd.conf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S /etc/init.d/quagga restart')
            time.sleep(10) 
            ssh.close()
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospf')
            time.sleep(2)
            SBclickT('Add')
            time.sleep(2)
            Bfill('#ui-id-3 > table > tbody.ospf_dialog_ospf_panel > tr:nth-child(3) > td:nth-child(2) > input','0')
            time.sleep(2)
            Bclick('#ui-id-3 > table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > select > option:nth-child(3)')
            time.sleep(2)
            Bfill('#ui-id-3 > table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > input','ci$c0')
            time.sleep(2)
            Bclick('#ui-id-3 > table > tbody:nth-child(2) > tr:nth-child(2) > td.ospf_interface_panel.no_cost > div:nth-child(2) > div.interface_col > label > input')
            time.sleep(2)
            SBclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()

            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospfstatus')
            result = driver.page_source
            print driver.page_source
            Bquit()

            if '192.168.2.0/24 192.168.3.0/24' in result:
                
                ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
                time.sleep(2)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.201')
                time.sleep(2)
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):

                    self.assertEqual(1,1)
                    UIRestD()
                else:
                    UIRestD()
                    self.assertEqual(1,0)

            else:
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case054()

            else:
                self.assertEqual(1,0)


    def test_case055(self):

        "Case_2043 RIPv2 authencation None"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            ssh.connect('192.168.1.201' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S nohup cp /etc/quagga/ripd.conf.none /etc/quagga/ripd.conf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S nohup /etc/init.d/quagga restart')
            time.sleep(10) 
            ssh.close()
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospf')
            time.sleep(2)
            Bclick('#ospf_panel > table.form_table.sep.rip_summary_table > tbody > tr > td:nth-child(2) > button')
            #Bclick('#rip_summary_table > tr > td:nth-child(2) > button')
            time.sleep(2)
            Bclick('#ui-id-3 > table > tbody:nth-child(2) > tr:nth-child(2) > td.ospf_interface_panel.no_cost > div:nth-child(2) > div.interface_col > label > input')
            #Bclick('#ospf_dialog > form > table > tbody:nth-child(2) > tr:nth-child(2) > td.ospf_interface_panel.no_cost > div:nth-child(2) > div.interface_col > label > input[type="checkbox"]')
            #time.sleep(2)
            #SBclickT('OK')
            time.sleep(2)
            SBclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()

            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospfstatus')
            result = driver.page_source
            print driver.page_source
            Bquit()

            if '192.168.2.0/24 192.168.3.0/24' in result:
                
                ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
                time.sleep(2)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.201')
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):
                    
                    self.assertEqual(1,1)
                    UIRestD()
                else:

                    UIRestD()
                    self.assertEqual(1,0)

            else:

                UIRestD()
                self.assertEqual(1,0)
 
        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            UIRestD() 
            
            if count <3:
                count+=1
                self.test_case055()

            else:
                self.assertEqual(1,0)


    def test_case056(self):

        "Case_2044 RIPv2 authencation Text"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            ssh.connect('192.168.1.201' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S nohup cp /etc/quagga/ripd.conf.text /etc/quagga/ripd.conf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S nohup /etc/init.d/quagga restart')
            time.sleep(10) 
            ssh.close()
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospf')
            time.sleep(2)
            Bclick('#ospf_panel > table.form_table.sep.rip_summary_table > tbody > tr > td:nth-child(2) > button')
            #Bclick('#rip_summary_table > tr > td:nth-child(2) > button')
            time.sleep(2)
            Bclick('#ui-id-3 > table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > select > option:nth-child(2)')
            time.sleep(2)
            Bfill('#ui-id-3 > table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > input','ci$c0')
            time.sleep(2)
            Bclick('#ui-id-3 > table > tbody:nth-child(2) > tr:nth-child(2) > td.ospf_interface_panel.no_cost > div:nth-child(2) > div.interface_col > label > input')
            #Bclick('#ospf_dialog > form > table > tbody:nth-child(2) > tr:nth-child(2) > td.ospf_interface_panel.no_cost > div:nth-child(2) > div.interface_col > label > input[type="checkbox"]')
            #time.sleep(2)
            #SBclickT('OK')
            time.sleep(2)
            SBclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()

            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospfstatus')
            result = driver.page_source
            print driver.page_source
            Bquit()

            if '192.168.2.0/24 192.168.3.0/24' in result:
                
                ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
                time.sleep(2)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.201')
                time.sleep(2)
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):
                    
                    self.assertEqual(1,1)
                    UIRestD()
                else:

                    UIRestD()
                    self.assertEqual(1,0)

            else:

                UIRestD()
                self.assertEqual(1,0)
 
        except:

            global count
            try:
                Bquit()
                
            except:
                a=0
            UIRestD()
            
            if count <3:
                count+=1
                self.test_case056()

            else:
                self.assertEqual(1,0)
           

    
    def test_case057(self):

        "Case_2045 RIPv2 authencation MD5"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            ssh.connect('192.168.1.201' , username="peplink" , password="peplink")
            ssh.exec_command('echo peplink | sudo -S nohup cp /etc/quagga/ripd.conf.md5 /etc/quagga/ripd.conf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S nohup /etc/init.d/quagga restart')
            time.sleep(10)
            ssh.close()
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospf')
            time.sleep(2)
            Bclick('#ospf_panel > table.form_table.sep.rip_summary_table > tbody > tr > td:nth-child(2) > button')
            #Bclick('#rip_summary_table > tr > td:nth-child(2) > button')
            time.sleep(2)
            Bclick('#ui-id-3 > table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > select > option:nth-child(3)')
            time.sleep(2)
            Bfill('#ui-id-3 > table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > input','ci$c0')
            time.sleep(2)
            Bclick('#ui-id-3 > table > tbody:nth-child(2) > tr:nth-child(2) > td.ospf_interface_panel.no_cost > div:nth-child(2) > div.interface_col > label > input')
            #Bclick('#ospf_dialog > form > table > tbody:nth-child(2) > tr:nth-child(2) > td.ospf_interface_panel.no_cost > div:nth-child(2) > div.interface_col > label > input[type="checkbox"]')
            #time.sleep(2)
            #SBclickT('OK')
            time.sleep(2)
            SBclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()

            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=ospfstatus')
            result = driver.page_source
            print driver.page_source
            Bquit()

            if '192.168.2.0/24 192.168.3.0/24' in result:
                
                ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
                time.sleep(2)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.201')
                time.sleep(2)
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):
                    
                    self.assertEqual(1,1)
                    UIRestD()
                    
                else:
                    UIRestD()
                    self.assertEqual(1,0)

            else:
                UIRestD()
                self.assertEqual(1,0)
 
        except:

            global count
            try:
                 Bquit()
                
            except:
                a=0
            UIRestD()
            
            if count <3:
                count+=1
                self.test_case057()

            else:
                self.assertEqual(1,0)


    def test_case058(self):

        "Case_1749-IPSec VPN-Mode-Main,Aggressive Mode"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            IPSec_7()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.11')
            time.sleep(2)
            t = stdout.read()
            print('t',str(t))
            ssh.close()

            if '4 received' in str(t):

                print ("PASS")
                Bquit()
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case058()

            else:
                self.assertEqual(1,0)


    def test_case059(self):

        "Case_1410-IPSec VPN-Preshared key Authencation"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            IPSec_7()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.11')
            time.sleep(2)
            t = stdout.read()
            print('t',str(t))
            ssh.close()

            if '4 received' in str(t):

                print ("PASS")
                Bquit()
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case059()

            else:
                self.assertEqual(1,0)

    
    def test_case060(self):

        "Case_1761-IPSec VPN-Event Log"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            IPSec_7()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog#ipsec_log')
            time.sleep(10)
            if Btext('IPsec: toFusionHubIPSec/1x1 - Connected'):

                print ("PASS")
                Bquit()
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case060()

            else:
                self.assertEqual(1,0)


    def test_case061(self):

        "Case_1762-Status -> IPSec VPN"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            IPSec_7()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=ipsecstatus')
            time.sleep(10)
            if Btext('192.168.1.0/24 &lt;-&gt; 192.168.2.0/24'):

                print ("PASS")
                Bquit()
                self.assertEqual(1,1)

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case061()

            else:
                self.assertEqual(1,0)


    def test_case062(self):

        "Case_1767-Dashboard IPSec VPN"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            IPSec_7()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=main')
            time.sleep(10)
            if Btext('toFusionHubIPSec') and Btext('Established'):

                print ("PASS")
                Bquit()
                self.assertEqual(1,1)

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case062()

            else:
                self.assertEqual(1,0)


    def test_case064(self):

        "Case_1099-SpeedFusion VPN Role endpoint /Hub mode"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            SF_toLoFH1()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(20)

            if Btext('connected to To_FH1_Test'):
                Bquit()
                time.sleep(10)
                ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
                time.sleep(2)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.11')
                time.sleep(2)
                t = stdout.read()
                print('t',str(t))
                ssh.close()

                if '4 received' in str(t):

                    print ("PASS")
                    Bquit()
                    UIRestD()

                else:

                    Bquit()
                    UIRestD()
                    self.assertEqual(1,0)
            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case064()

            else:
                self.assertEqual(1,0)


    def test_case065(self):

        "Case_1100-SpeedFusion Link faill over, Link fail back"
        a = 0
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            SF_toLoFH1()
            WAN1_Disable()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.11')
            time.sleep(2)
            t = stdout.read()
            print('t',str(t))
            ssh.close()

            if '0 received' in str(t):

                a += 1

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

            WAN1_Enable()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.2.11')
            time.sleep(2)
            t = stdout.read()
            print('t',str(t))
            ssh.close()

            if '4 received' in str(t):

                a += 1

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

            if a == 2:

                print ("PASS")
                Bquit()
                UIRestD()
                self.assertEqual(1,1)

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case065()

            else:
                self.assertEqual(1,0)


    def test_case066(self):

        "Case_1313-SpeedFusion Site-to-Site VPN in hub-and-spoke"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            Wan_set(1)
            SF_toLoFH1()
            time.sleep(2)
            SF_toLoFH2()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            ssh.connect("192.168.2.11" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.3.11')
            time.sleep(2)
            t = stdout.read()
            print('t',str(t))
            ssh.close()

            if '4 received' in str(t):

                print ("PASS")
                Bquit()
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

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
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            NAT_Mapping()
            QosSet()
            time.sleep(10)
            UIsApply(pepurl)    
            time.sleep(AppWait)
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            time.sleep(2)
            result1 = []
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "echo peplink | sudo -S iperf -c 10.88.80.11 -t60 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            for std in stdout.readlines():
                result1.append(std)

            c = re.findall(r'MBytes(.*?)Mbits/sec',str(result1))

            print (c[-1])

            if float(c[-1]) > 19 and float(c[-1]) < 21:

                a += 1
                ssh.close()

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            time.sleep(2)
            result2 = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "echo peplink | sudo -S iperf -c 10.88.81.1 -t60 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            for std in stdout.readlines():
                result2.append(std)

            s = re.findall(r'MBytes(.*?)Mbits/sec',str(result2))

            print (s[-1])

            if float(s[-1]) > 19 and float(s[-1]) < 21:

                a += 1
                ssh.close()

            if a == 2:

                path = "Test_Result/case067_temp.txt"
                txt = open(path,mode="w")
                txt.write("067=pass")
                txt.close()
                self.assertEqual(1,1)
                Bquit()
                UIRestD()

            else:

                path = "Test_Result/case067_temp.txt"
                txt = open(path,mode="w")
                txt.write("067=fail")
                txt.close()
                self.assertEqual(1,0)
                Bquit()
                UIRestD()

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case067()

            else:
                self.assertEqual(1,0)


    def test_case068(self):

        "Case_1358 - individual Bandwidth Limits - Guest"
        global qos
        a = 0

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            NAT_Mapping()
            QosSet()
            QosGroupChange()
            time.sleep(10)
            UIsApply(pepurl)    
            time.sleep(AppWait)
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            result1 = []
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "echo peplink | sudo -S iperf -c 10.88.80.11 -t60 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            for std in stdout.readlines():
                result1.append(std)

            c = re.findall(r'MBytes(.*?)Mbits/sec',str(result1))

            print (c[-1])
            
            if float(c[-1]) > 9 and float(c[-1]) < 11:

                a += 1
                ssh.close()

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            time.sleep(2)
            result2 = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "echo peplink | sudo -S iperf -c 10.88.81.1 -t60 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            for std in stdout.readlines():
                result2.append(std)

            s = re.findall(r'MBytes(.*?)Mbits/sec',str(result2))

            print (s[-1])

            if float(s[-1]) > 9 and float(s[-1]) < 11:

                a += 1
                ssh.close()

            if a == 2:

                path = "Test_Result/case068_temp.txt"
                txt = open(path,mode="w")
                txt.write("068=pass")
                txt.close()
                self.assertEqual(1,1)
                Bquit()
                UIRestD()

            else:

                path = "Test_Result/case068_temp.txt"
                txt = open(path,mode="w")
                txt.write("068=fail")
                txt.close()
                self.assertEqual(1,0)
                Bquit()
                UIRestD()

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case068()

            else:
                self.assertEqual(1,0)


    def test_case069(self):

        "Case_1356 - Modify Group Reserved Bandwidth"
        time.sleep(B20Wait)
        r=0
        path = "Test_Result/case067_temp.txt"
        txt1 = open(path,mode="r")
        
        a = txt1.read()
       

        if "067=pass" in str(a):
            r += 1
            txt1.close()

        path = "Test_Result/case068_temp.txt"
        txt2 = open(path,mode="r")
        
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
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            NAT_Mapping()
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
            Bclick('#upstream_display > td.tablecontent2 > select > option:nth-child(2)')
            Bfill('#upstream_display > td.tablecontent2 > input:nth-child(3)','10')
            Bclick('#downstream_display > td.tablecontent2 > select > option:nth-child(2)')
            Bfill('#downstream_display > td.tablecontent2 > input:nth-child(3)','50')
            SBclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)    
            time.sleep(AppWait)
            Bquit()
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            result1 = []
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "echo peplink | sudo -S iperf -c 10.88.80.11 -t10 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            for std in stdout.readlines():
                result1.append(std)

            c = re.findall(r'Bytes(.*?)Mbits/sec',str(result1))

            if float(c[-1]) > 10:

                a += 1
                ssh.close()

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            time.sleep(2)
            result2 = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "echo peplink | sudo -S iperf -c 10.88.81.1 -t10 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            for std in stdout.readlines():
                result2.append(std)

            s = re.findall(r'Bytes(.*?)Mbits/sec',str(result2))

            if float(s[-1]) > 60:
                
                a += 1
                ssh.close()

            if a == 2:

                Bquit()
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case070()

            else:
                self.assertEqual(1,0)


    
    def test_case071(self):

        "Case_1354 - QOS - Bandwidth control- enable"

        a = 0
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            NAT_Mapping()
            #setDown and Up streamBandwidth
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
            Bclick('#upstream_display > td.tablecontent2 > select > option:nth-child(2)')
            Bfill('#upstream_display > td.tablecontent2 > input:nth-child(3)','10')
            Bclick('#downstream_display > td.tablecontent2 > select > option:nth-child(2)')
            Bfill('#downstream_display > td.tablecontent2 > input:nth-child(3)','50')
            SBclickT('Save')
            #set Group Bandwidth Reservation
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=eqosbandwidth')
            Bclick('#eqos_bandwidth_gsmb_display > td > table > tbody:nth-child(1) > tr.tablecontent2 > td:nth-child(2) > input[type="checkbox"]')
            SBclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)    
            time.sleep(AppWait)
            Bquit()
               
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            time.sleep(2)
            result1 = []
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "echo peplink | sudo -S iperf -c 10.88.80.11 -t10 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            for std in stdout.readlines():
                result1.append(std)

            c = re.findall(r'Bytes(.*?)Mbits/sec',str(result1))

            if float(c[-1]) > 8 and float(c[-1]) < 10:

                a += 1
                ssh.close()

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S iperf -s')
            time.sleep(2)
            result2 = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "echo peplink | sudo -S iperf -c 10.88.81.1 -t10 -P4"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            for std in stdout.readlines():
                result2.append(std)

            s = re.findall(r'Bytes(.*?)Mbits/sec',str(result2))

            if float(s[-1]) > 40 and float(s[-1]) < 50:
                
                a += 1
                ssh.close()

            if a == 2:

                Bquit()
                UIRestD()

            else:
                
                Bquit()
                UIRestD()
                self.assertEqual(1,0)
                
        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case071()

            else:
                self.assertEqual(1,0)


    def test_case072(self):

        "Case_1915 LAN VLAN InterVLAN routing option support"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            # add vlan 60
            tn = telnetlib.Telnet('10.88.1.102')
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
            tn.write("interface 0/"+LAN_PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan participation include 60\r\n")
            time.sleep(2)
            tn.write("vlan tag 60\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            time.sleep(2)
            tn.close
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan')
            time.sleep(2)
            #BclickT('Untagged LAN')
            time.sleep(2)
            Bclick("table.form_table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1)")
            time.sleep(2)
            BclickT("here")
            time.sleep(2)
            BclickT("Proceed")
            time.sleep(2)
            BclickT("New LAN")
            time.sleep(2)
            BfillT("IP Settings","192.168.60.1")
            time.sleep(2)
            BfillT("Name","60","1","1","A")
            time.sleep(2)
            BfillT("VLAN ID","60","1","1","A")
            time.sleep(2)
            BclickT("Enable","5")
            time.sleep(2)
            BclickT("Save")
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.60.1')
            time.sleep(2)
            result1 = stdout.read()
            print('result1',str(result1))
            ssh.close()

            if '4 received' in str(result1):
                driver = Bopen()
                UIsLogin(pepurl)
                time.sleep(2)
                Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan')
                time.sleep(2)
                BclickT('Untagged LAN')
                time.sleep(2)
                BclickT("60")
                time.sleep(2)
                BncheckT("Inter-VLAN routing","1","1","A")
                time.sleep(2)
                BclickT("Save")
                time.sleep(10)
                UIsApply(pepurl)
                time.sleep(AppWait)
                Bquit()

                ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
                time.sleep(2)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.60.1')
                time.sleep(2)
                result2 = stdout.read()
                print('result2',str(result2))
                ssh.close()

                if '0 received' in str(result2):

                    print ('PASSED')
                    # del vlan 60
                    tn = telnetlib.Telnet('10.88.1.102')
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
                    tn.write("interface 0/"+LAN_PORT+"\r\n")
                    time.sleep(2)
                    tn.write("no vlan tagging 60\r\n")
                    time.sleep(2)
                    tn.write("vlan participation auto 60\r\n")
                    time.sleep(2)
                    tn.write("exit\r\n")
                    time.sleep(2)
                    tn.close
                    UIRestD()

                else:

                    self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            # del vlan 60
            tn = telnetlib.Telnet('10.88.1.102')
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
            tn.write("interface 0/"+LAN_PORT+"\r\n")
            time.sleep(2)
            tn.write("no vlan tagging 60\r\n")
            time.sleep(2)
            tn.write("vlan participation auto 60\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            time.sleep(2)
            tn.close
            UIRestD()

            if count <3:
                count+=1
                self.test_case072()

            else:
                self.assertEqual(1,0)


    def test_case073(self):

        "Case_1055 Loggin - Link Down/Up, Health Check fail Logging"

        try:
            a = 0
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?')
            time.sleep(2)
            BclickT('Disconnect')
            BclickT('OK')
            time.sleep(60)
            BclickT('Connect')
            time.sleep(60)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')

            if Bwait_text("WAN: WAN 1 disconnected"):
                a += 1

            if Bwait_text("WAN: WAN 1 connected (10.88.81.1)"):
                a += 1

            if Bwait_text("WAN: WAN 1 disconnected (Manual)"):
                a += 1

            if Bwait_text("WAN: WAN 1 connected (10.88.81.1)"):
                a += 1

            if a == 4:

                print ("PASS")
                Bquit()
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case073()

            else:
                self.assertEqual(1,0)


    def test_case074(self):

        "Case_1057 Loggin - DDNS fail, success logging"

        try:
            a = 0
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/support.cgi')
            time.sleep(2)
            Bclick('#hcfs_panel > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)')
            time.sleep(60)
            Bclick('#hcfs_panel > tr:nth-child(1) > td:nth-child(2) > input:nth-child(2)')
            time.sleep(60)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')

            if Bwait_text("WAN: WAN 1 connected (10.88.81.1)"):
                a += 1

            if Bwait_text("WAN: WAN 1 disconnected (WAN failed DNS test)"):
                a += 1

            if a == 2:
                
                print ("PASS")
                Bquit()
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case074()

            else:
                self.assertEqual(1,0)


    
    def test_case075(self):

        "Case_1058-Logging - automatic refresh, Clear Log"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1) 
            FireWallRlue1399()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
            time.sleep(2)
            BclickT("Clear Log")
            time.sleep(2)

            if not Btext('WAN: WAN 1 connected'):

                ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
                time.sleep(2)
                stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.80.11')
                time.sleep(2)
                t = stdout.read()
                time.sleep(60)
                    
                if Btext('Denied CONN=lan'):

                    print ("PASS")
                    Bquit()
                    UIRestD()

                else:
                    
                    Bquit()
                    UIRestD()
                    self.assertEqual(1,0)

            else:
            
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case075()

            else:
                self.assertEqual(1,0)


    def test_case076(self):

        "Case_1281-Firewall - Firewall rules with space character logging"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1) 
            NAT_Mapping()
            FireWallRlue1400()
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 10.88.80.11')
            time.sleep(2)
            t = stdout.read()

            if '4 received' in str(t):

                Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                time.sleep(2)
                
                if Btext('Allowed CONN'):

                    print ("PASS")
                    Bquit()
                    UIRestD()

                else:

                    Bquit()
                    UIRestD()
                    self.assertEqual(1,0)

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

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
            time.sleep(10)
            RAtoLocal = RA ('192.168.1.1','/GetHwInfo')
                
            if 'serial number: '+SN in RAtoLocal:

                print ("PASS")
                Bquit()
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case077()

            else:
                self.assertEqual(1,0)


    def test_case078(self):

        "Case_1074-Remote Assistance access from LAN/WAN side with password"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            EnableRA()
            Bquit()
            time.sleep(AppWait)
            RAtoRemote = RA (SN,'/GetHwInfo')
            print (RAtoRemote)
            if 'serial number: '+SN in RAtoRemote:

                print ("PASS")
                Bquit()
                UIRestD()
                self.assertEqual(1,1)
                    
            else:
                
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case078()

            else:
                self.assertEqual(1,0)

    
    def test_case080(self):

        "Case_1415 Web Blocking - Default Web Blocking (All Users)"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            driver.delete_all_cookies()
            time.sleep(10)
            UIsLogin(pepurl)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=imp2pblk')
            Bfill('#website_panel > table.grid_table.form_table.web_custom_panel.glue > tbody.matrix_row > tr > td:nth-child(1) > input','peplink.com')
            SBclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            Bquit()
            time.sleep(AppWait)

            driver = webdriver.Chrome()
            driver.get('http://www.peplink.com')
            time.sleep(10)
            
            if 'blocked due to content' in str(driver.page_source):
                print ("PASS")
                driver.quit()
                UIRestD()

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
            UIRestD()
         
            if count <3:
                count+=1
                self.test_case080()

            else:
                self.assertEqual(1,0)


    def test_case081(self):

        "Case_1061 Intrusion Detection and Dos Prevention - Sync Flood Protection"

        try:
            a = 0
            time.sleep(B20Wait)
            driver = Bopen()
            time.sleep(2)
            UIsLogin(pepurl)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            EnableRA()
            Bquit()
            driver = Bopen()
            time.sleep(2)
            UIsLogin(pepurl)
            time.sleep(2)
            Wan_set(1)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=firewall')
            time.sleep(2)
            Bclick('#firewall_settings > table:nth-child(5) > tbody > tr > td:nth-child(2) > button')
            time.sleep(2)
            Bcheck('#ui-id-1 > table > tbody > tr > td:nth-child(2) > label > input[type="checkbox"]')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            time.sleep(AppWait)
            Bquit()


            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S hping3 -i u1000 -S 10.88.81.1 -p 10000 -c 1000")
            time.sleep(2)
            ssh.close()
            time.sleep(10)

            AddkeytoDevice = RA (SN,'addkeyto')
            time.sleep(10)
            RAtoLocal = RA ('192.168.1.1','/test_case081')
            time.sleep(10)
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
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S hping3 -i u12500 -S 10.88.81.1 -p 10000 -c 1000")
            time.sleep(2)
            ssh.close()
            time.sleep(10)

            RAtoLocal = RA ('192.168.1.1','/test_case081')
            #print (RAtoLocal)

            i = re.findall(r'[0-9]+',RAtoLocal)
            print i

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
                UIRestD()


            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()
             
            if count <3:
                count+=1
                self.test_case081()

            else:
                self.assertEqual(1,0)


    def test_case082(self):

        "Case_1062 Intrusion Detection and Dos Prevention - Port Scan Protection"

        try:
            a = 0
            time.sleep(B20Wait)
            driver = Bopen()
            time.sleep(2)
            UIsLogin(pepurl)
            time.sleep(2)
            Wan_set(1)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=firewall')
            time.sleep(2)
            Bclick('#firewall_settings > table:nth-child(4) > tbody > tr > td:nth-child(2) > button')
            time.sleep(2)
            Bcheck('#ui-id-1 > table > tbody > tr > td:nth-child(2) > label > input[type="checkbox"]')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command("echo peplink | sudo -S nmap -v -sS -A 10.88.81.1")
            time.sleep(2)
            result = []
            for std in stdout.readlines():
                result.append(std)

            ssh.close()

            if result[-9] == u'TRACEROUTE (using proto 1/icmp)\n':

                print ("PASS")
                Bquit()
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()
    
            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case082()

            else:
                self.assertEqual(1,0)


    def test_case083(self):

        "Case_1063 Intrusion Detection and Dos Prevention - Ping Flood Protection"

        try:
            a = 0
            time.sleep(B20Wait)
            driver = Bopen()
            time.sleep(2)
            UIsLogin(pepurl)
            time.sleep(2)
            EnableRA()
            Bquit()
            driver = Bopen()
            time.sleep(2)
            UIsLogin(pepurl)
            time.sleep(2)
            Wan_set(1)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=firewall')
            time.sleep(2)
            Bclick('#firewall_settings > table:nth-child(5) > tbody > tr > td:nth-child(2) > button')
            time.sleep(2)
            Bcheck('#ui-id-1 > table > tbody > tr > td:nth-child(2) > label > input[type="checkbox"]')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            time.sleep(AppWait)
            Bquit()
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S hping3 -i u1000 10.88.81.1 --icmp -p 10000 -c 1000")
            time.sleep(2)
            ssh.close()

            time.sleep(10)

            AddkeytoDevice = RA (SN,'addkeyto')
            time.sleep(10)

            RAtoLocal = RA ('192.168.1.1','/test_case083')

            print (RAtoLocal)

            i = re.findall(r'[0-9]+',RAtoLocal)

            print i[15]
            print i[16]

            if i[15] > 50 and i[16] > 1800:

                print ("PASS")
                Bquit()
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)


        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case083()

            else:
                self.assertEqual(1,0)


    def test_case084(self):

        "Case_1064 Intrusion Detection and Dos Prevention - Intrusion Detection and DoS Prevention ON/OFF"

        try:
            time.sleep(B20Wait)
            a = 0
            b = 0
            a1 ="RAHost:192.168.1.1RAPort:2222BusyBoxv1.12.4"
            a2 ="built-inshell(ash)Enter'help'foralistofbuilt-incommands.~#~#iptables-tmangle-nvLIDS_ICMPChainIDS_ICMP"
            
            driver = Bopen()
            time.sleep(2)
            UIsLogin(pepurl)
            time.sleep(2)
            EnableRA()
            Bquit()
            driver = Bopen()
            time.sleep(2)
            UIsLogin(pepurl)
            time.sleep(2)
            Wan_set(1)
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=firewall')
            time.sleep(2)
            Bclick('#firewall_settings > table:nth-child(5) > tbody > tr > td:nth-child(2) > button')
            time.sleep(2)
            Bcheck('#ui-id-1 > table > tbody > tr > td:nth-child(2) > label > input[type="checkbox"]')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            time.sleep(AppWait)
            Bquit()
            
            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S hping3 -i u1000 10.88.81.1 --icmp -p 10000 -c 1000")
            time.sleep(2)
            ssh.close()

            time.sleep(10)

            AddkeytoDevice = RA (SN,'addkeyto')
            time.sleep(10)

            RAtoLocal = RA ('192.168.1.1','/test_case083')

            i = re.findall(r'[0-9]+',RAtoLocal)
            
            print "i[15] ="+str(i[15])
            print "i[16] ="+str(i[16])

            if i[15] == str(1000):
                a += 1
                print a
                
            if i[16] == str(28000):
                b += 1
                print b
                
            if a + b == 2:

                driver = Bopen()
                time.sleep(2)
                UIsLogin(pepurl)
                time.sleep(2)
                Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=firewall')
                time.sleep(2)
                Bclick('#firewall_settings > table:nth-child(5) > tbody > tr > td:nth-child(2) > button')
                time.sleep(2)
                Bncheck('#ui-id-1 > table > tbody > tr > td:nth-child(2) > label > input[type="checkbox"]')
                time.sleep(2)
                BclickT('Save')
                time.sleep(10)
                UIsApply(pepurl)
                time.sleep(AppWait)
                Bquit()
                
                RAtoLocal = RA ('192.168.1.1','/test_case083')
                x = "".join(RAtoLocal.split())
                
                print "x  ="+x
                print "a1 ="+a1
                print "a2 ="+a2

                if (a1 in x) and (a2 in x):

                    print ("PASS")
                    Bquit()
                    UIRestD()

                else:
                
                    Bquit()
                    UIRestD()
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
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=global')
            time.sleep(2)
            Bcheck('#mainContent > div.smart_content > div.service_passthrough_panel > table > tbody > tr:nth-child(4) > td:nth-child(2) > div > label > input')
            time.sleep(2)
            Bfill('#mainContent > div.smart_content > div.service_passthrough_panel > table > tbody > tr:nth-child(4) > td:nth-child(2) > div > div > input:nth-child(1)','2121')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()
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
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case086()

            else:
                self.assertEqual(1,0)


    def test_case087(self):

        "Case_1161 Service Passthrough - PPTP"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=pptp')
            time.sleep(2)
            Bcheck('#pptp_enable_yes')
            time.sleep(2)
            Bcheck('#pptp_form > table > tbody > tr:nth-child(1) > td > table > tbody.pptp_basic_panel > tr:nth-child(1) > td.tablecontent2 > label:nth-child(2) > input')
            time.sleep(2)
            Bcheck('#pptp_form > table > tbody > tr:nth-child(1) > td > table > tbody.pptp_basic_panel > tr:nth-child(3) > td.tablecontent2 > table > tbody > tbody > tr:nth-child(1) > td:nth-child(2) > div.connlist_table_box > label:nth-child(2) > input[type="checkbox"]')
            time.sleep(2)
            Bfill('#pptp_account_panel > div > table > tbody.matrix_row > tr > td:nth-child(1) > input','peplink5978')
            time.sleep(2)
            Bfill('#pptp_account_panel > div > table > tbody.matrix_row > tr > td:nth-child(2) > input[type="password"]','peplink5978')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()

            print 'test start'
            result = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S pon to10-88-81-1")
            time.sleep(30)
            stdin, stdout, stderr = ssh.exec_command("ifconfig ppp0")
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S poff to10-88-81-1")
            time.sleep(2)
            ssh.close()

            for std in stdout.readlines():
                result.append(std)

            if str(result[0]) == u'ppp0      Link encap:Point-to-Point Protocol  \n':

                print result[1]
                driver = Bopen()
                UIsLogin(pepurl)
                Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                if Bwait_text("PPTP: peplink5978/10.88.80.11 connected"):
                #if Bwait_text("PPTP: 192.168.1.10 connected (pptp9)"):

                    print 'pass'
                    Bquit()
                    UIRestD()

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

            if count <3:
                count+=1
                self.test_case087()

            else:
                self.assertEqual(1,0)


    def test_case088(self):

        "Case_1369 PPTP Server - Listen on Default IP (Local user)"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=pptp')
            time.sleep(2)
            Bcheck('#pptp_enable_yes')
            time.sleep(2)
            Bcheck('#pptp_form > table > tbody > tr:nth-child(1) > td > table > tbody.pptp_basic_panel > tr:nth-child(1) > td.tablecontent2 > label:nth-child(2) > input')
            time.sleep(2)
            Bcheck('#pptp_form > table > tbody > tr:nth-child(1) > td > table > tbody.pptp_basic_panel > tr:nth-child(3) > td.tablecontent2 > table > tbody > tbody > tr:nth-child(1) > td:nth-child(2) > div.connlist_table_box > label:nth-child(2) > input[type="checkbox"]')
            time.sleep(2)
            Bfill('#pptp_account_panel > div > table > tbody.matrix_row > tr > td:nth-child(1) > input','peplink5978')
            time.sleep(2)
            Bfill('#pptp_account_panel > div > table > tbody.matrix_row > tr > td:nth-child(2) > input[type="password"]','peplink5978')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()

            print 'test start'
            result = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S pon to10-88-81-1")
            time.sleep(30)
            stdin, stdout, stderr = ssh.exec_command("ifconfig ppp0")
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S poff to10-88-81-1")
            time.sleep(2)
            ssh.close()

            for std in stdout.readlines():
                result.append(std)

            if str(result[0]) == u'ppp0      Link encap:Point-to-Point Protocol  \n':

                print result[1]
                driver = Bopen()
                UIsLogin(pepurl)
                Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                if Bwait_text("PPTP: peplink5978/10.88.80.11 connected"):
                #if Bwait_text("PPTP: 192.168.1.10 connected (pptp9)"):
                    
                    print 'pass'
                    Bquit()
                    UIRestD()

                else:
                    
                    Bquit()
                    UIRestD()
                    self.assertEqual(1,0)

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:
            
            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case088()

            else:
                self.assertEqual(1,0)


    def test_case089(self):

        "Case_1370 PPTP Server - Listen on Addistional public IP Address"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(1)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=pptp')
            time.sleep(2)
            Bcheck('#pptp_enable_yes')
            time.sleep(2)
            Bcheck('#pptp_form > table > tbody > tr:nth-child(1) > td > table > tbody.pptp_basic_panel > tr:nth-child(1) > td.tablecontent2 > label:nth-child(2) > input')
            time.sleep(2)
            Bcheck('#pptp_form > table > tbody > tr:nth-child(1) > td > table > tbody.pptp_basic_panel > tr:nth-child(4) > td.tablecontent2 > table > tbody > tbody > tr:nth-child(1) > td:nth-child(2) > div.connlist_table_box > label:nth-child(2) > input[type="checkbox"]')
            time.sleep(2)
            Bfill('#pptp_account_panel > div > table > tbody.matrix_row > tr > td:nth-child(1) > input','peplink5978')
            time.sleep(2)
            Bfill('#pptp_account_panel > div > table > tbody.matrix_row > tr > td:nth-child(2) > input[type="password"]','peplink5978')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()
            print 'test start'
            result = []
            ssh.connect("10.88.80.11" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S pon to10-88-81-51")
            time.sleep(30)
            stdin, stdout, stderr = ssh.exec_command("ifconfig ppp0")
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S poff to10-88-81-51")
            time.sleep(2)
            ssh.close()

            for std in stdout.readlines():
                result.append(std)

            if str(result[0]) == u'ppp0      Link encap:Point-to-Point Protocol  \n':

                print result[1]
                driver = Bopen()
                UIsLogin(pepurl)
                Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utlog')
                if Bwait_text("PPTP: peplink5978/10.88.80.11 connected"):
                #if Bwait_text("PPTP: 192.168.1.10 connected (pptp9)"):

                    print 'pass'
                    Bquit()
                    UIRestD()

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

            if count <3:
                count+=1
                self.test_case089()

            else:
                self.assertEqual(1,0)


    def test_case090(self):

        "Case_1173-Service Forwarding - Web Proxy (same port)"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundremap')
            time.sleep(2)
            Bclick('#webproxy_forwarding_panel > table > tbody > tr:nth-child(2) > td.tablecontent2 > label > input')
            time.sleep(2)
            Bfill('#webproxy_forwarding_panel > div > table:nth-child(1) > tbody > tr:nth-child(2) > td.tablecontent2 > input:nth-child(1)','10.88.81.254')
            time.sleep(2)
            Bfill('#webproxy_forwarding_panel > div > table:nth-child(1) > tbody > tr:nth-child(2) > td.tablecontent2 > input:nth-child(2)','8080')
            time.sleep(2)
            Bclick('#webproxy_forwarding_panel > div > table:nth-child(2) > tbody.row_panel > tr:nth-child(1) > td:nth-child(2) > input')
            time.sleep(2)
            Bfill('#webproxy_forwarding_panel > div > table:nth-child(2) > tbody.row_panel > tr:nth-child(1) > td:nth-child(3) > input:nth-child(1)','10.88.80.11')
            time.sleep(2)
            Bfill('#webproxy_forwarding_panel > div > table:nth-child(2) > tbody.row_panel > tr:nth-child(1) > td:nth-child(4) > input','8080')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()

            result1 = []
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "echo peplink | sudo -S squidclient -h 10.88.81.254 -p 8080 https://www.peplink.com"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            for std in stdout.readlines():
                result1.append(std)

            result = re.findall(r'<p>(.*?) <a',str(result1[-10]))

            if  result[0] == 'Your cache administrator is':
                
                print ("PASSED")
                ssh.close()
                UIRestD()

            else:
                ssh.close()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case090()

            else:
                self.assertEqual(1,0)


    def test_case091(self):
                      
        "Case_1174-Service Forwarding - Web Proxy (different port)"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundremap')
            time.sleep(2)
            Bclick('#webproxy_forwarding_panel > table > tbody > tr:nth-child(2) > td.tablecontent2 > label > input')
            time.sleep(2)
            Bfill('#webproxy_forwarding_panel > div > table:nth-child(1) > tbody > tr:nth-child(2) > td.tablecontent2 > input:nth-child(1)','10.88.81.254')
            time.sleep(2)
            Bfill('#webproxy_forwarding_panel > div > table:nth-child(1) > tbody > tr:nth-child(2) > td.tablecontent2 > input:nth-child(2)','8888')
            time.sleep(2)
            Bclick('#webproxy_forwarding_panel > div > table:nth-child(2) > tbody.row_panel > tr:nth-child(1) > td:nth-child(2) > input')
            time.sleep(2)
            Bfill('#webproxy_forwarding_panel > div > table:nth-child(2) > tbody.row_panel > tr:nth-child(1) > td:nth-child(3) > input:nth-child(1)','10.88.80.11')
            time.sleep(2)
            Bfill('#webproxy_forwarding_panel > div > table:nth-child(2) > tbody.row_panel > tr:nth-child(1) > td:nth-child(4) > input','8080')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()
            result1 = []
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "echo peplink | sudo -S squidclient -h 10.88.81.254 -p 8888 https://www.peplink.com"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            for std in stdout.readlines():
                result1.append(std)

            result = re.findall(r'<p>(.*?) <a',str(result1[-10]))

            if  result[0] == 'Your cache administrator is':
                
                print ("PASSED")
                ssh.close()
                UIRestD()

            else:

                ssh.close()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case091()

            else:
                self.assertEqual(1,0)


    def test_case092(self):

        "Case_1174-Service Forwarding - Disable,Enable"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundremap')
            time.sleep(2)
            Bclick('#webproxy_forwarding_panel > table > tbody > tr:nth-child(2) > td.tablecontent2 > label > input')
            time.sleep(2)
            Bfill('#webproxy_forwarding_panel > div > table:nth-child(1) > tbody > tr:nth-child(2) > td.tablecontent2 > input:nth-child(1)','10.88.81.254')
            time.sleep(2)
            Bfill('#webproxy_forwarding_panel > div > table:nth-child(1) > tbody > tr:nth-child(2) > td.tablecontent2 > input:nth-child(2)','8888')
            time.sleep(2)
            Bclick('#webproxy_forwarding_panel > div > table:nth-child(2) > tbody.row_panel > tr:nth-child(1) > td:nth-child(2) > input')
            time.sleep(2)
            Bfill('#webproxy_forwarding_panel > div > table:nth-child(2) > tbody.row_panel > tr:nth-child(1) > td:nth-child(3) > input:nth-child(1)','10.88.80.11')
            time.sleep(2)
            Bfill('#webproxy_forwarding_panel > div > table:nth-child(2) > tbody.row_panel > tr:nth-child(1) > td:nth-child(4) > input','8080')
            time.sleep(2)
            BclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()
            result1 = []
            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
            time.sleep(2)
            cmd = "echo peplink | sudo -S squidclient -h 10.88.81.254 -p 8888 https://www.peplink.com"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            time.sleep(2)
            for std in stdout.readlines():
                result1.append(std)

            result = re.findall(r'<p>(.*?) <a',str(result1[-10]))

            if  result[0] == 'Your cache administrator is':
                               
                driver = Bopen()
                UIsLogin(pepurl)
                Bvisit ('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundremap')
                time.sleep(2)
                Bncheck('#webproxy_forwarding_panel > table > tbody > tr:nth-child(2) > td.tablecontent2 > label > input')
                time.sleep(2)
                BclickT('Save')
                time.sleep(10)
                UIsApply(pepurl)
                time.sleep(AppWait)
                Bquit()
                result2 = []
                ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
                time.sleep(2)
                ssh.exec_command('echo peplink | sudo -S killall -9 iperf')
                time.sleep(2)
                cmd = "echo peplink | sudo -S squidclient -h 10.88.81.254 -p 8888 https://www.peplink.com"
                stdin, stdout, stderr = ssh.exec_command(cmd)
                time.sleep(2)
                for std in stdout.readlines():
                    result1.append(std)

                result = re.findall(r'<p>(.*?) <a',str(result2))

                if result == []:

                    print ("PASSED")
                    ssh.close()
                    UIRestD()

                else:

                    ssh.close()
                    UIRestD()
                    self.assertEqual(1,0) 

            else:

                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            ssh.close()
            UIRestD()

            if count <3:
                count+=1
                self.test_case092()

            else:
                self.assertEqual(1,0)


    def test_case094(self):

        "Case_1148 Email Notification Send Notification Email when HC faill, Link Down/UP,Disconnect/Connection manually"

        try:
            a = 0
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            time.sleep(2)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            Wan_set(2)
            Bvisit("http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=uttimesync")
            Bclick("#mainContent > div.smart_content > form > table > tbody > tr:nth-child(2) > td:nth-child(2) > select > option:nth-child(6)")
            BclickT("Save")
            time.sleep(10)
            Bvisit("http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utnotify")
            time.sleep(2)
            Bcheck("#smtp_setup_panel > table > tbody:nth-child(1) > tr.tablecontent2 > td:nth-child(2) > label")
            time.sleep(2)
            Bfill("#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(1) > td:nth-child(2) > input","smtp.gmail.com")
            time.sleep(2)
            Bcheck('#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(1) > td:nth-child(2) > label > input[type="checkbox"]')
            time.sleep(2)
            Bcheck('#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(2) > td:nth-child(2) > label > input[type="checkbox"]')
            time.sleep(2)
            Bfill("#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(4) > td:nth-child(2) > input","lopeplink@gmail.com")
            time.sleep(2)
            Bfill('#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(5) > td:nth-child(2) > input[type="password"]',"peplink5978")
            time.sleep(2)
            Bfill('#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(6) > td:nth-child(2) > input[type="password"]',"peplink5978")
            time.sleep(2)
            Bfill("#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(7) > td:nth-child(2) > input","lopeplink@gmail.com")
            time.sleep(2)
            Bfill("#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(8) > td:nth-child(2) > textarea","lopeplink@gmail.com")
            time.sleep(2)
            BclickT("Save")
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)

            Bvisit("http://192.168.1.1/cgi-bin/MANGA/support.cgi")
            Bclick('#hcfs_panel > tr:nth-child(1) > td.tablecontent2 > input[type="button"]:nth-child(1)')
            time.sleep(60)
            Bclick('#hcfs_panel > tr:nth-child(1) > td.tablecontent2 > input[type="button"]:nth-child(2)')
            time.sleep(60)
            Bvisit("http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=main")
            time.sleep(2)
            BclickT("Disconnect","2")
            time.sleep(2)
            BclickT("OK")
            time.sleep(60)
            BclickT("Connect","2")
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
            time.sleep(2)
            mail.login('lopeplink@gmail.com', 'peplink5978')
            time.sleep(2)
            mail.list()
            time.sleep(2)
            mail.select("inbox")
            time.sleep(2)
            result, data = mail.search(None, "ALL")
            ids = data[0]
            time.sleep(2)
            id_list = ids.split()
            
            latest_email_id = id_list[-6]
            result, data = mail.fetch(latest_email_id, "(RFC822)")
            raw_email1 = data[0][1]

            if "WAN 1: Disconnected (Health check failed)" in raw_email1 and SN +" running "+ FWver in raw_email1:

                a += 1

            latest_email_id = id_list[-4]
            result, data = mail.fetch(latest_email_id, "(RFC822)")
            raw_email2 = data[0][1]

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
                UIRestD()

            else:

                print "Failed"
                Bquit()
                UIRestD()
                self.assertEqual(1,0)


        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case094()

            else:
                self.assertEqual(1,0)


    def test_case096(self):

        "Case_1351 Email Notification - Multiple Email Recepient"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            #UIsLogin(pepurl)
            time.sleep(2)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP = UIStart(pepurl,driver)
            Bvisit("http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=uttimesync")
            time.sleep(2)
            Bclick("#mainContent > div.smart_content > form > table > tbody > tr:nth-child(2) > td:nth-child(2) > select > option:nth-child(6)")
            time.sleep(2)
            BclickT("Save")
            time.sleep(10)
            Bvisit("http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utnotify")
            time.sleep(2)
            Bcheck("#smtp_setup_panel > table > tbody:nth-child(1) > tr.tablecontent2 > td:nth-child(2) > label")
            time.sleep(2)
            Bfill("#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(1) > td:nth-child(2) > input","smtp.gmail.com")
            time.sleep(2)
            Bcheck('#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(1) > td:nth-child(2) > label > input[type="checkbox"]')
            time.sleep(2)
            Bcheck('#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(2) > td:nth-child(2) > label > input[type="checkbox"]')
            time.sleep(2)
            Bfill("#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(4) > td:nth-child(2) > input","lopeplink@gmail.com")
            time.sleep(2)
            Bfill('#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(5) > td:nth-child(2) > input[type="password"]',"peplink5978")
            time.sleep(2)
            Bfill('#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(6) > td:nth-child(2) > input[type="password"]',"peplink5978")
            time.sleep(2)
            Bfill("#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(7) > td:nth-child(2) > input","lopeplink@gmail.com")
            time.sleep(2)
            Bfill("#smtp_setup_panel > table > tbody.smtp_details_panel > tr:nth-child(8) > td:nth-child(2) > textarea","lopeplink@gmail.com,lorancet@peplink.com")
            time.sleep(2)
            BclickT("Save")
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bvisit("http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=utnotify")
            time.sleep(2)
            BclickT("Test Email Notification")
            time.sleep(2)
            BclickT("Send Test Notification")
            time.sleep(60)

            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            time.sleep(2)
            mail.login('lopeplink@gmail.com', 'peplink5978')
            time.sleep(2)
            mail.list()
            time.sleep(2)
            mail.select("inbox")
            time.sleep(2)
            result, data = mail.search(None, "ALL")
            ids = data[0]
            id_list = ids.split()

            latest_email_id = id_list[-1]
            result, data = mail.fetch(latest_email_id, "(RFC822)")
            raw_email = data[0][1]

            if "lorancet@peplink.com" in raw_email and "lopeplink@gmail.com" in raw_email and SN +" running "+ FWver in raw_email:

                print "PASSED"
                Bquit()
                UIRestD()

            else:

                print "Failed"
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

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
            Bvisit("http://192.168.1.1/cgi-bin/MANGA/support.cgi")
            time.sleep(10)
            Bclick("//body/div/div[3]/li[5]/div[1]/input[2]")
            time.sleep(30)
            cmd = 'echo DNS Nslookup'

            for x in range(5):

                subprocess.Popen(cmd, shell=True)
                subprocess.call('nslookup wiki.peplink.com', shell=True)
                print 'nslookup wiki.peplink.com for '+ str(x)
                x =+ 1
                time.sleep(10)

            time.sleep(10)
            Bclick("//body/div/div[3]/li[5]/div[1]/input[3]")
            time.sleep(30)
            Bclick("Download")
            time.sleep(10)
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
            time.sleep(20)

            WAN1_logs = []
            i = 1
            while i <=1:
                try:
                    time.sleep(1)
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
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

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
            Bvisit("http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan")
            Bclick('#mainContent > div.smart_content > form > div.general_settings_panel > table.form_table.dns_panel > tbody.dns_general_panel > tr:nth-child(2) > td:nth-child(2) > input[type="checkbox"]')
            BclickT("Save")
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bvisit("http://192.168.1.1/cgi-bin/MANGA/support.cgi")
            time.sleep(10)
            Bclick("//body/div/div[3]/li[5]/div[1]/input[2]")
            time.sleep(30)

            cmd = 'echo DNS Nslookup'

            for x in range(5):

                subprocess.Popen(cmd, shell=True)
                subprocess.call('nslookup wiki.peplink.com', shell=True)
                print 'nslookup wiki.peplink.com for '+ str(x)
                x =+ 1
                time.sleep(10)

            time.sleep(10)
            Bclick("//body/div/div[3]/li[5]/div[1]/input[3]")
            time.sleep(30)
            Bclick("Download")
            time.sleep(10)
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
            tar.close()
            time.sleep(10)

            WAN1_logs = []
            i = 1
            while i <=1:
                try:
                    time.sleep(1)
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
                UIRestD()

            else:

                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case106()

            else:
                self.assertEqual(1,0)


    def test_case107(self):

        "Case_1826 Captive Portal Open Access"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            time.sleep(2)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            Bvisit("http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=portal")
            time.sleep(2)
            Bclick("#portal_summary_table > tbody > tr.tablecontent4 > td.tabletitle2 > a")
            time.sleep(2)
            Bcheck(".lan_action")
            time.sleep(2)
            BclickT("Save")
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()
            time.sleep(2)
            driver = Bopen()
            time.sleep(2)
            Bvisit("https://www.peplink.com")
            time.sleep(10)
            BclickT("Agree")
            time.sleep(10)
            result = re.findall(r'def_content = "(.+)"',driver.page_source)
            print result[0]
            time.sleep(10)
            if "Continue Browsing" == str(result[0]):

                print "PASSED"
                Bquit()
                UIRestD()

            else:

                print "Failed"
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case107()

            else:
                self.assertEqual(1,0)


    def test_case109(self):

        "Case_1907 Captive Portal with Walled garden support"

        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            os.system('nmcli device disconnect ens19')
            time.sleep(2)
            time.sleep(2)
            Bvisit("http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=portal")
            time.sleep(2)
            Bclick("#portal_summary_table > tbody > tr.tablecontent4 > td.tabletitle2 > a")
            time.sleep(2)
            Bcheck(".lan_action")
            time.sleep(2)
            Bfill("#white_list > table > tbody.matrix_row > tr > td:nth-child(1) > input","www.peplink.com")
            time.sleep(2)
            BclickT("Save")
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()
            time.sleep(2)
            driver = Bopen()
            Bvisit("https://www.google.com")
            time.sleep(10)
            print driver.page_source
            if "Agree" in str(driver.page_source):
                Bquit()
                driver = Bopen()
                time.sleep(2)
                Bvisit("https://www.peplink.com")
                time.sleep(10)
                result = re.findall(r'<title>(.+)</title>',driver.page_source)
                print result[0]

                if "Peplink SD-WAN. Protecting Business Continuity." == str(result[0]):

                    print "PASSED"
                    Bquit()
                    UIRestD()

                else:

                    print "Failed"
                    Bquit()
                    UIRestD()
                    self.assertEqual(1,0)

            else:

                print "Failed"
                Bquit()
                UIRestD()
                self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case109()

            else:
                self.assertEqual(1,0)


    def test_case121(self):

        "Case_2215-Outbound Policy Outbound FastestResponse LAN / WAN"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)
            Wan_set(2)
            #set_Outbound_Policy_fastest_response
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
            SBclickT('Add Rule')
            time.sleep(2)
            Bfill('#ui-id-3 > table > tbody.custom > tr:nth-child(1) > td:nth-child(2) > input','FastestResponse')
            time.sleep(2)
            Bclick('#ui-id-3 > table > tbody.custom > tr:nth-child(4) > td:nth-child(2) > div > select > option:nth-child(1)')
            time.sleep(2)
            Bclick('#ui-id-3 > table > tbody.algo_sel_panel > tr > td:nth-child(2) > select > option:nth-child(8)')
            time.sleep(2)
            Bcheck('#ui-id-3 > table > tbody.algo_panel.least_used.lowest_latency.fastest_response > tr > td:nth-child(2) > div > div:nth-child(1) > label > input[type="checkbox"]')
            time.sleep(2)
            Bcheck('#ui-id-3 > table > tbody.algo_panel.least_used.lowest_latency.fastest_response > tr > td:nth-child(2) > div > div:nth-child(2) > label > input[type="checkbox"]')
            time.sleep(2)
            SBclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()
            ssh.connect('10.88.81.254' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S tc qdisc add dev ens21 root netem delay 30ms 10ms loss 0.3')
            time.sleep(10)

            ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            ssh.exec_command("echo peplink | sudo -S nohup python PogoU64.py W7 &> log/out.tmp&")
            time.sleep(2)
            ssh.connect('192.168.1.9' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L7 10.88.80.11 1000')
            time.sleep(2)
            for std in stdout.readlines():
                r = std,

            ssh.connect('10.88.81.254' , username="peplink" , password="peplink")
            time.sleep(2)
            ssh.exec_command('echo peplink | sudo -S tc qdisc del dev ens21 root netem delay 30ms 10ms loss 0.3')
            time.sleep(2)
            ssh.close()
            print r[0]
            result = r[0]

            if ast.literal_eval(result)['10.88.81.1'] >= 950:
                print ast.literal_eval(result)['10.88.81.1']
                UIRestD()

            else:

                UIRestD()
                self.assertEqual(1,0)


        except:

            global count
            try:
                Bquit()

            except:
                a=0
            UIRestD()

            if count <3:
                count+=1
                self.test_case121()

            else:
                self.assertEqual(1,0)


    def test_case122(self):

        "Case_2216-Outbound Policy Outbound FastestResponse VLAN / WAN"
        try:
            time.sleep(B20Wait)
            driver = Bopen()
            UIsLogin(pepurl)

             # add vlan 60
            tn = telnetlib.Telnet('10.88.1.102')
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
            tn.write("interface 0/"+LAN_PORT+"\r\n")
            time.sleep(2)
            tn.write("vlan participation include 60\r\n")
            time.sleep(2)
            tn.write("vlan tag 60\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            time.sleep(2)
            tn.close
            time.sleep(2)
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan')
            time.sleep(2)
            #BclickT('Untagged LAN')
            time.sleep(2)
            Bclick("table.form_table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1)")
            time.sleep(2)
            BclickT("here")
            time.sleep(2)
            BclickT("Proceed")
            time.sleep(2)
            BclickT("New LAN")
            time.sleep(2)
            BfillT("IP Address","192.168.60.1")
            time.sleep(2)
            BfillT("Name","60","1","1","A")
            time.sleep(2)
            BfillT("VLAN ID","60","1","1","A")
            time.sleep(2)
            BclickT("Enable","5")
            time.sleep(2)
            BclickT("Save")

            Wan_set(2)
            #set_Outbound_Policy_fastest_response
            Bvisit('http://192.168.1.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
            SBclickT('Add Rule')
            time.sleep(2)
            Bfill('#ui-id-3 > table > tbody.custom > tr:nth-child(1) > td:nth-child(2) > input','FastestResponse')
            time.sleep(2)
            Bclick('#ui-id-3 > table > tbody.custom > tr:nth-child(4) > td:nth-child(2) > div > select > option:nth-child(1)')
            time.sleep(2)
            Bclick('#ui-id-3 > table > tbody.algo_sel_panel > tr > td:nth-child(2) > select > option:nth-child(8)')
            time.sleep(2)
            Bcheck('#ui-id-3 > table > tbody.algo_panel.least_used.lowest_latency.fastest_response > tr > td:nth-child(2) > div > div:nth-child(1) > label > input[type="checkbox"]')
            time.sleep(2)
            Bcheck('#ui-id-3 > table > tbody.algo_panel.least_used.lowest_latency.fastest_response > tr > td:nth-child(2) > div > div:nth-child(2) > label > input[type="checkbox"]')
            time.sleep(2)
            SBclickT('Save')
            time.sleep(10)
            UIsApply(pepurl)
            time.sleep(AppWait)
            Bquit()

            ssh.connect("192.168.1.9" , username="peplink" , password="peplink")
            time.sleep(2)
            stdin, stdout, stderr = ssh.exec_command('ping -c 4 192.168.60.9')
            time.sleep(2)
            result1 = stdout.read()
            print('result1',str(result1))
            ssh.close()

            if '4 received' in str(result1):

                ssh.connect('10.88.81.254' , username="peplink" , password="peplink")
                time.sleep(2)
                ssh.exec_command('echo peplink | sudo -S tc qdisc add dev ens21 root netem delay 30ms 10ms loss 0.3')
                time.sleep(10)
                ssh.connect('10.88.80.11' , username="peplink" , password="peplink")
                time.sleep(2)
                ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
                time.sleep(2)
                ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
                time.sleep(2)
                ssh.exec_command("echo peplink | sudo -S nohup python PogoU64.py W7 &> log/out.tmp&")
                time.sleep(2)
                ssh.connect('192.168.60.9' , username="peplink" , password="peplink")
                time.sleep(2)
                ssh.exec_command('echo peplink | sudo -S rm log/*.* -f') # 清除 Log 目錄
                time.sleep(2)
                ssh.exec_command('echo peplink | sudo -S killall python') # 清除 python 所有執行序
                time.sleep(2)
                stdin, stdout, stderr = ssh.exec_command('echo peplink | sudo -S nohup python PogoU64.py L7 10.88.80.11 1000')
                time.sleep(2)
                for std in stdout.readlines():
                    r = std,

                ssh.connect('10.88.81.254' , username="peplink" , password="peplink")
                time.sleep(2)
                ssh.exec_command('echo peplink | sudo -S tc qdisc del dev ens21 root netem delay 30ms 10ms loss 0.3')
                time.sleep(2)

                # del vlan 60
                tn = telnetlib.Telnet('10.88.1.102')
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
                tn.write("interface 0/"+LAN_PORT+"\r\n")
                time.sleep(2)
                tn.write("no vlan tagging 60\r\n")
                time.sleep(2)
                tn.write("vlan participation auto 60\r\n")
                time.sleep(2)
                tn.write("exit\r\n")
                time.sleep(2)
                tn.close

                ssh.close()
                print r[0]
                result = r[0]

                if ast.literal_eval(result)['10.88.81.1'] >= 950:

                    print ('PASS')
                    UIRestD()

                else:

                    print ('Failed')
                    UIRestD()
                    self.assertEqual(1,0)

        except:

            global count
            try:
                Bquit()

            except:
                a=0
            # del vlan 60
            tn = telnetlib.Telnet('10.88.1.102')
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
            tn.write("interface 0/"+LAN_PORT+"\r\n")
            time.sleep(2)
            tn.write("no vlan tagging 60\r\n")
            time.sleep(2)
            tn.write("vlan participation auto 60\r\n")
            time.sleep(2)
            tn.write("exit\r\n")
            time.sleep(2)
            tn.close
            UIRestD()

            if count <3:
                count+=1
                self.test_case122()

            else:
                self.assertEqual(1,0)

    
if __name__ == '__main__':

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
    time.sleep(2)
    os.system('nmcli device connect ens18')
    time.sleep(2)


    #time.sleep(3600)

    a = os.popen('ifconfig ens18').read()
    time.sleep(2)
    result = re.findall(ur'(?:[0-9a-fA-F]:?){12}',a)
    PC_MAC = str.upper(result[0])
    os.system('ping -c 4 192.168.1.9')
    time.sleep(2)
    b = os.popen('arp -a |grep 192.168.1.9').read()
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
            time.sleep(2)
            os.system('nmcli device connect ens18')

    os.chdir("/home/peplink/QA/QaPythonTemp/QaAutoRunTest/U64_Smoke_Test")
    ReportSfolder = 'Report/'
    ReportDfolder = '/QAreport/SmokeTestReportAuto/'

    time.sleep(30)
    if PogoFolderUpload(ReportSfolder,ReportDfolder): # 上傳 log
        filelist = glob.glob(ReportSfolder+'*.*') #刪本地 log
        for f in filelist:
            print 'Deleting file: ' + f
            os.remove(f)
    
