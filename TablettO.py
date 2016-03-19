#! /usr/bin/python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, url_for
from threading import Thread
from datetime import date
import time
import os
import os.path
import re
import subprocess



app = Flask(__name__, static_url_path = "/static", static_folder = "/static")

menu='''
  <ul>
    <a href="/"><li> <i class="fa fa-home fa-2x"></i> </li></a>
    <a href="/Sauvegarde"<li><li> <i class="ico-menu fa fa-file-archive-o fa-2x"></i></li></a>
    <a href="/Restaure"<li><li> <i class="ico-menu fa fa-tablet fa-2x" style="margin-left:2px;"></i></li></a>
    <a href="/Deploie"<li><li> <i class="ico-menu fa fa-tablet fa-2x" style="margin-left:-3px;"></i><i class="ico-menu fa fa-tablet fa-2x" style="margin-left:-10px;" ></i></li></a>
    <a href="/Devices"<li><li> <i class="ico-menu fa fa-info-circle  fa-2x"></i> </li></a>
    <a href="/Applications"<li><li> <i class="fa fa-play-circle-o fa-2x"></i></li></a>
    <a href="/Systeme"<li><li> <i class="ico-menu fa fa-cogs fa-2x"></i></li></a>
  </ul>
'''

def ListDevices():
    devices = os.popen("adb devices -l").read()
    devices= re.split(' |:|\n',devices)
    devices=devices[4:]
    if len(devices)<4:
        dicDevices="pas de devices"
    else :
        item = devices.count('')
        for i in range (1,item):
            devices.remove('')
            dicDevices={}
        for i in range(0,len(devices)-7,10):
            j=i/10+1
            dicDevices["device"+str(int(j))]=(devices[i],devices[i+7],devices[i+3])
    return dicDevices



def listApps():
    dicSSDossiers={}
    dicApps={}

    for dossier, sous_dossiers, fichiers in os.walk('/media/Backups/Apps'):
        dossiers=re.split('/' , str(dossier))
        dossier=dossiers[-1]
        if len(fichiers)!=0:
            dicApps[dossier]=fichiers



    return dicApps

def install(id_devices,apks,dicApps):
    for apk in apks:
        path = [c for cle ,value in dicApps.items() if value==apk][0]
        os.system("cd "+ path +" && adb -s usb:"+ id_device +"  install -l " + apk )


def deploieBackups(id_device,nom_backup):
    os.system("cd /media/Backups/Backups && adb -s usb:"+ id_device +"  restore " + nom_backup )

def demarreVideo(nom_video):
    os.system("cd /media/Backups/Videos && adb screenrecord " + nom_backup )



app = Flask(__name__)

@app.route('/')
def accueil():
    try:
        os.makedirs("/media/Backups/Backups")
    except:
        rien="rien"
    try:
        os.makedirs("/media/Backups/Videos")
    except:
        print("probleme dans la creation de /media/Backups/Videos")
    menu_l={\
    "Accueil":"ico-menu fa fa-home fa-2x",\
    "Sauvegarde":"ico-menu fa fa-file-archive-o fa-2x",\
    "Restaure":"ico-menu fa fa-tablet fa-2x",\
    "Déploie":'ico-menu fa fa-tablet fa-2x" style="margin-left:-8px;"></i><i class="ico-menu fa fa-tablet fa-2x" style="margin-left:-10px;"',\
    "Systeme":"fa fa-cogs fa-2x",\
    "Applications":"ico-menu fa fa-play-circle-o fa-2x",\
    "Device":"ico-menu fa fa-info-circle fa-2x"}


    return render_template('accueil.html', titre="TablettO", menu_l=menu_l)

@app.route('/Accueil')
def accueil2():
    try:
        os.makedirs("/media/Backups/Backups")
    except:
        rien="rien"
    menu_l={\
    "Accueil":"ico-menu fa fa-home fa-2x",\
    "Sauvegarde":"ico-menu fa fa-file-archive-o fa-2x",\
    "Restaure":"ico-menu fa fa-tablet fa-2x",\
    "Déploie":'ico-menu fa fa-tablet fa-2x" style="margin-left:-8px;"></i><i class="ico-menu fa fa-tablet fa-2x" style="margin-left:-10px;"',\
    "Systeme":"fa fa-cogs fa-2x",\
    "Applications":"ico-menu fa fa-play-circle-o fa-2x",\
    "Device":"ico-menu fa fa-info-circle fa-2x"}


    return render_template('accueil.html', titre="TablettO", menu_l=menu_l)


@app.route('/Devices')
def devices():
    devices =  ListDevices()
    if devices =="pas de devices":
        return render_template('device.html', titre="Devices",devices=devices , lien="Devices", messagebox="Devices")
    else :
        return render_template('devices.html', titre="Devices" ,devices=devices ,lien="Devices", messagebox="")

@app.route('/Systeme')
def systeme():
    devices =  ListDevices()
    if devices =="pas de devices":

        return render_template('systeme.html', titre="Devices",devices=devices , lien="Devices", messagebox="Devices")
    else :
        return render_template('systeme.html', titre="Devices" ,devices=devices ,lien="Devices", messagebox="")



@app.route('/contact')
def contact():
    mail = "etienne.clave@ac-mayotte.fr"
    Dane = "Dane Mayotte"
    return "Mail: {} ---  {}".format(mail, Dane)


