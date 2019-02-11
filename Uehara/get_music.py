#!/usr/bin/python
# coding: utf-8

import get_videosId_from_playlist
import subprocess
import os
import sys
from get_videosId_from_playlist import videos


args = sys.argv
artist_name = args[1]
cwd = os.getcwd()

if os.path.exists("/Users/masahiro/.pyenv/shims/ffmpeg") == False:
    cmd = "ln -s /Users/masahiro/python_scripts/ffmpeg /Users/masahiro/.pyenv/shims/ffmpeg"
    subprocess.check_output(cmd.split())
if os.path.exists("/Users/masahiro/.pyenv/shims/ffprobe") == False:
    cmd = "ln -s /Users/masahiro/python_scripts/ffprobe /Users/masahiro/.pyenv/shims/ffprobe"
    subprocess.check_output(cmd.split())


#list = get_videosId_from_playlist.get_videoslist("PL2asJ5KzP_gxSWCYGlq2C_p46p3dWsz3W", 100)     #Perfume
#list = get_videosId_from_playlist.get_videoslist("PLoY0enzhPx2cqimHp1RZTedyfbTWt7CN5", 127)     #MrChildren
#list = get_videosId_from_playlist.get_videoslist("PL2qplHrkMEV2nysubMrgSm_kgsCOt4ABc", 52)    #椎名林檎＆東京事変
#list = get_videosId_from_playlist.get_videoslist("PL9E8B1088C1E4C364", 129)                     #モー娘。
#list = get_videosId_from_playlist.get_videoslist("PLvt3UoZ0f1I_xSB0joYb1lBRdIrvp14Cq", 85)     #RADWIMPS
#list = get_videosId_from_playlist.get_videoslist("PLuylb7DJT7NmBRf7LHqHaK537xx-ihLVW", 103)     #安室奈美恵
#list = get_videosId_from_playlist.get_videoslist("PLBE4VAbp9-xmqnueAp0b7dT3V5AGMk7_p", 52)     #宇多田ヒカル
#list = get_videosId_from_playlist.get_videoslist("PLFCBB7A75C835C03E", 80)                     #福山雅治
list = get_videosId_from_playlist.get_videoslist("PL6LL6bATt3FtrftcyFYBSq2UXKglBQZ3W", 88)     #スピッツ
#list = get_videosId_from_playlist.get_videoslist("PLqncrgMY2pY4DTMKk6YNsGyaN-lXz5Zh0", 72)     #ポルノグラフィティ
#list = get_videosId_from_playlist.get_videoslist("PLoY0enzhPx2cy3ySudH4pOkgs8MGM5QzE", 120)    #ASIANKANG-FUGENERATION
#list = get_videosId_from_playlist.get_videoslist("PL9MHpazTdQCBOwRAlpb0EZnyct3Ej7t7W", 77)    #スキマスイッチ
#list = get_videosId_from_playlist.get_videoslist("PLHcJQn3tSs7j9PR1iJSYEFN_RkzX6LGJG", 40)    #Greeeen
#list = get_videosId_from_playlist.get_videoslist("PLIyWtPwrYr7bfm1M13cqwdeKqLD-3tChb", 63)    #サカナクション



print(list)

video_URL = ""
file_name = ""

for video in list:
    success_flag = True
    video_URL = "https://www.youtube.com/watch?v=" + video.id
    cmd = "youtube-dl -x --audio-format wav -o '%(id)s.' " + video_URL
    try:
        subprocess.check_output(cmd.split())
    except:
        success_flag = False

    #input_name = video.id + ".wav"
    input_name = "'" + video.id + ".wav"

    i=0
    if success_flag :
        while((i+1)*30<=video.second):
            #30秒ごとに分割する
            #output_name = "Musics/ViewCount=" + video.viewcount + "&_&ID=" + video.id + ".wav"

            music_dir = cwd + "/Musics/" + artist_name + "/ViewCount=" + video.viewcount + "&_&ID=" + video.id
            cmd = "mkdir -p " + music_dir
            subprocess.check_output(cmd.split())
            music_path = music_dir + "/" + str(i+1) + ".wav"
            cmd = "ffmpeg -ss " + str(i*30.0) + " -i " + input_name + " -t 30.0 " + music_path
            subprocess.check_output(cmd.split())

            i=i+1

        cmd = "rm " + input_name
        subprocess.check_output(cmd.split())
