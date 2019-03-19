# coding=UTF-8

from PogoModules.PogoUpdate import *
import ftputil,time,os,socket

UpdateHost = 'file.peplink-ttc.com'
UpdateUname = 'pogopyupdate'
UpdateUpass = 'surTaMtbMy97E'
UpdateSfolder = '/QaPythonTemp/QaAutoRunTest/U64_Smoke_Test/SmokTestModules/'
UpdateDfolder = 'SmokTestModules/'
UpdateCount = 0
  
if not os.path.exists(UpdateDfolder):
    UpdateDfolder = ''

ftp = PogoFTP()
if ftp != 0:
    UpdateCount += PogoUpdate(ftp,'__init__.py',UpdateSfolder,UpdateDfolder)
    UpdateCount += PogoUpdate(ftp,'modules.py',UpdateSfolder,UpdateDfolder)
    UpdateCount += PogoUpdate(ftp,'LoSmokTest_PEPLINK.py',UpdateSfolder,UpdateDfolder)
    UpdateCount += PogoUpdate(ftp,'LoSmokTest_PEPWAVE.py',UpdateSfolder,UpdateDfolder)
    UpdateCount += PogoUpdate(ftp,'LoSmokeUpdate.py',UpdateSfolder,UpdateDfolder)
    ftp.close()

if UpdateCount != 0:
    print 'for make sure all module can 100% update, will STOP the program, please restart again!!'
    raise SystemExit
