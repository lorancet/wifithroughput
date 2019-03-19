# coding=UTF-8

PogoUpgradeVer = '2018/3/30 v5.1.7'

'''
Pogo Firmware Upgrade

!! linux 需要 cifs-utils 套件 & 先建一個 autofirmare 的空目錄!!

2018/3/30 v5.1.7 bug fix
2018/3/29 v5.1.6 改 renew IP 用 nmcli
2018/3/27 v5.1.5 BixThroughput Linux 支援
2018/3/12 v5.1.4 bug fix
2018/3/9 v5.1.3 bug fix
2018/3/7 v5.1.2 bug fix
2018/3/5 v5.1.1 改良 linux 的目錄取得方式
2018/3/2 v5.1.0 Linux 相容
2018/1/15 v5.0.9 bug fix
2018/1/15 v5.0.8 執行後面加變數 2 為配合 multiwan 的 BIX throughput 自動測試升級用
2018/1/8 v5.0.7 執行後面加變數即不會出現完成後等待, 先用 1 , 其實是有變數就不等
2017/10/2 v5.0.6 log 與 顯示加強
2017/9/25 v5.0.5 upload 等待時間再加長
2017/9/21 v5.0.4 BxAC 也歸入慢速機
2017/9/20 v5.0.3 增加 RC 版本判斷 renew IP 
2017/9/20 v5.0.2 版本 check 
2017/9/20 v5.0.1 判斷小設備增加上傳等待時間
2017/9/19 v5.0 配合最新 PogoModule 重新改寫
2016/1/22 v4.0 改寫 整合 PogoModule
V3.10: 增加 Fusion Hub 辦識
V3.9: 增加 HD2 Mini 辦識
V3.8: 增加 MediaFast 辦識
V3.7: 改寫 HW 辦識
V3.6: 更新HW辦識
V3.5: 檔名配合 6.3 , 又有新HW.. OOXX
V3.4: 加入 M700 HW3 判斷, 更新 Pogo UI
V3.3: 修正 710 HW3 誤判
V3.2: 修正 B2500 誤判 X86
V3.1: 加入 抓取 當前 firmware 版本功能
V3.0: first release
'''
import os,time,sys,platform
from subprocess import Popen, call, PIPE, STDOUT
SSHP = 'peplink'

def RenewIP(SSHP = 'peplink'):

    if platform.system() == 'Windows':
        Popen('ipconfig /release',shell=True).wait()
        time.sleep(2)
        Popen('ipconfig /renew',shell=True).wait()
        time.sleep(2)           


    elif platform.system() == 'Linux':    
        niclist = os.listdir('/sys/class/net/')
        for nic in niclist:            
            Popen('nmcli device disconnect ' + nic ,shell=True).wait()
            print nic + '[Down]'
            time.sleep(10)
            Popen('nmcli device connect ' + nic ,shell=True).wait()
            print nic + '[Up]'
            time.sleep(10)
    
RenewIP()
time.sleep(10)


if len (sys.argv) != 1:
    if str(sys.argv[1]) == '2': # BIX throughput 的雙網卡配置
        if platform.system() == 'Windows':
            call('route change 0.0.0.0 mask 0.0.0.0 10.88.11.254 metric 2')
            call('route add 1.1.1.0 mask 255.255.255.0 192.168.1.1')
            call('route add 2.1.1.0 mask 255.255.255.0 192.168.1.1')
            call('route add 3.1.1.0 mask 255.255.255.0 192.168.1.1')
            call('route add 4.1.1.0 mask 255.255.255.0 192.168.1.1')
            call('route add 5.1.1.0 mask 255.255.255.0 192.168.1.1')
            call('route add 6.1.1.0 mask 255.255.255.0 192.168.1.1')
            call('route add 7.1.1.0 mask 255.255.255.0 192.168.1.1')
            call('route add 8.1.1.0 mask 255.255.255.0 192.168.1.1')
            call('route add 192.168.2.0 mask 255.255.255.0 192.168.1.1')

        elif platform.system() == 'Linux':
            SSHP = 'peplink'
            #call('echo '+SSHP+'| sudo -S route add -net default gw 10.88.11.254 netmask 0.0.0.0 metric 2',shell=True)
            call('echo '+SSHP+'| sudo -S route del default gw 192.168.1.1',shell=True)
            call('echo '+SSHP+'| sudo -S route add -net 1.1.1.0 netmask 255.255.255.0 gw 192.168.1.1',shell=True)
            call('echo '+SSHP+'| sudo -S route add -net 2.1.1.0 netmask 255.255.255.0 gw 192.168.1.1',shell=True)
            call('echo '+SSHP+'| sudo -S route add -net 3.1.1.0 netmask 255.255.255.0 gw 192.168.1.1',shell=True)
            call('echo '+SSHP+'| sudo -S route add -net 4.1.1.0 netmask 255.255.255.0 gw 192.168.1.1',shell=True)
            call('echo '+SSHP+'| sudo -S route add -net 5.1.1.0 netmask 255.255.255.0 gw 192.168.1.1',shell=True)
            call('echo '+SSHP+'| sudo -S route add -net 6.1.1.0 netmask 255.255.255.0 gw 192.168.1.1',shell=True)
            call('echo '+SSHP+'| sudo -S route add -net 7.1.1.0 netmask 255.255.255.0 gw 192.168.1.1',shell=True)
            call('echo '+SSHP+'| sudo -S route add -net 8.1.1.0 netmask 255.255.255.0 gw 192.168.1.1',shell=True)
            call('echo '+SSHP+'| sudo -S route add -net 192.168.2.0 netmask 255.255.255.0 gw 192.168.1.1',shell=True)

        time.sleep(10)




