# coding=UTF-8
LoSmokeTestModulesUIVer = '2016/3/01 v1.0.0'

from splinter import Browser 
import time
import Queue
import sys
import paramiko
import socket
from datetime import datetime
from threading import Thread
from subprocess import Popen, PIPE #PingCheck & PingWait 會用到
import re
import os
from PogoModules.PogoUI import *
from PogoModules.PogoPeplink import *

IpAdd = '192.168.50.1'
pepurl = 'http://'+IpAdd #http:// + 設備IP


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())



def HD4_Wan_set(wan):


        link = 0
        for i in range(wan):

                link += 1
                e = i + 2
                Bclick("li.pt__item:nth-child("+str(e)+") > div:nth-child(1) > span:nth-child(3) > span:nth-child(2) > button:nth-child(2)")
                Bsleep(5)
                SBclickT('Static IP')
                SBfillT('IP Address', '10.88.81'+str(link)+'.1','1','9','1')
                SBfillT('Default Gateway', '10.88.81'+str(link)+'.254','1','6','1')
                SBfillT('DNS Server 1', '10.88.3.1')
                SBfillT('DNS Server 2', '168.95.1.1')
                SBfillT('Additional Public IP Address', '10.88.81'+str(link)+'.51','2')
                SBclickT('255.255.255.255','9')
                SBclickTB('Additional Public IP Address')        
                Bsleep(5)
                SBclickT('Save')

                if wan == 1 :
                        try:
                                Bsleep(5)
                                Bdrop_offset('li.pt__item:nth-child(3) > div:nth-child(1) > div:nth-child(4)',0,250)

                        except:
                                print e

def HD2_Wan_set(wan):


        link = 0
        for i in range(wan):

                link += 1
                e = i + 2
                Bclick("li.pt__item:nth-child("+str(e)+") > div:nth-child(1) > span:nth-child(3) > span:nth-child(2) > button:nth-child(2)")
                Bsleep(5)
                SBclickT('Static IP')
                SBfillT('IP Address', '10.88.8'+str(link)+'.1','1','9','1')
                SBfillT('Default Gateway', '10.88.8'+str(link)+'.254','1','6','1')
                SBfillT('DNS Server 1', '10.88.3.1')
                SBfillT('DNS Server 2', '168.95.1.1')
                SBfillT('Additional Public IP Address', '10.88.8'+str(link)+'.51','2')
                SBclickT('255.255.255.255','9')
                SBclickTB('Additional Public IP Address')        
                Bsleep(5)
                SBclickT('Save')
                Bsleep(10)

                if wan == 1 :
                        try:
                                Bsleep(5)
                                Bdrop_offset('li.pt__item:nth-child(3) > div:nth-child(1) > div:nth-child(4)',0,170)

                        except:
                                print e

def Pepwave_WAN_Set_Static_Tag(VID):

        Bclick('button.ni_btn_details:nth-child(1)')
        Bsleep(5)
        SBclickT('Static IP')
        SBfillT('IP Address', '10.88.81.1','1','9','1')
        SBfillT('Default Gateway', '10.88.81.254','1','6','1')
        SBfillT('DNS Server 1', '10.88.3.1')
        SBfillT('DNS Server 2', '168.95.1.1')
        SBfillT('Additional Public IP Address', '10.88.81.51','2')
        SBclickT('255.255.255.255','9')
        SBclickTB('Additional Public IP Address')        
        Bsleep(2)
        Bcheck('#vlan_setting_display > td:nth-child(2) > input:nth-child(1)')
        Bsleep(2)
        Bfill('#vlan_setting_display > td:nth-child(2) > input:nth-child(1)', VID)
        Bsleep(5)        
        SBclickT('Save')


def Wan_set(wan):
          
    link = 0

    for i in range(wan):
            link += 1
                       
            Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink='+str(link)) 
            #Bcheck('Enable')
            #Bcheck ('#enable_display > td:nth-child(2) > input:nth-child(1)')
            SBclickT('Static IP') #選 static 
            SBfillT('IP Address', '10.88.8'+str(link)+'.1','1','0','1')
            BfillT('Default Gateway', '10.88.8'+str(link)+'.254')
            SBfillT('DNS Server 1', '10.88.3.1')
            SBfillT('DNS Server 2', '168.95.1.1')
            SBfillT('Additional IP Address', '10.88.8'+str(link)+'.51')
            BclickT('255.255.255.255','6') 
            SBclickTB('Additional IP Address')
            time.sleep(5)
            SBclickT('Save')
    

        
