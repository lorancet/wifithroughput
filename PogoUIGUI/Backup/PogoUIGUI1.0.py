# coding=UTF-8
PogoUIGUIVer = '2017/1/18 v1.0'

'''
PogoUIGUI 輔助工具

2017/1/18 v1.0 first release

'''

from Tkinter import *
from datetime import datetime

from PogoModules.PogoUI import *
from PogoModules.PogoPeplink import *



class PogoUIGUI(Frame):

    def __init__(self, master=None):        
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # import 模組的版本訊息        

        self.master.title ('PogoUIGUI ' + PogoUIGUIVer)
        self.dispPogoPeplinkVer0 = Label(self)
        self.dispPogoPeplinkVer0 ['text'] = 'PogoPeplink: '
        self.dispPogoPeplinkVer0.grid(row=1, column=0, sticky = W)
        self.dispPogoPeplinkVer1 = Label(self)
        self.dispPogoPeplinkVer1 ['text'] = PogoPeplinkVer
        self.dispPogoPeplinkVer1.grid(row=1, column=1, columnspan=2, sticky = W)
        self.dispPogoUIVer0 = Label(self)
        self.dispPogoUIVer0 ['text'] = 'PogoUI: '
        self.dispPogoUIVer0.grid(row=2, column=0, sticky = W)
        self.dispPogoUIVer1 = Label(self)
        self.dispPogoUIVer1 ['text'] = PogoUIVer
        self.dispPogoUIVer1.grid(row=2, column=1,columnspan=2, sticky = W)
        


        #顯示與記錄操作
        self.Command0 = Label(self)
        self.Command0 ['text'] = 'Command: '
        self.Command0.grid(row=4, column=0)
        self.Command1 = Entry(self)
        self.Command1 ['width'] = 120
        self.Command1.grid(row=4, column=1,columnspan=14, sticky = W)

        self.Command2 = Button(self)
        self.Command2 ['text'] = 'Run'
        self.Command2.grid(row=4, column=15)
        self.Command2 ['command'] = self.UIRun

        self.sendlog = Button(self)
        self.sendlog ['text'] = 'Save to File'
        self.sendlog.grid(row=4, column=16)
        self.sendlog ['command'] = self.UISave

        #顯示訊息
        self.dispEvent0 = Label(self)
        self.dispEvent0  ['text'] = 'Show Event: '
        self.dispEvent0 .grid(row=5, column=0)
        self.dispEvent1 = Label(self)
        self.dispEvent1 ['text'] = 'info will update here'
        self.dispEvent1.grid(row=5, column=1,columnspan=8)

        

        #開關 Browser
        self.Browser = Label(self)
        self.Browser ['text'] = 'Browser Action: '
        self.Browser.grid(row=6, column=0)
        
        self.Bopen =  Button(self)
        self.Bopen ['text'] = 'Bopen'
        self.Bopen.grid(row=6, column=1)
        self.Bopen ['command'] = self.UIBopen

        self.Bquit =  Button(self)
        self.Bquit ['text'] = 'Boquit'
        self.Bquit.grid(row=6, column=2)
        self.Bquit ['command'] = self.UIBquit

        #指定網址
        self.Bvisit0 = Label(self)
        self.Bvisit0 ['text'] = 'URL: '
        self.Bvisit0.grid(row=7, column=0)
        
        self.Bvisit1 = Entry(self)
        self.Bvisit1 ['width'] = 40
        self.Bvisit1.grid(row=7, column=1,columnspan=5, sticky = W)
        self.Bvisit1.insert(0,'http://')
        
        self.Bvisit2 = Button(self)
        self.Bvisit2 ['text'] = 'Bvisit'
        self.Bvisit2.grid(row=7, column=6)
        self.Bvisit2 ['command'] = self.UIBvisit

        #說明

        self.Bxxx0 = Label(self)
        self.Bxxx0 ['text'] = '選取與操作: 以下為基本用法 element可用 css / xpath / name / link_text'
        self.Bxxx0.grid(row=8, column=0,columnspan=5, sticky = W)

        #Bxxx 功能 第一行
        self.Bxxx1 = Label(self)
        self.Bxxx1 ['text'] = 'element: '
        self.Bxxx1.grid(row=9, column=0)
        
        self.Bxxx2 = Entry(self)
        self.Bxxx2 ['width'] = 40
        self.Bxxx2.grid(row=9, column=1,columnspan=5, sticky = W)

        self.Bxxx3 = Button(self)
        self.Bxxx3 ['text'] = 'Bclick'
        self.Bxxx3.grid(row=9, column=6)
        self.Bxxx3 ['command'] = self.UIBclick
        

        self.Bxxx4 = Button(self)
        self.Bxxx4 ['text'] = 'Bcheck'
        self.Bxxx4.grid(row=9, column=7)
        self.Bxxx4 ['command'] = self.UIBcheck
        

        self.Bxxx5 = Button(self)
        self.Bxxx5 ['text'] = 'Bncheck'
        self.Bxxx5.grid(row=9, column=8)
        self.Bxxx5 ['command'] = self.UIBncheck

        self.Bxxx6 = Label(self)
        self.Bxxx6 ['text'] = 'Fill/element2/x軸: '
        self.Bxxx6.grid(row=9, column=9,columnspan=2)

        self.Bxxx7 = Entry(self)
        self.Bxxx7 ['width'] = 40
        self.Bxxx7.grid(row=9, column=11,columnspan=5, sticky = W)

        self.Bxxx8 = Button(self)
        self.Bxxx8 ['text'] = 'Bfill'
        self.Bxxx8.grid(row=9, column=16)
        self.Bxxx8 ['command'] = self.UIBfill

        self.Bxxx9 = Button(self)
        self.Bxxx9 ['text'] = 'Bdrop'
        self.Bxxx9.grid(row=9, column=17)
        self.Bxxx9 ['command'] = self.UIBdrop

        self.Bxxx10 = Label(self)
        self.Bxxx10 ['text'] = 'y軸: '
        self.Bxxx10.grid(row=9, column=18)

        self.Bxxx11 = Entry(self)
        self.Bxxx11 ['width'] = 5
        self.Bxxx11.grid(row=9, column=19)
        
        self.Bxxx12 = Button(self)
        self.Bxxx12 ['text'] = 'Bdrop_offset'
        self.Bxxx12.grid(row=9, column=20)
        self.Bxxx12 ['command'] = self.UIBdrop_offset
        
        #說明
        self.BxxxT0 = Label(self)
        self.BxxxT0 ['text'] = '選取與操作: 以下為進階用法 抓特定文字的相對位置, UI版本相容性高'
        self.BxxxT0.grid(row=10, column=0,columnspan=5, sticky = W)
        
        #BxxxT 功能 第一行
        self.BxxxT1 = Label(self)
        self.BxxxT1 ['text'] = '點選Text: '
        self.BxxxT1.grid(row=11, column=0)
        
        self.BxxxT2 = Entry(self)
        self.BxxxT2 ['width'] = 40
        self.BxxxT2.grid(row=11, column=1,columnspan=5, sticky = W)

        self.BxxxT3 = Label(self)
        self.BxxxT3 ['text'] = '第幾個(adj) '
        self.BxxxT3.grid(row=11, column=6)

        self.BxxxT4 = Entry(self)
        self.BxxxT4 ['width'] = 5
        self.BxxxT4.grid(row=11, column=7)
        self.BxxxT4.insert (0, '0')

        self.BxxxT5 = Button(self)
        self.BxxxT5 ['text'] = 'BclickT'
        self.BxxxT5.grid(row=11, column=8)
        self.BxxxT5 ['command'] = self.UIBclickT
        
         #BxxxT 功能 第二行
        self.BxxxTA1 = Label(self)
        self.BxxxTA1 ['text'] = '搜尋Text: '
        self.BxxxTA1.grid(row=12, column=0)
        
        self.BxxxTA2 = Entry(self)
        self.BxxxTA2 ['width'] = 40
        self.BxxxTA2.grid(row=12, column=1,columnspan=5, sticky = W)

        self.BxxxTA3 = Label(self)
        self.BxxxTA3 ['text'] = '目標序(num): '
        self.BxxxTA3.grid(row=12, column=6)

        self.BxxxTA4 = Entry(self)
        self.BxxxTA4 ['width'] = 5
        self.BxxxTA4.grid(row=12, column=7)
        self.BxxxTA4.insert (0, '1')

        self.BxxxTA5 = Label(self)
        self.BxxxTA5 ['text'] = '第幾個(adj): '
        self.BxxxTA5.grid(row=12, column=8)

        self.BxxxTA6 = Entry(self)
        self.BxxxTA6 ['width'] = 5
        self.BxxxTA6.grid(row=12, column=9)
        self.BxxxTA6.insert (0, '0')

        self.BxxxTA7 = Label(self)
        self.BxxxTA7 ['text'] = '層(adj2): '
        self.BxxxTA7.grid(row=12, column=10)

        self.BxxxTA8 = Entry(self)
        self.BxxxTA8 ['width'] = 5
        self.BxxxTA8.grid(row=12, column=11)
        self.BxxxTA8.insert (0, 'A')

        self.BxxxTA9 = Button(self)
        self.BxxxTA9 ['text'] = 'BclickTI/Input'
        self.BxxxTA9.grid(row=12, column=12,columnspan=2)
        self.BxxxTA9 ['command'] = self.UIBclickTI

        self.BxxxTA10 = Button(self)
        self.BxxxTA10 ['text'] = 'BclickTB/Button'
        self.BxxxTA10.grid(row=12, column=14,columnspan=2)
        self.BxxxTA10 ['command'] = self.UIBclickTB

        self.BxxxTA11 = Button(self)
        self.BxxxTA11 ['text'] = 'BclickTO/Option'
        self.BxxxTA11.grid(row=12, column=16,columnspan=2)
        self.BxxxTA11 ['command'] = self.UIBclickTO

        self.BxxxTA12 = Button(self)
        self.BxxxTA12 ['text'] = 'BcheckT'
        self.BxxxTA12.grid(row=12, column=18)
        self.BxxxTA12 ['command'] = self.UIBcheckT

        self.BxxxTA13 = Button(self)
        self.BxxxTA13 ['text'] = 'BncheckT'
        self.BxxxTA13.grid(row=12, column=19)
        self.BxxxTA13 ['command'] = self.UIBncheckT

         #BxxxT 功能 第三行
        self.BxxxTB1 = Label(self)
        self.BxxxTB1 ['text'] = '搜尋Text: '
        self.BxxxTB1.grid(row=13, column=0)
        
        self.BxxxTB2 = Entry(self)
        self.BxxxTB2 ['width'] = 40
        self.BxxxTB2.grid(row=13, column=1,columnspan=5, sticky = W)

        self.BxxxTB3 = Label(self)
        self.BxxxTB3 ['text'] = '目標序(num): '
        self.BxxxTB3.grid(row=13, column=6)

        self.BxxxTB4 = Entry(self)
        self.BxxxTB4 ['width'] = 5
        self.BxxxTB4.grid(row=13, column=7)
        self.BxxxTB4.insert (0, '1')

        self.BxxxTB5 = Label(self)
        self.BxxxTB5 ['text'] = '第幾個(adj): '
        self.BxxxTB5.grid(row=13, column=8)

        self.BxxxTB6 = Entry(self)
        self.BxxxTB6 ['width'] = 5
        self.BxxxTB6.grid(row=13, column=9)
        self.BxxxTB6.insert (0, '0')

        self.BxxxTB7 = Label(self)
        self.BxxxTB7 ['text'] = '層(adj2): '
        self.BxxxTB7.grid(row=13, column=10)

        self.BxxxTB8 = Entry(self)
        self.BxxxTB8 ['width'] = 5
        self.BxxxTB8.grid(row=13, column=11)
        self.BxxxTB8.insert (0, 'A')

        self.BxxxTB9 = Label(self)
        self.BxxxTB9 ['text'] = 'Fill: '
        self.BxxxTB9.grid(row=13, column=12)

        self.BxxxTB10 = Entry(self)
        self.BxxxTB10 ['width'] = 40
        self.BxxxTB10.grid(row=13, column=13,columnspan=5, sticky = W)

        self.BxxxTB11 = Button(self)
        self.BxxxTB11 ['text'] = 'BfillT'
        self.BxxxTB11.grid(row=13, column=18)
        self.BxxxTB11 ['command'] = self.UIBfillT

        self.BxxxTB12 = Button(self)
        self.BxxxTB12 ['text'] = 'BfillTT/TextArea'
        self.BxxxTB12.grid(row=13, column=19, columnspan=2)
        self.BxxxTB12 ['command'] = self.UIBfillTT

         #BxxxT 功能 第四行
        self.BxxxTC1 = Label(self)
        self.BxxxTC1 ['text'] = '搜尋Text1: '
        self.BxxxTC1.grid(row=14, column=0)
        
        self.BxxxTC2 = Entry(self)
        self.BxxxTC2 ['width'] = 40
        self.BxxxTC2.grid(row=14, column=1,columnspan=5, sticky = W)

        self.BxxxTC3 = Label(self)
        self.BxxxTC3 ['text'] = '搜尋Text2: '
        self.BxxxTC3.grid(row=14, column=6)

        self.BxxxTC4 = Entry(self)
        self.BxxxTC4 ['width'] = 40
        self.BxxxTC4.grid(row=14, column=7,columnspan=5, sticky = W)

        self.BxxxTC5 = Button(self)
        self.BxxxTC5 ['text'] = 'BselectTO/Option'
        self.BxxxTC5.grid(row=14, column=12,columnspan=2)      

        #說明
        self.Baddon0 = Label(self)
        self.Baddon0 ['text'] = '附加操作: 以下為輔助功能'
        self.Baddon0.grid(row=15, column=0,columnspan=5, sticky = W)

        #輔助功能項

        self.Baddon1 = Label(self)
        self.Baddon1 ['text'] = '秒數: '
        self.Baddon1.grid(row=16, column=0)
        
        self.Baddon2 = Entry(self)
        self.Baddon2 ['width'] = 5
        self.Baddon2.grid(row=16, column=1)

        self.Baddon3 = Button(self)
        self.Baddon3 ['text'] = 'Bsleep'
        self.Baddon3.grid(row=16, column=2)
        self.Baddon3 ['command'] = self.UIBsleep
             
        self.BaddonA1 = Label(self)
        self.BaddonA1 ['text'] = 'element/Text: '
        self.BaddonA1.grid(row=17, column=0)
        
        self.BaddonA2 = Entry(self)
        self.BaddonA2 ['width'] = 40
        self.BaddonA2.grid(row=17, column=1,columnspan=5, sticky = W)

        self.BaddonA3 = Label(self)
        self.BaddonA3 ['text'] = '次數: '
        self.BaddonA3.grid(row=17, column=6)
        
        self.BaddonA4 = Entry(self)
        self.BaddonA4 ['width'] = 5
        self.BaddonA4.grid(row=17, column=7)
        self.BaddonA4.insert (0 , '3')

        self.BaddonA5 = Button(self)
        self.BaddonA5 ['text'] = 'Bwait'
        self.BaddonA5.grid(row=17, column=8)
        self.BaddonA5 ['command'] = self.UIBwait

        self.BaddonA6 = Button(self)
        self.BaddonA6 ['text'] = 'Bwait_text'
        self.BaddonA6.grid(row=17, column=9)
        self.BaddonA6 ['command'] = self.UIBwait_text
        
        #說明
        self.BPP0 = Label(self)
        self.BPP0 ['text'] = 'PogoPeplink 整合 Suit'
        self.BPP0.grid(row=18, column=0,columnspan=5, sticky = W)

        #PogoPeplink

        self.BPP1 = Label(self)
        self.BPP1 ['text'] = 'Url: '
        self.BPP1.grid(row=19, column=0)
        
        self.BPP2 = Entry(self)
        self.BPP2 ['width'] = 40
        self.BPP2.grid(row=19, column=1,columnspan=5, sticky = W)
        self.BPP2. insert (0, 'http://')

        self.BPP3 = Label(self)
        self.BPP3 ['text'] = 'Username: '
        self.BPP3.grid(row=19, column=6)
        
        self.BPP4 = Entry(self)
        self.BPP4 ['width'] = 5
        self.BPP4.grid(row=19, column=7)
        self.BPP4. insert (0, 'admin')

        self.BPP5 = Label(self)
        self.BPP5 ['text'] = 'Password: '
        self.BPP5.grid(row=19, column=8)
        
        self.BPP6 = Entry(self)
        self.BPP6 ['width'] = 5
        self.BPP6.grid(row=19, column=9)
        self.BPP6. insert (0, 'admin')
           
        self.BPP7 = Button(self)
        self.BPP7 ['text'] = 'UIsLogin'
        self.BPP7.grid(row=19, column=10)
        self.BPP7 ['command'] = self.UIUIsLogin

        self.BPP8 = Button(self)
        self.BPP8 ['text'] = 'UIStartUP'
        self.BPP8.grid(row=19, column=11)
        self.BPP8 ['command'] = self.UIUIStartUP
        
                   
        self.BPPA1 = Label(self)
        self.BPPA1 ['text'] = 'Url: '
        self.BPPA1.grid(row=20, column=0)
        
        self.BPPA2 = Entry(self)
        self.BPPA2 ['width'] = 40
        self.BPPA2.grid(row=20, column=1,columnspan=5, sticky = W)
        self.BPPA2. insert (0, 'http://')

        self.BPPA3 = Label(self)
        self.BPPA3 ['text'] = '嘗試次數: '
        self.BPPA3.grid(row=20, column=6)
        
        self.BPPA4 = Entry(self)
        self.BPPA4 ['width'] = 5
        self.BPPA4.grid(row=20, column=7)
        self.BPPA4. insert (0, '30')

        self.BPPA5 = Label(self)
        self.BPPA5 ['text'] = '等待(sec): '
        self.BPPA5.grid(row=20, column=8)
        
        self.BPPA6 = Entry(self)
        self.BPPA6 ['width'] = 5
        self.BPPA6.grid(row=20, column=9)
        self.BPPA6. insert (0, '10')
           
        self.BPPA7 = Button(self)
        self.BPPA7 ['text'] = 'UIsApply'
        self.BPPA7.grid(row=20, column=10)
        self.BPPA7 ['command'] = self.UIUIsApply
                   
        self.BPPB1 = Label(self)
        self.BPPB1 ['text'] = '手動取得設備變數前, 需先開到 stauts page, opt 1 多了 SN/UP, opt 2 多了 LANmac'
        self.BPPB1.grid(row=21, column=0,columnspan=8)

        self.BPPB2 = Label(self)
        self.BPPB2 ['text'] = '格式(opt): '
        self.BPPB2.grid(row=21, column=8)        

        self.BPPB3 = Entry(self)
        self.BPPB3 ['width'] = 5
        self.BPPB3.grid(row=21, column=9)
        self.BPPB3.insert (0,'0')

        self.BPPB4 = Button(self)
        self.BPPB4 ['text'] = 'HWCheck'
        self.BPPB4.grid(row=21, column=10)
        self.BPPB4 ['command'] = self.UIHWCheck
        


    
    def UIBopen(self):        
        self.Command1.delete(0,200)
        command = 'driver = Bopen()'
        self.Command1.insert(0, command)

    def UIBquit(self):
        self.Command1.delete(0,200)
        command = 'Bquit()'
        self.Command1.insert(0, command)

    def UIRun(self):        
        cmd = self.Command1.get()
        if 'driver' in cmd: # drive 這變數在函式內需轉換
            cmd2 = cmd.replace ('driver' , 'self.driver')
        else
            cmd2 = cmd
        exec (cmd2)
        

    def UISave(self):
        cmd = self.Command1.get()

        runTime = datetime.now()
        logTime = datetime.strftime(runTime, '%Y-%m-%d-%H%M')
        
        log.write(cmd)
        log.write('\n')
        self.dispEvent1 ['text'] = '[' + logTime + '] | log write | ' + cmd

    def UIBvisit(self):
        self.Command1.delete(0,200)
        url = self.Bvisit1.get()
        command = 'Bvisit("' + url + '")'
        self.Command1.insert(0, command)

    def UIBclick(self):
        self.Command1.delete(0,200)
        e1 = self.Bxxx2.get()
        command = 'Bclick("'+ e1 +'")'
        self.Command1.insert(0, command)

    def UIBcheck(self):
        self.Command1.delete(0,200)
        e1 = self.Bxxx2.get()
        command = 'Bcheck("'+ e1 +'")'
        self.Command1.insert(0, command)      

    def UIBncheck(self):
        self.Command1.delete(0,200)
        e1 = self.Bxxx2.get()
        command = 'Bncheck("'+ e1 +'")'
        self.Command1.insert(0, command)

    def UIBfill(self):
        self.Command1.delete(0,200)
        e1 = self.Bxxx2.get()
        e2 = self.Bxxx7.get()
        command = 'Bfill("' + e1 + '","' + e2 + '")'
        self.Command1.insert(0, command)

    def UIBdrop(self):
        self.Command1.delete(0,200)
        e1 = self.Bxxx2.get()
        e2 = self.Bxxx7.get()
        command = 'Bdrop("' + e1 + '","' + e2 + '")'
        self.Command1.insert(0, command)

    def UIBdrop_offset(self):
        self.Command1.delete(0,200)
        e1 = self.Bxxx2.get()
        e2 = self.Bxxx7.get()
        e3 = self.Bxxx11.get()
        command = 'Bdrop_offset("' + e1 + '","' + e2 + "," + e3 + '")'
        self.Command1.insert(0, command)

    def UIBclickT(self):
        self.Command1.delete(0,200)
        e1 = self.BxxxT2.get()
        e2 = self.BxxxT4.get()
        command = 'BclickT("' + e1 + '","' + e2 + '")'
        self.Command1.insert(0, command)        

    def UIBclickTI(self):
        self.Command1.delete(0,200)
        e1 = self.BxxxTA2.get()
        e2 = self.BxxxTA4.get()
        e3 = self.BxxxTA6.get()
        e4 = self.BxxxTA8.get()
        command = 'BclickTI("' + e1 + '","' + e2 +  '","' + e3  +'","' + e4 + '")'
        self.Command1.insert(0, command)

    def UIBclickTB(self):
        self.Command1.delete(0,200)
        e1 = self.BxxxTA2.get()
        e2 = self.BxxxTA4.get()
        e3 = self.BxxxTA6.get()
        e4 = self.BxxxTA8.get()
        command = 'BclickTB("' + e1 + '","' + e2 +  '","' + e3  +'","' + e4 + '")'
        self.Command1.insert(0, command)

    def UIBclickTO(self):
        self.Command1.delete(0,200)
        e1 = self.BxxxTA2.get()
        e2 = self.BxxxTA4.get()
        e3 = self.BxxxTA6.get()
        e4 = self.BxxxTA8.get()
        command = 'BclickTO("' + e1 + '","' + e2 +  '","' + e3  +'","' + e4 + '")'
        self.Command1.insert(0, command)

    def UIBcheckT(self):
        self.Command1.delete(0,200)
        e1 = self.BxxxTA2.get()
        e2 = self.BxxxTA4.get()
        e3 = self.BxxxTA6.get()
        e4 = self.BxxxTA8.get()
        command = 'BcheckT("' + e1 + '","' + e2 +  '","' + e3  +'","' + e4 + '")'
        self.Command1.insert(0, command)

    def UIBncheckT(self):
        self.Command1.delete(0,200)
        e1 = self.BxxxTA2.get()
        e2 = self.BxxxTA4.get()
        e3 = self.BxxxTA6.get()
        e4 = self.BxxxTA8.get()
        command = 'BncheckT("' + e1 + '","' + e2 +  '","' + e3  +'","' + e4 + '")'
        self.Command1.insert(0, command)

    def UIBfillT(self):
        self.Command1.delete(0,200)
        e1 = self.BxxxTB2.get()
        e2 = self.BxxxTB4.get()
        e3 = self.BxxxTB6.get()
        e4 = self.BxxxTB8.get()
        e5 = self.BxxxTB10.get()
        command = 'BfillT("' + e1 + '","' + e5 +  '","' + e2  +'","' + e3 + '","' + e4 + '")'
        self.Command1.insert(0, command)

    def UIBfillTT(self):
        self.Command1.delete(0,200)
        e1 = self.BxxxTB2.get()
        e2 = self.BxxxTB4.get()
        e3 = self.BxxxTB6.get()
        e4 = self.BxxxTB8.get()
        e5 = self.BxxxTB10.get()
        command = 'BfillTT("' + e1 + '","' + e5 +  '","' + e2  +'","' + e3 + '","' + e4 + '")'
        self.Command1.insert(0, command)

    def UIBselectTO(self):
        self.Command1.delete(0,200)
        e1 = self.BxxxTC2.get()
        e2 = self.BxxxTC4.get()
        command = 'BselectTO("' + e1 + '","' + e2 + '")'
        self.Command1.insert(0, command)

    def UIBsleep(self):
        self.Command1.delete(0,200)
        e1 = self.Baddon2.get()        
        command = 'Bsleep("' + e1 + '")'
        self.Command1.insert(0, command)

    def UIBwait(self):
        self.Command1.delete(0,200)
        e1 = self.BxxxA2.get()
        e2 = self.BxxxA4.get()
        command = 'Bwait("' + e1 + '","' + e2 + '")'
        self.Command1.insert(0, command)

    def UIBwait_text(self):
        self.Command1.delete(0,200)
        e1 = self.BxxxA2.get()
        e2 = self.BxxxA4.get()
        command = 'Bwait_text("' + e1 + '","' + e2 + '")'
        self.Command1.insert(0, command)

    def UIUIsLogin(self):
        self.Command1.delete(0,200)
        e1 = self.BPP2.get()
        e2 = self.BPP4.get()
        e3 = self.BPP6.get()
        command = 'UIsLogin("' + e1 + '","' + e2 + '","' + e3 + '")'
        self.Command1.insert(0, command)
        
    def UIUIsApply(self):
        self.Command1.delete(0,200)
        e1 = self.BPPA2.get()
        e2 = self.BPPA4.get()
        e3 = self.BPPA6.get()
        command = 'UIsApply("' + e1 + '","' + e2 + '","' + e3 + '")'
        self.Command1.insert(0, command)

    def UIHWCheck(self):
        self.Command1.delete(0,200)
        e1 = self.BPPB3.get()
        if e1 == '0':
            command = 'HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver = HWCheck(driver,0)'
        if e1 == '1':
            command = 'HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,SN,UP = HWCheck(driver,1)'
        if e1 == '2':
            command = 'HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,SWver,LANmac = HWCheck(driver,2)'
        self.Command1.insert(0, command)

    def UIUIStartUP(self):
        self.Command1.delete(0,200)
        e1 = self.BPP2.get()
        e2 = self.BPP4.get()
        e3 = self.BPP6.get()
        command = 'SWver, HWmode, Mtype, HWmodel, HWver, FWver, HWmodels,LANmac = UIStartUP("' + e1 + '",driver,"' + e2 + '","' + e3 + '")'
        self.Command1.insert(0, command)
        
if __name__ == '__main__':

        
    runTime = datetime.now()
    logTime = datetime.strftime(runTime, '%Y-%m-%d-%H%M') # 給Log檔名用的時間格式
    logTime2 = datetime.strftime(runTime, '%Y/%m/%d') # Log 轉入 Google & Excel 用的時間格式
    logname = 'PogoUIGUI-' + logTime
    logfile = logname + ".log"    
    log = file('log/'+logfile, 'w')
    
    root = Tk()
    app = PogoUIGUI(master=root)
    app.mainloop()
    log.close()
