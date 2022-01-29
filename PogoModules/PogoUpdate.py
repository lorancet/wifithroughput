# coding=UTF-8
PogoUpdateVer = '2019/10/9 v2.0.0'

'''
Pogo Module Update 工具

建議放在程式最前方
from PogoModules.PogoUpdate import *

需要 ftputil

2019/10/9 v2.0.0 與 Python3 版本合併, 直接相容 Python 2 & 3
2019/2/25 v1.0.16 修正 PogoUpdateF 目錄判斷錯誤 
2019/2/21 v1.0.15 更改 PogoUpdateF 運作方式, 可設定來源與目的目錄比對
2018/11/1 v1.0.14 全部 UpdateHost domain 相關改用 PogoServerIp()
2018/10/30 v1.0.13 增加 UpddateIP , 有時 DNS 異常, 直接給IP的備案
2018/3/2 v1.0.12 增加連動 Update Server 功能
2018/2/26 v1.0.11 改用 domain file.peplink-ttc.com 來當更新位置
2017/9/14 v1.0.10 PogoFolderUpload return 值
2017/9/8 v1.0.9 PogoFolderUpload bug fix
2017/8/25 v1.0.8 增加 PogoFolderUpload
2017/7/26 v1.0.7 增加 PogoUpdateF 更新整個目錄的語法
2017/6/6 v1.0.6 remote display error message
2017/6/5 v1.0.5 PogoUpdate1 簡化指令
2017/5/17 v1.0.4 取消 delay 2 sec 語法修改
2017/1/18 v1.0.3 __init__.py 一併檢查
2016/8/25 v1.0.2 一些修正
2016/8/24 v1.0.1 自動判斷是否為單獨或模組式執行
2016/8/24 v1.0.0 first release

'''


import ftputil,time,os,socket


UpdateHost = 'file.peplink-ttc.com'
UpddateIP = '10.88.1.198'
UpdateUname = 'pogopyupdate'
UpdateUpass = 'surTaMtbMy97E'
UpdateSfolder = '/PogoPythonTemp/PogoAutoWorkTemp/PogoModules/'
UpdateDfolder = 'PogoModules/'


UpdateCount = 0


def PogoServerDomain():
    return UpdateHost

def PogoServerIp():
    try:
    	ip = socket.gethostbyname(UpdateHost)
    except:
        print('DNS server can not get ' + UpdateHost + ' value , now use static IP')
        ip = UpddateIP
    return ip
        

def PogoServerId():
    return UpdateUname

def PogoServerPass():
    return UpdateUpass
    
    


def PogoFTP():
    try:
        ftp = ftputil.FTPHost(PogoServerIp(),UpdateUname,UpdateUpass)
        if ftp:
            print('Update Server Success Connect!!')        
            return ftp
    except Exception as e :
        print('Update process Fail!! Update Server can not connect !!')
        print('-----Error!!-----')
        return 0


def PogoUpdate(ftp,fname,UpdateSfolder,UpdateDfolder):
    try:
        
        if ftp.download_if_newer(UpdateSfolder+fname ,UpdateDfolder+fname):
            print(fname + ' have new Version !! Success Update!!')
            return 1
        else:
            print(fname + ' is up to date, no update need!!')
            return 0

    except Exception as e:
        print('Update process Fail!!')
        print('-----Error!!-----')
        return 0

def PogoUpdate1(fname,UpdateSfolder,UpdateDfolder):
    
    UpdateCount = 0

    ftp = PogoFTP()
    if ftp != 0:
        UpdateCount += PogoUpdate(ftp,fname,UpdateSfolder,UpdateDfolder)        
        ftp.close()

    if UpdateCount != 0:
        print('for make sure all module can 100% update, will STOP the program, please restart again!!')
        raise SystemExit

def PogoUpdateF(UpdateSfolder,UpdateDfolder):

    '''
    檢查整個目錄, 進行更新

    範例

    # coding=UTF-8

    from PogoModules.PogoUpdate import *

    UpdateSfolder = 'QaPythonTemp/QaAutoRunTest/UnitTest_Smoke_Test'
    UpdateDfolder = 'testx'

    PogoUpdateF(UpdateSfolder,UpdateDfolder)
    
    '''
    
    UpdateCount = 0

    ftp = PogoFTP()

    if ftp != 0:         
        subdd = ''
        count = 0
        for item in ftp.walk(UpdateSfolder):

            if count == 0:
                print('1')
                print(item)
                rootf = item[0]
                print('rootf')
                print(rootf)
            count += 1

            DestF = UpdateDfolder + item[0].replace(rootf,'')

            try:
                if os.makedirs(DestF):
                     print(("Creating dir " + DestF))                 
            except Exception as e :
                print(("Exist dir "  + DestF))    

            for subdir in item[1]:
                print(("Subdirs " +  subdir))
              
                    
            for file in item[2]:
                
                if ftp.download_if_newer(ftp.path.join(item[0],file),  os.path.join(DestF,file)):
                    UpdateCount += 1
                    print((r"Updating File {0} || {1}".format(item[0], file)))
                else:
                    print((r"no Change File {0} || {1}".format(item[0], file)))
                
        ftp.close()
    
    if UpdateCount != 0:
        print('for make sure all module can 100% update, will STOP the program, please restart again!!')
        raise SystemExit    






def PogoFolderUpload(localDir, ftpDir):

    def upload_dir(localDir, ftpDir): 
        list = os.listdir(localDir)
        for fname in list:
            if os.path.isdir(localDir + fname):             
                if(ftp.path.exists(ftpDir + fname) != True):                   
                    ftp.mkdir(ftpDir + fname)
                    print((ftpDir + fname + " is created."))
                upload_dir(localDir + fname + "/", ftpDir + fname + "/")
            else:               
                if(ftp.upload_if_newer(localDir + fname, ftpDir + fname)):
                    print((ftpDir + fname + " is uploaded."))
                else:
                    print((localDir + fname + " has already been uploaded."))


    ftp = PogoFTP()
    if ftp != 0:
        upload_dir(localDir, ftpDir)
        return 1
    else:
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
    print('for make sure all module can 100% update, will STOP the program, please restart again!!')
    raise SystemExit
