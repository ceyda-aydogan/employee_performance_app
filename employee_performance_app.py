from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
import mysql.connector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import bs4 as bs
import urllib.request

class calisanPerformansi(QWidget):
    def __init__(self,parent=None):
        super(calisanPerformansi,self).__init__(parent)
        grid=QGridLayout()
        
##Satış kaydı labelı
        grid.addWidget(QLabel("SATIŞ KAYDI"),0,0,1,2)
        grid.addWidget(QLabel("Çalışan:"),1,0)
        grid.addWidget(QLabel("Tarih:"),2,0)
        grid.addWidget(QLabel("Günlük Satış Miktarı:"),3,0)

##Satış kaydı inputu
        self.calisan=QLineEdit()
        grid.addWidget(self.calisan,1,1)
        self.tarih=QDateEdit(calendarPopup=True)
        grid.addWidget(self.tarih,2,1)
        self.gunlukSatisMiktari=QLineEdit()
        grid.addWidget(self.gunlukSatisMiktari,3,1)
          
##Kaydet butonu 
        kaydet=QPushButton("Kaydet")
        grid.addWidget(kaydet,5,0,1,2)
        kaydet.clicked.connect(self.satisKaydi)
        kaydet.clicked.connect(self.verileriListele)

##Çalışanların ortalama satışı labelı
        grid.addWidget(QLabel("ÇALIŞANLARIN ORTALAMA SATIŞ BİLGİSİ"),0,3,1,2)
        grid.addWidget(QLabel("Net Satış Tutarı:"),1,3)
        grid.addWidget(QLabel("Çalışan Sayısı:"),2,3)
        grid.addWidget(QLabel("Ortalama Satış:"),3,3)
        
##Çalışanların ortalama satışı inputu
        self.bosluk=QLabel("      ")
        grid.addWidget(self.bosluk,0,2)
        self.netSatis=QLineEdit()
        grid.addWidget(self.netSatis,1,4)
        self.calisanSayi=QLineEdit()
        grid.addWidget(self.calisanSayi,2,4)
        self.ortSatis=QLabel("")
        grid.addWidget(self.ortSatis,3,4)
        self.note=QLabel("")
        grid.addWidget(self.note,4,3,1,2)
        
##Hesapla Butonu
        hesapla=QPushButton("Hesapla")
        grid.addWidget(hesapla,5,3,1,2)
        hesapla.clicked.connect(self.ortSatisHesapla)
  
##Grafik labelı
        grid.addWidget(QLabel("GRAFİK"),7,0,1,2)
        
#Grafik 
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas,8,0,4,2)
        self.toolbar = NavigationToolbar(self.canvas, self)
        grid.addWidget(self.toolbar,12,0,1,2)
        
##Grafik butonu
        grafigiGoster=QPushButton("Grafiği Göster")
        grid.addWidget(grafigiGoster,13,0,1,2)
        grafigiGoster.clicked.connect(self.veriGrafigi)
        grafigiGoster.clicked.connect(self.makineOgr)
        
##Doğrusal Regresyon labelı
        grid.addWidget(QLabel("DOĞRUSAL REGRESYON SONUCU"),8,3)
        grid.addWidget(QLabel("Sonraki Çalışanın\nTahmini Satış Miktarı:"),9,3)
        
##Doğrusal Regresyon çıktısı
        self.linearSonucu=QLabel("")
        grid.addWidget(self.linearSonucu,9,4)
      
##Verilen iş ilanları labelı
        grid.addWidget(QLabel("VERİLEN İŞ İLANLARI"),10,3,1,2)
        grid.addWidget(QLabel("Kariyer.net:"),11,3)
        grid.addWidget(QLabel("LinkedIn:"),12,3)
        
##Verilen iş ilanları inputu
        self.kariyerNet=QLabel("")
        grid.addWidget(self.kariyerNet,11,4)
        self.linkedIn=QLabel("")
        grid.addWidget(self.linkedIn,12,4)
        
