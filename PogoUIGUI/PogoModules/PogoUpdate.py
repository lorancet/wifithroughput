# coding=UTF-8
PogoUpdateVer = '2017/5/17 v1.0.4'

'''
Pogo Module Update 工具

建議放在程式最前方
from PogoModules.PogoUpdate import *

需要 ftputil

2017/5/17 v1.0.4 取消 delay 2 sec 語法修改
2017/1/18 v1.0.3 __init__.py 一併檢查
2016/8/25 v1.0.2 一些修正
2016/8/24 v1.0.1 自動判斷是否為單獨或模組式執行
2016/8/24 v1.0.0 first release

'''


import ftputil,time,os


UpdateHost = '10.88.1.199'
UpdateUname = 'pogopyupdate'
UpdateUpass = 'surTaMtbMy97E'
UpdateSfolder = '/PogoPythonTemp/PogoAutoWorkTemp/PogoModules/'
UpdateDfolder = 'PogoModules/'

UpdateCount = 0

def PogoFTP():
    try:
        ftp = ftputil.FTPHost(UpdateHost,UpdateUname,UpdateUpass)
        if ftp:
            print 'Update Server Success Connect!!'        
            return ftp
    except:
        print 'Update process Fail!! Update Server can not connect !!'
        return 0


def PogoUpdate(ftp,fname,UpdateSfolder,UpdateDfolder):
    if ftp.download_if_newer(UpdateSfolder+fname ,UpdateDfolder+fname):
        print fname + ' have new Version !! Success Update!!'
        return 1
    else:
        print fname + ' is up to date, no update need!!'
        return 0



if not os.path.exists(UpdateDfolder):
    UpdateDfolder = ''


ftp = PogoFTP()
if ftp != 0:
    UpdateCount += PogoUpdate(ftp,'__init__.py',UpdateSfolder,UpdateDfolder)
    UpdateCount += PogoUpdate(ftp,'PogoPeplink.py',UpdateSfolder,UpdateDfolder)
    UpdateCount += PogoUpdate(ftp,'PogoUI.py',UpdateSfolder,UpdateDfolder)
    UpdateCount += PogoUpdate(ftp,'PogoUpdate.py',UpdateSfolder,UpdateDfolder)
    ftp.close()


if UpdateCount != 0:
    print 'for make sure all module can 100% update, will STOP the program, please restart again!!'
    raise SystemExit