from PogoModules.PogoUpdate import *
PogoUpdate1('pogoupgrade.py','/PogoPythonTemp/PogoAutoWorkTemp/FirmwareTool/','') 


from PogoModules.PogoUI import *
from PogoModules.PogoPeplink import *

from datetime import datetime

AllVer = 'PogoUpgrade: ' + PogoUpgradeVer + '\n' + 'PogoPeplink: ' + PogoPeplinkVer + '\n' + 'PogoUI: ' + PogoUIVer
print AllVer


if __name__ == "__main__":
        
    runTime = datetime.now()
    logTime = datetime.strftime(runTime, '%Y-%m-%d-%H%M') # 給Log檔名用的時間格式
    logTime2 = datetime.strftime(runTime, '%Y/%m/%d') # Log 轉入 Google & Excel 用的時間格式    
    logname = logTime
    logfile = logname + ".log" 
    log = file('log/'+logfile, 'w')

    log.write (AllVer)
    log.write('\n\n')

    if platform.system() == 'Windows':
        firmwarefolder = 'Z:\\autofirmware\\'
    elif platform.system() == 'Linux':
        cmd = 'echo '+SSHP+'| sudo -S mount -t cifs -r -o username=' + PogoServerId() + ',password=' + PogoServerPass() + ' //' + PogoServerIp() + '/Share/autofirmware autofirmware'
        Popen(cmd, shell=True).wait()
        firmwarefolder = 'autofirmware/'


    FX86,FBx10,FSurf,FMOTG,FPPC,FBx0,FM700,FX64,FBR,FFH,FBR1AC =  FWFile('N',firmwarefolder) # firmware 路徑

            
    try:
        ipFile = file('pogoupgrade.txt','r')
    except:
        msg =  "Error: pogoupgrade.txt Open Failed!"
        log.write (msg)
        print msg
        sys.exit(1)

    driver = Bopen() 

    for line in ipFile:
        IpAdd = line.strip('\r\n')
        pepurl = 'http://'+IpAdd #http:// + 設備IP
        Mtype = 'None'

        msg = IpAdd
        log.write('\n')
        log.write (msg)
        log.write('\n')
        print msg        
        
        if  PingCheck(IpAdd) == 1:
            
            try:                
                SWver, HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,LANmac = UIStartUP(pepurl,driver)
                FWver1 = re.findall(r'(.*) build',FWver)[0]
                print FWver1

                try:
                    FWver2 = re.findall(r' build (.*)',FWver)[0]
                except:
                    FWver2 = None 
                
                print FWver2
                FWF = FWMapping(Mtype)
                if platform.system() == 'Linux':
                    FWF = os.getcwd() + '/' + FWF
                print FWF

                if FWver1 in FWF and FWver2 is None :  # Daily Build Check
                    msg = 'Device already hast last firmware : ' + FWver1
                    log.write (msg)
                    log.write('\n')
                    print msg                    
                    continue
                
                elif FWver1 in FWF and FWver2 in FWF :  # RC Build Check
                    msg =  'Device already hast last firmware : ' + FWver1 + ' Build ' +  FWver2
                    log.write (msg)
                    log.write('\n')
                    print msg                    
                    continue                         

                else:
                    FWUpgrade(pepurl, FWF)
                    msg = 'Devcie upgrade firmware from: ' + FWver
                    log.write (msg)
                    log.write('\n')
                    print msg                    
                    msg = 'Devcie upgrade firmware to: ' + FWF
                    log.write (msg)
                    log.write('\n')
                    print msg       


                    
                    if any(x in Mtype for x in ('Bx0','M700','HD2','BR','MOTG','Surf','BxAC')):
                        Bsleep(90)
                    else:
                        Bsleep(60)
            except:
                msg = 'Error: ' + IpAdd
                log.write (msg)
                log.write('\n')
                print msg
        else:
                msg = 'Not found: ' + IpAdd
                log.write (msg)
                log.write('\n')
                print msg            
         
        time.sleep(1)
        
    Bquit()
    log.close()
    log = file('log/'+logfile, 'r')
    info = log.read()
    print '\n'
    print '=[ Log File ]================================================================'
    print '\n'
    print info
    log.close()
    if len (sys.argv) == 1:
        raw_input('Press enter to continue: ')