@app.route('/Sauvegarde', methods=['GET', 'POST'])
def Sauvegarde():
    devices = ListDevices()
    nbdevices = len(devices)
    if request.method == 'POST':
        if len(devices)==1:
            nom_device=devices["device1"][1]
            id_device=devices["device1"][0]
        else :
            key_device=request.form['key_device']
            nom_device=devices[key_device][1]
            id_device=devices[key_device][0]


        nom_backup=request.form['nom_backup']
        os.system("cd /media/Backups/Backups && adb -s "+ id_device +"  backup  -all -system -shared -apk -f "+nom_backup+".ab")
        taille=os.path.getsize("/media/Backups/Backups/"+nom_backup+".ab")
        if taille==0:
            return render_template('sauvegarde.html', titre="Oups !! ",devices=devices, nom_device=nom_device ,nom_backup=nom_backup , taille=taille , messagebox="sauvegarde")
        return render_template('sauvegarde.html', titre="Sauvegarde términé ",devices=devices, nom_device=nom_device ,nom_backup=nom_backup , taille=taille , messagebox="messagefin")
    if devices =="pas de devices":
        devices={}
        return  render_template('sauvegarde.html', titre="Sauvegarde", nbdevices=nbdevices ,devices=devices, messagebox="device")
    else :
        return render_template('sauvegarde.html', titre="Sauvegarde", nbdevices=nbdevices ,devices=devices, messagebox="")





@app.route('/Restaure', methods=['GET', 'POST'])
def Restaure():
    devices = ListDevices()
    nbdevices = len(devices)
    backups = os.listdir("/media/Backups/Backups")
    if len(backups)==0:
        return  render_template('restaure.html', titre="Oups !!", nbdevices=nbdevices ,devices=devices,backups=backups,messagebox="backup")
    if request.method == 'POST':

        nom_backup=request.form['nom_backup']
        if len(devices)==1:
            nom_device=devices["device1"][1]
            id_device=devices["device1"][0]
        else :
            key_device=request.form['key_device']
            nom_device=devices[key_device][1]
            id_device=devices[key_device][0]

        taille=os.path.getsize("/media/Backups/Backups/"+nom_backup)
        if taille==0:
            return render_template('restaure.html', titre="Oups !! ",devices=devices, nom_device=nom_device ,nom_backup=nom_backup , taille=taille , messagebox="sauvegarde")

        os.system("cd /media/Backups/Backups && adb -s "+ id_device +"  restore  "+  nom_backup)
        return render_template('restaure.html', titre="Restauration términée ",nbdevices=nbdevices, devices=devices, nom_device=nom_device ,nom_backup=nom_backup , messagebox="messagefin")
    if devices =="pas de devices":
        devices={}
        return  render_template('restaure.html', titre="Oups !!", nbdevices=nbdevices ,devices=devices,backups=backups, messagebox="device")
    else :
        return render_template('restaure.html', titre="Restaure", nbdevices=nbdevices ,devices=devices,backups=backups,messagebox="")

@app.route('/Deploie', methods=['GET', 'POST'])
def Deploie():
    devices = ListDevices()
    backups = os.listdir("/media/Backups/Backups")

    if len(backups)==0:
        return render_template('deploie.html', titre="Deploie",menu=menu,  backups=backups, messagebox="Backup")
    if devices =="pas de devices":
        devices={}
        return render_template('deploie.html', titre="Deploie",menu=menu,  backups=backups, messagebox="Device")

    if request.method == 'POST':
        nom_backup=request.form['nom_backup']

        for key,value in devices.items() :
            t = Thread(target=deploieBackups, args=(value[2],nom_backup,))
            t.start()

        return render_template('deploie.html', titre="Deploie",menu=menu, backups=backups, messagebox="messagefin")

    else :
        return render_template('deploie.html', titre="Deploie",menu=menu, backups=backups, messagebox="")




global value
value = "Demarrer"
@app.route('/Capture', methods=['GET', 'POST'])
def Capture():
    devices = ListDevices()
    global value
    global p
    global nom_capture

    if request.method == 'POST':
        nom_video=request.form['nom_video']

        if value=="Demarrer":
            value="Stopper"
            nom_capture=request.form['nom_video']
            global p
            p=subprocess.Popen(["/usr/bin/adb","shell","screenrecord /sdcard/capture.mp4"])
            #return  render_template('capture.html', titre="Capture d'ecran ", value=value, devices=devices, messagebox="encours")


        else:
            value="Demarrer"
            global p
            p.kill()
            time.sleep(3)
            os.system("cd /media/Backups/Videos && adb pull  /sdcard/capture.mp4 && mv capture.mp4  "+ nom_capture+".mp4")
            os.system("adb shell rm /sdcard/capture.mp4")
            #return  render_template('capture.html', titre="Capture d'ecran ", value=value, devices=devices, messagebox="messagefin")

    if devices =="pas de devices":
        devices={}

        return  render_template('capture.html', titre="Capture d'ecran ", value=value, devices=devices, messagebox="device")
    else :

        return render_template('capture.html', titre="Capture d'ecran",value=value, devices=devices, messagebox="")

@app.route('/Applications')
def applications():
    return render_template('applications.html', titre="Applications")

@app.route('/Installation', methods=['GET', 'POST'])
def app_install():
    dicApps=listApps()


    if request.method == 'POST':
        listeApps=request.form.getlist('checkO')


        for key,value in devices.items() :
            t = Thread(target=install, args=(value[2],listeApps,dicApps,))
            t.start()


    else:
        return render_template('app_install.html', titre="Installation d'application", dicApps=dicApps)


@app.route('/Recuperation', methods=['GET', 'POST'])
def app_recup():
    return render_template('app_install.html', titre="Récupreation d'application")

if __name__ == '__main__':
    app.run(debug=True)
