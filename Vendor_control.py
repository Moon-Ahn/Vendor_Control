#!/usr/bin/env python3
#coding: UTF-8
import sys
import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
from requests.auth import HTTPDigestAuth
from multiprocessing import Process, Queue
import datetime
import csv
import threading,time

global table_Count
table_Count = 0

protocols = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 윈도우 설정
        self.setGeometry(700, 200, 320, 510)  # x, y, w, h
        self.setWindowTitle('Alarm status')

        VDN = ['Color', 'Tamper', 'Chroma', 'Brightness', 'Density (L)', 'Density (H)', 'Feature 1',
               'Feature 2', 'Feature 3', 'Feature 4', 'Sensitivity 1', 'Sensitivity 2', 'Sensitivity 3', 'Sensitivity 4',
               'Alarm Period','Alarm Output','Test Mode']
        VDL = ['VDL0', 'VDL1', 'VDL2', 'VDL3', 'VDL4', 'VDL5', 'VDL6', 'VDL7', 'VDL8', 'VDL9', 'VDL10', 'VDL11', 'VDL12', 'VDL13',
              'VDL14','VDL15','VDL16']
        VD = ['VD0', 'VD1', 'VD2', 'VD3', 'VD4', 'VD5', 'VD6', 'VD7', 'VD8', 'VD9', 'VD10', 'VD11', 'VD12', 'VD13',
              'VD14']

        myFont = QtGui.QFont("Arial", 11)

        for i in range(0, 17):
            VDL[i] = QLabel(VDN[i], self)
            VDL[i].resize(130, 25)
            VDL[i].move(20, 60 + 25 * i)
            VDL[i].setFont(myFont)

        for i in range(0, 15):
            VD[i] = QLineEdit('', self)
            VD[i].resize(130, 25)
            VD[i].move(180, 60 + 25 * i)
            VD[i].setAlignment(Qt.AlignCenter)

        self.Alarm_Output = QComboBox(self)
        self.Alarm_Output.resize(130, 25)
        self.Alarm_Output.move(180, 60 + 25 * (i+1))
        self.Alarm_Output.setEditable(True)
        self.Alarm_Output.lineEdit().setReadOnly(True)
        self.Alarm_Output.lineEdit().setAlignment(Qt.AlignCenter)
        self.Alarm_Output.addItem("Enable")
        self.Alarm_Output.addItem("Disable")

        self.Test_mode = QComboBox(self)
        self.Test_mode.resize(130, 25)
        self.Test_mode.move(180, 60 + 25 * (i + 2))
        self.Test_mode.setEditable(True)
        self.Test_mode.lineEdit().setReadOnly(True)
        self.Test_mode.lineEdit().setAlignment(Qt.AlignCenter)
        self.Test_mode.addItem("Off")
        self.Test_mode.addItem("On")

        # QButton 위젯 생성
        self.button0 = QPushButton('Seyeon IP', self)
        self.button0.clicked.connect(self.Seyeon_IP_open)
        self.button0.setGeometry(10, 10, 100, 30)

        # QButton 위젯 생성
        self.button0 = QPushButton('Vendor Change', self)
        self.button0.clicked.connect(lambda : self.Vendor_Change(VD,self.Alarm_Output,self.Test_mode))
        self.button0.setGeometry(180, 10, 130, 30)

        # QDialog 설정

        self.dialog = QDialog()

    # 버튼 이벤트 함수
    def Seyeon_IP_open(self):
        # 버튼 추가
        ############## LINE ###############

        IP = ['IP0', 'IP1', 'IP2', 'IP3', 'IP4', 'IP5', 'IP6', 'IP7', 'IP8', 'IP9', 'IP10', 'IP11', 'IP12', 'IP13',
              'IP14', 'IP15']
        ID = ['ID0', 'ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'ID6', 'ID7', 'ID8', 'ID9', 'ID10', 'ID11', 'ID12', 'ID13',
              'ID14', 'ID15']
        PS = ['PS0', 'PS1', 'PS2', 'PS3', 'PS4', 'PS5', 'PS6', 'PS7', 'PS8', 'PS9', 'PS10', 'PS11', 'PS12', 'PS13',
              'PS14', 'PS15']

        ##############NAME 텍스트 값 불러오기###############
        NAME_Read = []
        try:
            self.Seyeon_Read_file(NAME_Read, 'NAME')

            # print(NAME_Read)
        except:
            pass
        ###############################################
        ##############IP 텍스트 값 불러오기###############
        IP_Read = []
        try:
            self.Seyeon_Read_file(IP_Read, 'IP')
        except:
            pass
        ###############################################

        myFont = QtGui.QFont("Arial", 11)
        myFont.setBold(True)
        Explain1 = QLabel('IP                             ID                        '
                          'PASS', self.dialog)
        Explain1.setFont(myFont)
        Explain1.move(22, 64)

        Button_Font = QtGui.QFont("Arial", 10)
        Button_Font.setBold(True)

        try:
            Name = QLineEdit(NAME_Read[0], self.dialog)
        except:
            Name = QLineEdit('', self.dialog)
        Name.resize(130, 25)
        Name.move(20, 20)

        k = 0
        for i in range(0, 16):

            try:
                IP[i] = QLineEdit(IP_Read[k], self.dialog)
            except:
                IP[i] = QLineEdit('', self.dialog)
            IP[i].resize(130, 25)
            IP[i].move(20, 85 + 25 * i)
            try:
                ID[i] = QLineEdit(IP_Read[k+1], self.dialog)
            except:
                ID[i] = QLineEdit('', self.dialog)
            ID[i].resize(110, 25)
            ID[i].move(150, 85 + 25 * i)
            try:
                PS[i] = QLineEdit(IP_Read[k + 2], self.dialog)
            except:
                PS[i] = QLineEdit('', self.dialog)
            PS[i].setEchoMode(QLineEdit.Password)
            PS[i].resize(110, 25)
            PS[i].move(260, 85 + 25 * i)
            k += 3

        SaveB = QPushButton('SAVE', self.dialog)
        SaveB.resize(100, 26)
        SaveB.move(170, 20)
        SaveB.setFont(myFont)
        SaveB.clicked.connect(lambda: self.Seyeon_Save_and_dialog_close(Name, IP, ID, PS))

        # QDialog 세팅
        self.dialog.setWindowTitle('Seyeon')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(400, 510)
        self.dialog.show()

    def Seyeon_Read_file(self,FILE,Case):
        if Case == 'NAME':
            f = open("Seyeon_NAME_Save.txt", 'r', encoding='UTF8')
            t = f.read()
            FILE.append(t)
            f.close()
        elif Case == 'IP':
            f = open("Seyeon_IP_Save.txt", 'r', encoding='UTF8')
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                FILE.append(line)
            # print(FILE)
            f.close()

    ########################################################
    def Seyeon_Save_and_dialog_close(self,NAME, IP, ID, PAS):

        f = open("Seyeon_NAME_Save.txt", 'w', encoding='UTF8')
        f.write(NAME.text())
        f.close()

        f = open("Seyeon_IP_Save.txt", 'w', encoding='UTF8')
        for i in range(0, 16):
            f.write(IP[i].text() + '\n')
            f.write(ID[i].text() + '\n')
            f.write(PAS[i].text() + '\n')
        f.close()
        #f = open("IP.txt",'w',encoding='UTF8')
        # for i in range(0,16):
        #     f.write(IP[i].text() + '\n')
        self.dialog.close()

    def Vendor_Change(self,Ven_Status,Alarm,Testmode):

        Cam_Status=[]
        f = open("Seyeon_IP_Save.txt", 'r', encoding='UTF8')
        lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '')
            Cam_Status.append(line)
        # print(FILE)
        # f.close()
        # print(Cam_Status[0])
        # print(Ven_Status[0].text())
        # print('change')
        k = 0
        IP=[]
        ID=[]
        PAS=[]
        for i in range(0, 16):
            try:
                IP.append(Cam_Status[k])
                ID.append(Cam_Status[k+1])
                PAS.append(Cam_Status[k+2])
            except:
                pass
            k += 3

        for t in range(0, 16):
            try:
                if IP[t]=='':
                    pass

                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?ColorLow='+Ven_Status[0].text()+'&FwCgiVer=0x0001',
                    auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?ColorHigh=' + Ven_Status[1].text() +
                    '&FwCgiVer=0x0001',auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?Chroma=' + Ven_Status[2].text() +
                    '&FwCgiVer=0x0001',auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?Brightness=' + Ven_Status[3].text() +
                    '&FwCgiVer=0x0001', auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?IntensityLow=' + Ven_Status[4].text() +
                    '&FwCgiVer=0x0001', auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?IntensityHigh=' + Ven_Status[5].text() +
                    '&FwCgiVer=0x0001', auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?BackgroundTh1=' + Ven_Status[6].text() +
                    '&FwCgiVer=0x0001', auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?BackgroundTh2=' + Ven_Status[7].text() +
                    '&FwCgiVer=0x0001', auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?BackgroundTh3=' + Ven_Status[8].text() +
                    '&FwCgiVer=0x0001', auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?BackgroundTh4=' + Ven_Status[9].text() +
                    '&FwCgiVer=0x0001', auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?Sensitivity1=' + Ven_Status[10].text() +
                    '&FwCgiVer=0x0001', auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?Sensitivity2=' + Ven_Status[11].text() +
                    '&FwCgiVer=0x0001', auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?Sensitivity3=' + Ven_Status[12].text() +
                    '&FwCgiVer=0x0001', auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?Sensitivity4=' + Ven_Status[13].text() +
                    '&FwCgiVer=0x0001', auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?AlarmPeriod=' + Ven_Status[14].text() +
                    '&FwCgiVer=0x0001', auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?AlarmDisable=' + str(Alarm.currentIndex()) +
                    '&FwCgiVer=0x0001', auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
                requests.get(
                    'http://' + IP[t] + '/cgi-bin/admin/fwvamispecific.cgi?TestMode=' + str(Testmode.currentIndex()) +
                    '&FwCgiVer=0x0001', auth=HTTPDigestAuth(ID[t], PAS[t]), timeout=1)
            except:
                pass
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())