def NAT_Mapping(): #632
    
        # Set NAT Mapping
        time.sleep(2)
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=natmap')
        time.sleep(2)
        Bclick('.add_action')
        time.sleep(2)
        Bfill('#host', '192.168.50.9')
        time.sleep(2)
        Bclick('#NATIn_conn_1_hasSelect')
        time.sleep(2)
        Bclick('#inbound_table > tbody:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#inbound_table > tbody:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bclick('button.ui-button:nth-child(1)')
        time.sleep(2)


        
def Inboun_access_310_632(DL1):
        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=inboundservers')
        time.sleep(2)
        Bclick('.add_action')
        time.sleep(2)
        Bfill('name', 'Server_01')
        time.sleep(2)
        Bfill('ip', DL1)
        time.sleep(2)
        BclickT ('Save')
        time.sleep(2)
        
        #Service setting HTTP
        time.sleep(2)
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=inbounddistribution')
        time.sleep(2)
        Bclick('.add_action')
        time.sleep(2)
        Bfill('name','HTTP')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.tablecontent2.protocol_tr > td:nth-child(2) > select.protocol_selector_action > optgroup:nth-child(2) > option:nth-child(1)')
        #Bclick('select.TEXTAREA:nth-child(5) > optgroup:nth-child(2) > option:nth-child(1)')
        time.sleep(2)
        Bcheck('#inbound_conn_1_hasSelect')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.multiple_server_panel > td.tablecontent2 > table > tbody > tr > td > label > input')
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
        #Bclick('select.TEXTAREA:nth-child(5) > optgroup:nth-child(2) > option:nth-child(7)')
        time.sleep(2)
        Bcheck('#inbound_conn_1_hasSelect')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.multiple_server_panel > td.tablecontent2 > table > tbody > tr > td > label > input')
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
        #Bclick('select.TEXTAREA:nth-child(5) > optgroup:nth-child(4) > option:nth-child(5)')
        time.sleep(2)
        Bcheck('#inbound_conn_1_hasSelect')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.multiple_server_panel > td.tablecontent2 > table > tbody > tr > td > label > input')
        time.sleep(2)
        BclickT ('Save')
        time.sleep(2)
        
        #Service setting POP3
        time.sleep(2)
        Bclick('.add_action')
        time.sleep(2)
        Bfill('name','POP3')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.tablecontent2.protocol_tr > td:nth-child(2) > select.protocol_selector_action > optgroup:nth-child(2) > option:nth-child(4)')
        #Bclick('select.TEXTAREA:nth-child(5) > optgroup:nth-child(2) > option:nth-child(4)')
        time.sleep(2)
        Bcheck('#inbound_conn_1_hasSelect')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.multiple_server_panel > td.tablecontent2 > table > tbody > tr > td > label > input')
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
        #Bclick('select.TEXTAREA:nth-child(5) > optgroup:nth-child(2) > option:nth-child(6)')
        time.sleep(2)
        Bcheck('#inbound_conn_1_hasSelect')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.multiple_server_panel > td.tablecontent2 > table > tbody > tr > td > label > input')
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
        #Bclick('select.TEXTAREA:nth-child(5) > optgroup:nth-child(3) > option:nth-child(3)')
        time.sleep(2)
        Bcheck('#inbound_conn_1_hasSelect')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.multiple_server_panel > td.tablecontent2 > table > tbody > tr > td > label > input')
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
        #Bclick('#Protocol > option:nth-child(2)')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr:nth-child(5) > td:nth-child(2) > div > select > option:nth-child(1)')
        #Bclick('#destporttype > option:nth-child(1)')
        time.sleep(2)
        Bcheck('#inbound_conn_1_hasSelect')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.multiple_server_panel > td.tablecontent2 > table > tbody > tr > td > label > input')
        time.sleep(2)
        BclickT ('Save')
        time.sleep(2)


def Inboun_access_20(DL1):
        
        #Service setting HTTP
        time.sleep(2)
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=inbounddistribution')
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


def InboundAccessLoadWeight():
        
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=inboundservers')
        time.sleep(2)
        BclickT ('Add Server')
        time.sleep(2)
        Bfill('table.form_table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)', 'Server_01')
        time.sleep(2)
        Bfill('tr.tablecontent2:nth-child(2) > td:nth-child(2) > input:nth-child(1)', '192.168.1.8')
        time.sleep(2)
        BclickT ('Save')
        time.sleep(2)
        BclickT ('Add Server')
        time.sleep(2)
        Bfill('table.form_table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)', 'Server_02')
        time.sleep(2)
        Bfill('tr.tablecontent2:nth-child(2) > td:nth-child(2) > input:nth-child(1)', '192.168.1.9')
        time.sleep(2)
        BclickT ('Save')
        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=inbounddistribution')
        time.sleep(2)
        Bclick('.add_action')
        time.sleep(2)
        Bfill('name','TCP666')
        time.sleep(2)
        #Bclick('#Protocol > option:nth-child(2)') #UDP
        #time.sleep(2)
        Bclick('#destporttype > option:nth-child(2)')
        time.sleep(2)
        Bfill('#Port','666')
        time.sleep(2)
        Bclick('#inbound_conn_1_hasSelect')
        
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(1) > td:nth-child(2) > div:nth-child(1) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.multiple_server_panel > td.tablecontent2 > table > tbody > tr.tablecontent2.server_1 > td > label')
        time.sleep(2)
        Bclick('#ui-id-1 > table > tr.multiple_server_panel > td.tablecontent2 > table > tbody > tr.tablecontent2.server_2 > td > label')
        BclickT ('Save')
        time.sleep(2)

        

def Enable_CLI():
        
        time.sleep(2)        
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utadmin')
        time.sleep(2)
        BcheckT('CLI SSH & Console')
        time.sleep(2)    
        BclickT('LAN / WAN','1')
        time.sleep(2)
        BclickT ('Save')
        time.sleep(2)
        print 'Success - Enable SSH Setting'


def LanSet_20(MAC_ADD): #DHCP Server Test

        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan')
        time.sleep(2)
        BfillT('IP Range', '192.168.50.10','1','1','1')
        time.sleep(2)
        BfillT('IP Range', '192.168.50.100','2','1','1')
        time.sleep(2)
        BfillT('Lease Time', '6','2','1','1')
        time.sleep(2)
        BclickT('Assign DNS server automatically')
        time.sleep(2)
        BfillT('DNS Server 1:','1.1.1.1')
        time.sleep(2)
        BfillT('DNS Server 2:','2.2.2.2')
        time.sleep(2)
        BclickT('Add')
        time.sleep(2)
        BclickT('15. DNS Domain Name')
        time.sleep(2)
        BfillT('Add Extended DHCP Option','PEPLINK_TTC')
        time.sleep(2)
        BclickT('OK')
        time.sleep(2)
        BfillT('DHCP Reservation', 'Lo-XP1','1','0','1')
        time.sleep(2)
        BfillT('DHCP Reservation', MAC_ADD,'2','0','1')        
        time.sleep(2)
        BfillT('DHCP Reservation', '192.168.1.200','3','0','1')
        time.sleep(2)
        BclickT('Save')
        time.sleep(2)




def LanSet_310(MAC_ADD): #DHCP Server Test

        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan')
        time.sleep(2)
        BfillT('IP Range', '192.168.50.10','1','1','1')
        time.sleep(2)
        BfillT('IP Range', '192.168.50.100','2','1','1')
        time.sleep(2)
        BfillT('Lease Time', '6','2','1','1')
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
        BclickT('Add')
        time.sleep(2)
        BclickT('15. DNS Domain Name')
        time.sleep(2)
        BfillT('Add Extended DHCP Option','PEPLINK_TTC')
        time.sleep(2)
        Bclick('button.ui-button:nth-child(1)')
        time.sleep(2)
        BfillT('DHCP Reservation', 'Lo-XP1','1','0','1')
        time.sleep(2)
        BfillT('DHCP Reservation', MAC_ADD,'2','0','1')        
        time.sleep(2)
        BfillT('DHCP Reservation', '192.168.1.200','3','0','1')
        time.sleep(2)
        BclickT('Save')
        time.sleep(2)

def DNS_Server():
    
        # Set DNS Server
        time.sleep(2)
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=edns')
        time.sleep(2)
        Bclick('#edns_server_panel > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > button:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_server_edit_dialog > form:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_server_edit_dialog > form:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')    
        time.sleep(2)
        Bclick('#edns_server_edit_dialog > form:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_server_edit_dialog > form:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_server_edit_dialog > form:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_server_edit_dialog > form:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')    
        time.sleep(2)
        BclickT('Save')
        time.sleep(2)
        Bclick('#edns_default_panel > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > button:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_default_soa_panel > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(1) > td:nth-child(1) > a:nth-child(1)')
        time.sleep(2)
        Bfill('nameserver_addr','10.88.81.1')
        time.sleep(2)
        BclickT('Save')
        time.sleep(3)
        Bwait('#edns_default_ns_panel > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_default_ns_panel > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        Bfill('_value','ns2')
        time.sleep(2)
        Bfill('_a_value','10.88.82.1')
        time.sleep(2)
        BclickT('Save')
        time.sleep(2)


        # add domain peptest.com.tw
        time.sleep(2)
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=edns')
        time.sleep(2)
        Bclick('#edns_domain_panel > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        Bfill('name','peptest.com.tw')
        time.sleep(2)
        BclickT('Save')
        time.sleep(2)

        # add domain peptest1.com.tw
        time.sleep(2)
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=edns')
        time.sleep(2)
        Bclick('#edns_domain_panel > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        Bfill('name','peptest1.com.tw')
        time.sleep(2)
        BclickT('Save')
        time.sleep(2)

        #add a Records  www
        time.sleep(2)
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=edns')
        time.sleep(2)
        Bclick('#edns_domain_panel > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(1) > td:nth-child(1) > a:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_a_panel > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(3) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        Bfill('#edns_domain_a_edit_dialog > form:nth-child(1) > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)','www')
        time.sleep(2)
        Bclick('#edns_domain_a_value > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_domain_a_value > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > div:nth-child(1) > div:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_domain_a_value > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_domain_a_value > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > div:nth-child(1) > div:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        BclickT('Save')
        time.sleep(2)
        #add a Records  www.tw
        time.sleep(2)
        Bwait('tr.tablecontent3:nth-child(4) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent3:nth-child(4) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        Bfill('#edns_domain_a_edit_dialog > form:nth-child(1) > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)','www.tw')
        time.sleep(2)
        Bclick('#edns_domain_a_value > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bfill('#edns_domain_a_value > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > div:nth-child(1) > div:nth-child(3) > input:nth-child(2)','10.88.81.52')
        time.sleep(2)
        Bclick('#edns_domain_a_value > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > div:nth-child(1) > div:nth-child(3) > input:nth-child(1)')    
        time.sleep(2)
        Bclick('#edns_domain_a_value > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bfill('#edns_domain_a_value > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > div:nth-child(1) > div:nth-child(3) > input:nth-child(2)','10.88.82.52')
        time.sleep(2)
        Bclick('#edns_domain_a_value > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > div:nth-child(1) > div:nth-child(3) > input:nth-child(1)')
        time.sleep(3)
        BclickT('Save')
        time.sleep(2)

        #add a Records  www1 測試 Priority
        time.sleep(3)
        Bwait('tr.tablecontent3:nth-child(5) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent3:nth-child(5) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        Bfill('#edns_domain_a_edit_dialog > form:nth-child(1) > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)','www1')
        time.sleep(2)
        Bclick('#priority_custom_yes')
        time.sleep(2)
        Bclick('#edns_domain_a_value > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_domain_a_value > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > div:nth-child(1) > div:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_domain_a_value > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_domain_a_value > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > div:nth-child(1) > div:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_domain_a_priority > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > select:nth-child(1) > option:nth-child(2)')
        time.sleep(3)
        BclickT('Save')
        time.sleep(2)

        #add MX Records
        time.sleep(3)
        Bwait('#edns_mx_panel > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_mx_panel > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        Bfill('#edns_domain_mx_edit_dialog > form:nth-child(1) > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)','mail')
        time.sleep(2)
        Bfill('#edns_domain_mx_edit_dialog > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(1) > input:nth-child(1)','1')
        time.sleep(2)
        Bfill('#edns_domain_mx_edit_dialog > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)','mail')
        time.sleep(2)
        BclickT('Save')
        time.sleep(2)

        #add TXT Records
        time.sleep(3)
        Bwait('#edns_txt_panel > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        Bclick('#edns_txt_panel > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        Bfill('#edns_domain_txt_edit_dialog > form:nth-child(1) > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > textarea:nth-child(1)','v=spf1 include:10.88.81.1')
        time.sleep(2)
        BclickT('Save')
        time.sleep(2)
        BclickT('Close')

def FireWallRlue1397():
        
        #Firewall inbound allow / default deny
        print 'Test case 1397\n'
        time.sleep(2)
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=firewall')
        time.sleep(2)
        Bclick('#firewall_settings > table:nth-child(3) > tfoot > tr:nth-child(2) > td > button')
        time.sleep(2)
        Bfill('rulename', 'test 1281')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(9) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)        
        Bcheck('tr.tablecontent2:nth-child(10) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
        BclickT('Save')
        time.sleep(2)
        Bclick('#inbound_0 > td:nth-child(1) > div:nth-child(1) > a:nth-child(1)')
        time.sleep(2)
        Bclick('#ui-id-5 > form:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        BclickT('Save')
        time.sleep(2)


def FireWallRlue1398():
                
        #Firewall inbound deny / default allow
        time.sleep(2)
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=firewall')
        time.sleep(2)
        Bclick('#firewall_settings > table:nth-child(3) > tfoot > tr:nth-child(2) > td > button')
        time.sleep(2)
        Bfill('rulename', 'test 1281')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(9) > td:nth-child(2) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bcheck('tr.tablecontent2:nth-child(10) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
        BclickT('Save')
        time.sleep(2)
        
def FireWallRlue1399():
    
        time.sleep(2)
        #Firewall Outbound deny / default allow
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=firewall')
        time.sleep(2)
        Bclick('#firewall_settings > table:nth-child(2) > tfoot > tr:nth-child(2) > td > button')
        time.sleep(2)
        Bfill('rulename', 'test 1281')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(9) > td:nth-child(2) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(10) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        BclickT('Save')
        time.sleep(2)

def FireWallRlue1400():

        time.sleep(2)    
        #Firewall Outbound allow / default deny
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=firewall')
        time.sleep(2)
        Bclick('#firewall_settings > table:nth-child(2) > tfoot > tr:nth-child(2) > td > button')
        time.sleep(2)
        Bfill('rulename', 'test 1281')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(9) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(10) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        SBclickT('Save')
        time.sleep(2)
         #修改Default Rules
        time.sleep(2)
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=firewall')
        time.sleep(2)
        Bclick('#outbound_0 > td:nth-child(1) > div:nth-child(1) > a:nth-child(1)')
        time.sleep(2)
        Bclick('#ui-id-5 > form:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        BclickT('Save')
        time.sleep(2)


#Test Case 1222 Outbound Policy Custom Rules Priority Any proto
def SetOutboundPolicy1222():
    
        po1 = 'tbody.algo_panel:nth-child(7) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)'
        po2 = 'tbody.algo_panel:nth-child(7) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)'
        time.sleep(2)
        Bvisit ('192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
        time.sleep(2)
        Bclick('.add_action')
        time.sleep(2)
        Bfill('rulename', 'Test Case 1222')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(4) > td:nth-child(2) > div:nth-child(1) > select:nth-child(1) > option:nth-child(1)')
        time.sleep(2)
        Bclick('.algo_action > option:nth-child(4)')
        time.sleep(2)
        Bdrop(po1,po2)
        time.sleep(2)
        BclickT('Save')
        time.sleep(5)
        print 'SetOutboundPolicy1222'

#Test Case 1232 Outbound Policy Custom Rules Weighed by MAC address
def SetOutboundPolicy1232(MAC_add):

        time.sleep(2)       
        Bvisit('192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
        time.sleep(2)
        Bclick('tr.sort_item:nth-child(1) > td:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)')
        time.sleep(2)
        Bfill('rulename', 'Test Case 1232')

        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(3) > td:nth-child(2) > div:nth-child(1) > select:nth-child(1) > option:nth-child(5)')
        time.sleep(2)
        Bfill('tr.tablecontent2:nth-child(3) > td:nth-child(2) > div:nth-child(1) > input:nth-child(4)', MAC_add )
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
        print 'SetOutboundPolicy1232'

#Test Case 1233 Outbound Policy Custom Rules Least Used by Source IP Network
def SetOutboundPolicy1233():

        time.sleep(2)
        Bvisit('192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
        time.sleep(2)
        Bclick('tr.sort_item:nth-child(1) > td:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)')
        time.sleep(2)
        Bfill('rulename', 'Test Case 1233')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(3) > td:nth-child(2) > div:nth-child(1) > select:nth-child(1) > option:nth-child(4)')
        time.sleep(2)
        Bfill('tr.tablecontent2:nth-child(3) > td:nth-child(2) > div:nth-child(1) > input:nth-child(2)','192.168.1.0')
        time.sleep(2)
        Bclick('.algo_action > option:nth-child(6)')
        time.sleep(2)
        Bclick('.chkbox_panel > div:nth-child(1) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        BclickT('Save')
        time.sleep(2)
        print 'SetOutboundPolicy1233 Least Used WAN1'


def OutboundByDomain():

        time.sleep(2)       
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
        time.sleep(2)
        Bclick('.add_action')
        time.sleep(2)
        Bfill('rulename', 'Outbound By Domain')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(4) > td:nth-child(2) > div:nth-child(1) > select:nth-child(1) > option:nth-child(6)')
        time.sleep(2)
        Bfill('tr.tablecontent2:nth-child(4) > td:nth-child(2) > div:nth-child(1) > input:nth-child(5)','lo.pepttc.com')
        time.sleep(2)
        Bclick('tr.tablecontent2:nth-child(4) > td:nth-child(2) > div:nth-child(1) > select:nth-child(1) > option:nth-child(1)')
        time.sleep(2)        
        Bclick('.algo_action > option:nth-child(3)')
        time.sleep(2)
        Bcheck('option.conn:nth-child(2)')
        time.sleep(2)
        SBclickT('Save')

def FirewallByDomain():

            time.sleep(2)
            Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=firewall')
            time.sleep(2)
            Bclick('table.form_table:nth-child(1) > tfoot:nth-child(3) > tr:nth-child(2) > td:nth-child(1) > button:nth-child(1)')
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

        #開啟Expert Mode
def Enable_ExperMode():

        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
        time.sleep(2)
        Bclick('#mainContent > div.smart_content.outbound_policy > table.form_table.sep.outbound_summary > thead > tr.tabletitle > td > div.helpIcon')
        time.sleep(2)
        Bclick('#_tips_box_ > a')
        time.sleep(2)


        #新增Outbound Policy
        
def Outbound_ExpertMode():

        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
        time.sleep(2)
        Bclick('.addAction')
        time.sleep(2)
        Bfill('rulename', 'Expert Mode Test')
        time.sleep(2)
        Bfill('dstip', '192.168.2.0')
        time.sleep(2)
        Bclick('.algorithm > tr:nth-child(1) > td:nth-child(2) > select:nth-child(1) > option:nth-child(4)')
        time.sleep(2)
        SBclickT('Save')
        time.sleep(2)
        Bdrop_offset('#custom_2',0,-50)
        time.sleep(2)
        Bclick('div.menu_item:nth-child(8)')
     #新增Outbound Policy
        



        #新增Outbound Policy
def Outbound_Policy():

        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
        time.sleep(2)
        Bclick('.addAction')
        time.sleep(2)
        Bfill('rulename', 'Expert Mode Test')
        time.sleep(2)
        Bfill('dstip', '192.168.2.0')
        time.sleep(2)
        Bclick('.algorithm > tr:nth-child(1) > td:nth-child(2) > select:nth-child(1) > option:nth-child(4)')
        time.sleep(2)
        SBclickT('Save')
        time.sleep(2)
        Bdrop_offset('#custom_2',0,-50)
        time.sleep(2)
        Bclick('div.menu_item:nth-child(8)')
     #新增Outbound Policy
        

def Outbound_Policy7():

        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=outboundpolicy')
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
        time.sleep(2)


def DNS_Proxy_Enable():
 
        #WAN1 設定
        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan')
        time.sleep(2)
        BfillT('Local DNS Records', 'pepttc.test.com','1','0','1')
        time.sleep(2)
        BfillT('Local DNS Records', '210.1.1.10','2','0','1')
        time.sleep(2)
        BclickT('Save')
        time.sleep(2)
        
def DNS_Proxy_Disable():
 
        #WAN1 設定
        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=advlan')
        time.sleep(2)
        Bncheck('.ldns_enable_action')
        time.sleep(2)
        Bclick('.save_action')
        time.sleep(2)

def QosSet():
        
        print 'QosSet'
        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=eqosgroup')
        time.sleep(2)
        SBclickT('Add')
        time.sleep(2)
        Bfill('#user_group_panel > form > table > tbody > tr.tablecontent2.ip_row > td:nth-child(2) > input','192.168.50.9')
        time.sleep(2)
        Bclick('#user_group_panel > form > table > tbody > tr:nth-child(3) > td:nth-child(2) > select > option:nth-child(2)')
        time.sleep(2)
        SBclickT('Save')
        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=eqosbandwidth')
        time.sleep(2)
        Bclick('#is_enable_yes')
        time.sleep(2)
        Bfill('eqos_bandwidth_max_cap_ui_in_1','20')
        time.sleep(2)
        Bfill('eqos_bandwidth_max_cap_ui_out_1','20')
        time.sleep(2)
        Bfill('eqos_bandwidth_max_cap_ui_in_2','10')
        time.sleep(2)
        Bfill('eqos_bandwidth_max_cap_ui_out_2','10')
        time.sleep(2)
        Bclick('#eqos_bandwidth_display > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)



def QosSet_BR(): #BR','MOTG','Surf

        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=eqosgroup')
        time.sleep(2)
        Bcheck('#add_group_button')
        time.sleep(2)
        Bfill('.ui-autocomplete-input','192.168.1.9')
        time.sleep(2)
        Bcheck('tr.tablecontent2:nth-child(3) > td:nth-child(2) > select:nth-child(1) > option:nth-child(2)')
        time.sleep(2)
        Bcheck('button.ui-button:nth-child(1)')
        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=eqosbandwidth')
        time.sleep(2)
        Bcheck('#is_enable_yes')
        time.sleep(2)
        Bfill('eqos_bandwidth_max_cap_ui_in_1','20')
        time.sleep(2)
        Bfill('eqos_bandwidth_max_cap_ui_out_1','20')
        time.sleep(2)
        Bcheck('#eqos_bandwidth_display > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)

def QosGroupChange():
    
        print 'QosGroupChange'
        #Login
        time.sleep(2)        
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=eqosgroup')
        time.sleep(2)
        Bclick('#custom_1 > td.tabletitle2 > a')
        time.sleep(2)
        Bclick('#user_group_panel > form > table > tbody > tr:nth-child(3) > td:nth-child(2) > select > option:nth-child(3)')
        time.sleep(2)
        SBclickT('Save')
        time.sleep(2)



def SMNP_Set():

        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utsnmp')
        time.sleep(2)
        BcheckT('SNMPv1')
        BcheckT('SNMPv2c')
        BcheckT('SNMPv3')
        BcheckT('SNMP Trap')
        time.sleep(2)
        BfillT('SNMP Trap Community','public')
        time.sleep(2)
        BfillT('SNMP Trap Server','192.168.50.9')
        time.sleep(3)
        Bclick('.submit_action')
        time.sleep(2)
        BclickT('Add SNMP Community')
        time.sleep(2)
        BfillT('Community Name','public')
        time.sleep(2)
        BfillT('Allowed Network','192.168.50.0')
        time.sleep(2)
        SBclickT ('Save')
        time.sleep(3)
        BclickT('Add SNMP User')
        time.sleep(2)
        BfillT('User Name','md5')
        time.sleep(2)
        Bclick('div.ui-dialog:nth-child(9) > form:nth-child(2) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > select:nth-child(1) > option:nth-child(2)')
        time.sleep(2)
        Bfill('input.auth_fields','peplink5978')
        time.sleep(2)
        SBclickT ('Save')
        time.sleep(3)
        BclickT('Add SNMP User')
        time.sleep(2)
        BfillT('User Name','sha')
        time.sleep(2)
        Bclick('div.ui-dialog:nth-child(9) > form:nth-child(2) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > select:nth-child(1) > option:nth-child(3)')
        time.sleep(2)
        Bfill('input.auth_fields','peplink5978')
        time.sleep(2)
        SBclickT ('Save')
        time.sleep(3)

def SF_toLoFH1():

        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=advmvpn')
        time.sleep(2)
        Bfill('.oneoff_mvpn_display > form:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > input:nth-child(1)','TEST1')
        time.sleep(2)
        Bclick('tr.tablecontent3:nth-child(3) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        Bclick('#vpn_summary_table > tr:nth-child(2) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        BfillT('Name','To_FH1_Test')
        time.sleep(2)
        BfillT('Remote ID','Lo-FH1')
        time.sleep(2)
        Bfill('vpn_server_list','10.88.80.2')
        time.sleep(2)
        SBclickT('Save')
        time.sleep(2)

def SF_toLoFH2():

        time.sleep(2)
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=advmvpn')
        time.sleep(2)
        Bclick('#vpn_summary_table > tr:nth-child(2) > td:nth-child(1) > button:nth-child(1)')
        time.sleep(2)
        BfillT('Name','To_FH2_Test')
        time.sleep(2)
        BfillT('Remote ID','Lo-FH2')
        time.sleep(2)
        Bfill('vpn_server_list','10.88.80.3')
        time.sleep(2)
        SBclickT('Save')
        time.sleep(2)

def WAN1_Disable():

        time.sleep(2)    
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
        time.sleep(2)
        Bncheck('#enable_display > td:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        SBclickT ('Save')
        time.sleep(2)

def WAN1_Enable():

        time.sleep(2)    
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
        time.sleep(2)
        Bcheck('#enable_display > td:nth-child(2) > input:nth-child(1)')
        time.sleep(2)
        SBclickT ('Save')
        time.sleep(2)
        
def PepAnalysis():

        time.sleep(2)    
        Bvisit('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=pepvpnstatus')
        time.sleep(2)
        Bclick('tr.peer_row:nth-child(1) > td:nth-child(6) > button:nth-child(1)')
        time.sleep(2)
        Bclick('.testIcon')
        time.sleep(2)
        Bclick('.start_action')
        time.sleep(60)
        Bcap('log/PepAnalysis-1048.png') 
        time.sleep(2)

def WAN1_Tag(VID):

        time.sleep(2)    
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
        time.sleep(2)
        Bcheck('#physical_panel > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(2) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bfill('#vlan_setting_display > td:nth-child(2) > input:nth-child(1)', VID )
        time.sleep(2)
        SBclickT ('Save')

def ICMP_Disable():

        time.sleep(2)               
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
        time.sleep(2)
        Bncheck('#reply_ping_enable')
        time.sleep(2)
        Bclick('.save_action')
        time.sleep(2)
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=2')
        time.sleep(2)
        Bncheck('#reply_ping_enable')
        time.sleep(2)
        #SBclickT ('Save')
        Bclick('.save_action')
        time.sleep(2)

def ICMP_Disable_BR(): # BR,MOTG,Surf

        time.sleep(2)    
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
        time.sleep(2)
        Bncheck('#reply_ping_enable')
        time.sleep(2)
        SBclickT ('Save')
        time.sleep(2)
        
def ICMP_Enable():

        time.sleep(2)
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
        time.sleep(2)
        Bcheck('#reply_ping_enable')
        time.sleep(2)
        SBclickT ('Save')
        time.sleep(2)

def ICMP_Enable_BR(): # BR,MOTG,Surf

        time.sleep(2)    
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
        time.sleep(2)
        Bcheck('#reply_ping_enable')
        time.sleep(2)
        SBclickT ('Save')
        time.sleep(2)

#WAN1 Static 設定
    
def WAN1_Static(VID):

        time.sleep(2)        
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
        time.sleep(2)
        Bcheck('Enable')
        time.sleep(2)
        SBclickT('Static IP') #選 static 
        SBfillT('IP Address', '10.88.81.1','1','0','1')
        BfillT('Default Gateway', '10.88.81.254')
        SBfillT('DNS Server 1', '10.88.3.1')
        SBfillT('DNS Server 2', '168.95.1.1')
        time.sleep(2)
        Bcheck('#physical_panel > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(2) > td:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
        time.sleep(2)
        Bfill('#vlan_setting_display > td:nth-child(2) > input:nth-child(1)',VID)
        time.sleep(2)
        SBclickT ('Save')
        time.sleep(2)
                
#WAN1 DHCP Client 設定
    
def WAN1_DHCP_Client():

        time.sleep(2)        
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')
        time.sleep(2)
        Bcheck('Enable')
        time.sleep(2)
        SBclickT('DHCP')
        time.sleep(2)
        SBclickT ('Save')
        time.sleep(2)
    
#WAN1 PPPoE Client 設定
    

def UIRestD():
        
        driver = Bopen()
        UIsLogin(pepurl)
        time.sleep(2)
        #UIsLogin(pepurl) #Login  
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=utconfig')
        time.sleep(2)
        Bwait('.restore_action')
        time.sleep(2)
        Bclick('.restore_action')
        time.sleep(2)
        Bwait('button.ui-button:nth-child(1)')
        time.sleep(2)
        Bclick('button.ui-button:nth-child(1)')
        time.sleep(60)
        Bquit()

def IPSec_7():

        time.sleep(2)
        # IPSec 設定    
        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=ipsec')
        #AES
        time.sleep(2)
        Bclick ('.ipsec_add_button')
        time.sleep(2)
        Bfill ('name','toFusionHubIPSec') #profile name
        time.sleep(2)
        Bcheck('ipsec_enable') # disable active
        time.sleep(2)
        Bclick('#ipsec_dialog > form > table:nth-child(6) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > label:nth-child(1) > input')
        time.sleep(2)
        Bfill ('ipsec_remote_gateway', '10.88.80.2') #remote GW
        time.sleep(2)
        Bfill ('_ip', '192.168.2.0')
        time.sleep(2)
        Bcheck('#ipsec_dialog > form > table:nth-child(6) > tbody:nth-child(1) > tr.tablecontent2.mode_select_panel > td:nth-child(2) > label:nth-child(4) > input[type="radio"]')
        time.sleep(2)
        Bfill ('ipsec_psk','peplink')
        time.sleep(2)
        Bfill ('#ipsec_dialog > form > table:nth-child(6) > tbody:nth-child(1) > tr:nth-child(13) > td:nth-child(2) > input','1.1.1.1')
        time.sleep(2)
        Bfill ('#ipsec_dialog > form > table:nth-child(6) > tbody:nth-child(1) > tr:nth-child(14) > td:nth-child(2) > input','2.2.2.2')
        time.sleep(2)
        Bclick('tr.multirow_select_row:nth-child(1) > td:nth-child(2) > select:nth-child(1) > option:nth-child(1)')
        time.sleep(2)
        Bclick("#ipsec_dialog_aggressive_mode_display > tr:nth-child(2) > td:nth-child(2) > select > option:nth-child(1)")
        time.sleep(2)
        SBclickT ('Save')
        time.sleep(2)

def EnableRA():

        Bvisit (pepurl + '/cgi-bin/MANGA/index.cgi?mode=config&option=utsysinfo')
        Bsleep(10)        
        BclickT("Turn On")
        Bsleep(2)        
        Bvisit (pepurl + '/cgi-bin/MANGA/support.cgi')
        Bsleep(2)
        BcheckT("Allow direct connection")
        Bsleep(60)
    


def BandwidthAllowance():

        Bvisit ('http://192.168.50.1/cgi-bin/MANGA/index.cgi?mode=config&option=wanlink&wanlink=1')     
        time.sleep(2)
        BcheckT('Bandwidth Allowance Monitor Settings')
        time.sleep(2)
        SBclickT('OK')
        time.sleep(2)
        Bclick('#mainContent > div.smart_content > form > table.form_table.sep.bam_display > tbody > tr:nth-child(4) > td:nth-child(2) > select > option:nth-child(3)')
        time.sleep(2)    
        Bfill('tr.bam_details_panel:nth-child(4) > td:nth-child(2) > input:nth-child(1)','100')
        time.sleep(2)
        SBclickT('Save')  




def U64Reboot():

    SSHD = ["10.88.80.11","192.168.1.8","192.168.1.9"]
    for iSSHD in SSHD:
        print iSSHD

        if  PingCheck(iSSHD) == 1:
            print 'Porcess reboot ' + iSSHD
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
                    print std,
                

            except Exception,e:
                print 'U64 Reboot failed:',e            
                print e
                ssh.close()
				

