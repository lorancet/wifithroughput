# coding=UTF-8
#需安裝 python3 & iperf3 

server = '10.88.80.120'
client = '192.168.50.10'


if __name__ == "__main__":

    width = ['24w20','24w2040','24w40','5w20','5w40','5w80']


    for i in width:
        print('download' + str(i))
        print('upload' + str(i))