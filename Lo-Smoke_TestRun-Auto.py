# coding=UTF-8
# 20190214 新增自動同步更新

import os,time,platform
from subprocess import Popen, call, PIPE, STDOUT
from datetime import datetime , timedelta
from threading import Timer
from PogoModules.PogoUpdate import *
from SmokTestModules.LoSmokeUpdate import *
from SmokTestModules.modules import *
from PogoModules.PogoUI import *
from PogoModules.PogoPeplink import *

PogoUpdate1('Lo-Smoke_TestRun-Auto.py','/QaPythonTemp/QaAutoRunTest/U64_Smoke_Test/','')

def testrun(cmd):
    testrun = Popen(cmd , shell = True, stdout=PIPE, stderr=STDOUT)
    testout = ''       

    #with screen out
    for line in iter(testrun.stdout.readline,''):
        testout = testout + line + '\n'
        print (line),
        sys.stdout.flush()
    testrun.wait()


    #without screen out
    #testout = testrun.communicate()[0]

    return testout

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        hrs, mins2 = divmod(mins, 60)
        timeformat = '{:02d}:{:02d}:{:02d}'.format(hrs, mins2, secs)
        #print(timeformat, end ='\r')
        print '\r' + timeformat
        sys.stdout.flush()
        time.sleep(1)
        t -= 1
    print('Time UP!!\n\n\n\n\n')

def autopogoupgrade():

    global upstatus

    print ('Auto firmware Upgrade Processing..')

    upstatus = False
    
    os.chdir("/home/peplink/QA/QaPythonTemp/QaAutoRunTest/U64_Smoke_Test")

    testout = testrun('python2.7 pogoupgrade.py 1')
    
    if 'for make sure all module can 100% update, will STOP the program, please restart again!!' in testout:
        print ('Auto firmware Upgrade program has update, restart after 60 sec')
        Bsleep (60)
        print ('Auto firmware Upgrade Processing..RUN after upgrade')
        testout = testrun('python pogoupgrade.py 1')


    if 'Devcie upgrade firmware to: ' in testout:
        print ('Auto firmware Upgrade Sucess!!')
        upstatus = True
    else:
        print ('Auto firmware Upgrade Fail!!')
    print (upstatus)
    
    os.chdir("/home/peplink/QA/QaPythonTemp/QaAutoRunTest/U64_Smoke_Test")
            
def SmokeTest():

    if upstatus == True:
        
        os.system('nmcli device disconnect ens19')
        time.sleep(2)
        os.system('nmcli device connect ens19')
        time.sleep(2)
        os.system('nmcli device disconnect ens18')
        time.sleep(2)
        os.system('nmcli device connect ens18')
        time.sleep(2)
        
        try:
        
            if subprocess.check_output( 'ping 192.168.50.1 -c 4', shell = True):
            
                IpAdd = '192.168.50.1'
        
        except:
        
            IpAdd = '192.168.1.1'
    
        print IpAdd
            
        pepurl = 'http://'+IpAdd #http:// + 設備IP
        driver = Bopen()
        HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac,SN,UP = UIStart(pepurl,driver)
        Bquit()

        print ('HWmode is ',HWmode)
        
        print ('Device Upgraded, Smoketest Processing..')
        testout = testrun('python2.7 ' + HWmodels + '_Smoke_Test_Balance.py')

        if 'for make sure all module can 100% update, will STOP the program, please restart again!!' in testout:
                print ('Smoketest program has update, restart after 60 sec')
                Bsleep (60)
                testout = testrun('python2.7 ' + HWmodels + '_Smoke_Test_Balance.py')
            
    else:
        print ('Device not Upgrade, skip Smoketest!!')



if __name__ == '__main__':

    autotest = True
          
    while autotest is True:
        if len (sys.argv) == 1:
                autotest = False
                secs = 0

        elif len (sys.argv) == 2:
                testhour = int(sys.argv[1])                  
                x=datetime.today()
                print (x)

                x1 = x + timedelta(days=1) 
                y=x1.replace(day= x1.day, hour=testhour, minute=0, second=0, microsecond=0)

                delta_t=y-x

                secs=delta_t.seconds+1
               
        print ('Auto firmware Upgrade will start after:')
        Timer(secs, autopogoupgrade).start()        
        Timer(secs+900 , SmokeTest).start()
        print ('Auto Throughput  will start after:')
        countdown(secs)
        