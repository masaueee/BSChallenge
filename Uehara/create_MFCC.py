# coding: utf-8
import os
import sys
import glob
import librosa
import librosa.display
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import subprocess

def calc_mfcc(infile_path,outfile_path):
    y, sr = librosa.load(infile_path, sr=4410, offset = 0.0)
    n_mels = 128
    hop_length = 2068
    n_fft = 2048
    S = librosa.feature.melspectrogram(y=y, sr=sr,n_mels=n_mels, hop_length=hop_length, n_fft=n_fft)
    log_S = librosa.power_to_db(S, np.max)
    plt.figure(figsize=(12, 4))
    librosa.display.specshow(data=log_S, sr=sr, hop_length=hop_length, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel spectrogram')
    plt.tight_layout()
    plt.savefig(outfile_path)


cwd = os.getcwd()
artists_list = [filename for filename in os.listdir(cwd + "/data/input/") if not filename.startswith('.')]
for artist in artists_list:
    music_list = [filename for filename in os.listdir(cwd + "/data/input/" + artist + "/") if not filename.startswith('.')]
    for music in music_list:
        wavfiles = [filename for filename in os.listdir("{}/data/input/{}/{}/".format(cwd, artist, music)) if not filename.startswith('.')]
        for wavfile in wavfiles:
            infile_path  = "{}/data/input/{}/{}/{}".format(cwd, artist, music, wavfile)
            outfile_dir = "{}/data/output/{}/{}".format(cwd, artist, music)
            cmd = "mkdir -p " + outfile_dir
            subprocess.check_output(cmd.split())
            outfile_path = "{}/data/output/{}/{}/{}.png".format(cwd, artist, music, wavfile.replace(".wav", ""))
            calc_mfcc(infile_path,outfile_path)
