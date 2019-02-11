# coding: utf-8
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request
import time
import os
import sys
import glob
import subprocess

#choromeのdriverを定義
driver_path = "/Users/masahiro/python_scripts/chromedriver"
driver= webdriver.Chrome(executable_path=driver_path)
driver.get("http://unetvocalsep.herokuapp.com/")
time.sleep(5)

def extract_voice(infile_path, outfile_path):

    JS_DROP_FILE = "var tgt=arguments[0],e=document.createElement('input');e.type='"+\
    "file';e.addEventListener('change',function(event){var dataTrans" +\
    "fer={dropEffect:'',effectAllowed:'all',files:e.files,items:{},t" +\
    "ypes:[],setData:function(format,data){},getData:function(format" +\
    "){}};var emit=function(event,target){var evt=document.createEve" +\
    "nt('Event');evt.initEvent(event,true,false);evt.dataTransfer=da"+\
    "taTransfer;target.dispatchEvent(evt);};emit('dragenter',tgt);em"+\
    "it('dragover',tgt);emit('drop',tgt);document.body.removeChild(e"+\
    ");},false);document.body.appendChild(e);return e;"

    drop_area = driver.find_element_by_id("dropbox")

    tmp = driver.execute_script(JS_DROP_FILE, drop_area)
    tmp.send_keys(infile_path)
    # check the status
    status = driver.find_element_by_id("dropbox").text
    while status == "Processing, please wait...":
        time.sleep(3)
        status = driver.find_element_by_id("dropbox").text

    url = driver.find_element_by_id("audio-vocal").get_attribute("src")
    urllib.request.urlretrieve(url, outfile_path)


cwd = os.getcwd()
artists_list = [filename for filename in os.listdir(cwd + "/Musics/") if not filename.startswith('.')]
for artist in artists_list:
    music_list = [filename for filename in os.listdir(cwd + "/Musics/" + artist + "/") if not filename.startswith('.')]
    for music in music_list:
        wavfiles = [filename for filename in os.listdir("{}/Musics/{}/{}/".format(cwd, artist, music)) if not filename.startswith('.')]
        for wavfile in wavfiles:
            infile_path  = "{}/Musics/{}/{}/{}".format(cwd, artist, music, wavfile)
            outfile_dir = "{}/data/input/{}/{}".format(cwd, artist, music)
            cmd = "mkdir -p " + outfile_dir
            subprocess.check_output(cmd.split())
            outfile_path = "{}/data/input/{}/{}/{}".format(cwd, artist, music, wavfile)
            extract_voice(infile_path, outfile_path)


"""
cwd = os.getcwd()
artists_list = os.listdir(cwd + "/Musics/")

for artist in artists_list:
    music_list = os.listdir(cwd + "/Musics/" + artist + "/")
    for music in music_list:
        wavfiles = os.listdir("{}/Musics/{}/{}/".format(cwd, artist, music))
        for wavfile in wavfiles:
            infile_path  = "{}/Musics/{}/{}/{}".format(cwd, artist, music, wavfile)
            outfile_dir = "{}/data/input/{}/{}".format(cwd, artist, music)
            cmd = "mkdir -p " + outfile_dir
            subprocess.check_output(cmd.split())
            outfile_path = "{}/data/input/{}/{}/{}".format(cwd, artist, music, wavfile)
            extract_voice(infile_path, outfile_path)



        def get_voice(artist_name):
            #引数ディレクトリ直下の音楽一覧を取得
            path_list = glob.glob("/Users/masahiro/python_scripts/Musics/" + artist_name + "/*")
            for file_path in path_list:
                file_name = os.path.basename(file_path)
                voice_path = "/Users/masahiro/python_scripts/Voices/" + artist_name + "/" + file_name
                extract_voice(file_path, voice_path)


        voice_dir = cwd + "/data/input/" + artist_name + "/ViewCount=" + video.viewcount + "&_&ID=" + video.id
        cmd = "mkdir -p " + voice_dir
        subprocess.check_output(cmd.split())
        voice_path = voice_dir + "/" + str(i+1) + ".wav"

        extract_voice(music_path, voice_path)
"""
