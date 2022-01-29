# coding=UTF-8
#需安裝 python3 & iperf3 
from Smoke_Module import * 

IpAdd = '10.92.112.47' #設備IP #2938-619E-C1C0
pepurl = 'http://'+IpAdd #http:// + 設備IP
AppWait = 120 #小型設備要加 dealy 建議 120 sec, RC18 後自動修改

server = '10.88.80.120'
client = '192.168.50.10'
IPFS = 'nohup iperf -s &> iperfs.txt&' # Iperf 當Server 的 Command
IPFC = 'iperf -c ' #Iperf 當Client 的 Command 要留空格後面加 IP
RunTime =  1 # 測試次數
RunTimeC = 0 # 測試次數計數器(啟始數)



if __name__ == "__main__":




    width = ['24w20','24w2040','24w40','5w20','5w40','5w80']

    for i in width:
        #Config_File_Upload2('Config/'+ i +'.txt')
        print('Config/'+ i +'.txt')
        Bsleep(120)
        #print('download' + str(i))
        #print('upload' + str(i))