##İlanları getir butonu
        ilanlariGetir=QPushButton("İlanları Getir")
        grid.addWidget(ilanlariGetir,13,3,1,2)
        ilanlariGetir.clicked.connect(self.kariyerNetIlan)
        ilanlariGetir.clicked.connect(self.linkedInIlan)
        
        self.setLayout(grid)
        self.setWindowTitle("ÇALIŞAN PERFORMANSI UYGULAMASI")
        self.resize(800,500)

    def satisKaydi(self):
        calisan=self.calisan.text()
        tarih=self.tarih.date()
        trh=tarih.toPyDate()
        gunlukSatisMiktari=self.gunlukSatisMiktari.text()
        gunlukSatisMiktari=int(gunlukSatisMiktari)
        baglanti=mysql.connector.connect(user="root",password="",host="127.0.0.1",database="programlama")
        isaretci=baglanti.cursor()
        isaretci.execute('''INSERT INTO satis(calisan,tarih,gunlukSatisMiktari) VALUES ("%s","%s","%d")'''%(calisan,trh,gunlukSatisMiktari))
        baglanti.commit()
        baglanti.close()
        
    def verileriListele(self):
        baglanti=mysql.connector.connect(user="root",password="",host="127.0.0.1",database="programlama")
        isaretci=baglanti.cursor()
        isaretci.execute('''SELECT * FROM satis''')
        sonuc=isaretci.fetchall()
        
        calisanListe=[]
        tarihListe=[]
        gunlukSatisListe=[]

        for i in sonuc:
            calisanListe.append(i[1])
        for j in sonuc:
            tarihListe.append(j[2])        
        for k in sonuc:
            gunlukSatisListe.append(k[3])
            
        gunlukSatisArr=np.array(gunlukSatisListe)
        netSatisHesabi=gunlukSatisArr.sum()
        netSatisHesabi=str(netSatisHesabi)
        self.netSatis.setText(netSatisHesabi)
        
        baglanti.commit()
        baglanti.close()
        
    def ortSatisHesapla(self):
        netSH=0
        try: netSH=int(self.netSatis.text())
        except: pass
        calisanSayisi=0
        try: calisanSayisi=int(self.calisanSayi.text())
        except: pass
    
        if not calisanSayisi:
            self.calisanSayi.setText('<font color="red">Lütfen çalışan sayısını giriniz</font>')
            self.calisanSayi.setFocus()
        else:
            ortSatis=netSH/calisanSayisi
            self.ortSatis.setText('<font>%s</font>'%ortSatis)
            if ortSatis<=50:
                self.note.setText('<font color="red">Satış Miktarı Düşük</font>')
            else:
                self.note.setText('<font color="green">Satış Miktarı Yeterli</font>')
                
    def veriGrafigi(self):
        data = pd.read_csv(r"C:\Users\ASUS\programlama.csv")
        x=list(data['calisan'])
        y=list(data['gunlukSatisMiktari'])
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x,y,'o-')
        ax.set_title("Çalışanlara Göre Satış Miktarları",fontweight='bold')
        ax.set_xlabel("Çalışanlar")
        ax.set_ylabel("Satış Miktarları")
        self.canvas.draw()
        
    def kariyerNetIlan(self):
        kaynak=urllib.request.urlopen('https://www.kariyer.net/is-ilani/epengle-tekstil-endustri-ve-ticaret-anonim-sirke-urun-gelistirme-uzmani-2671826').read()
        sayfa=bs.BeautifulSoup(kaynak,'lxml')
        for baglanti in sayfa.find_all("a",class_="link position"):
            baglanti=baglanti.string
            self.kariyerNet.setText('<font color="blue">%s</font>'%baglanti)
        
    def linkedInIlan(self):
        kaynak=urllib.request.urlopen('https://www.linkedin.com/jobs/view/2425881263/?alternateChannel=search&refId=XdnIv7MUTxHJ3pL8YTlUiQ%3D%3D&trackingId=KS9Tg6XycjrMnofinLFVOQ%3D%3D').read()
        sayfa=bs.BeautifulSoup(kaynak,'lxml')
        for baglanti in sayfa.find_all("h1"):
            baglanti=baglanti.string
            self.linkedIn.setText('<font color="blue">%s</font>'%baglanti)
            
    def makineOgr(self):
        data = pd.read_csv(r"C:\Users\ASUS\programlama.csv")
        calisanID=data[['calisanID']]
        gunlukSatisMiktari=data[['gunlukSatisMiktari']]
        x_train,x_test,y_train,y_test=train_test_split(calisanID,gunlukSatisMiktari,test_size=0.33,random_state=0)
        lr=LinearRegression()
        lr.fit(x_train,y_train)
        tahmin=lr.predict([[17]])
        self.linearSonucu.setText('<font>%d</font>'%tahmin)
  

uyg=QApplication([])
pencere=calisanPerformansi()
pencere.show()
uyg.exec_()