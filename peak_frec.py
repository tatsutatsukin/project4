# -*- coding: utf-8 -*-
"""Peak_Frec.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qNdwxXa9P_7HOtemdOgzn4jE54IEGkJz
"""

import glob
import re
import os
import argparse
import sys
import scipy.io.wavfile
import math
import numpy as np
import matplotlib.pyplot as plt

import math
from scipy import signal
from scipy import fftpack


class GetMonoInterval:
    #音名
    vecInterval=[]
    #周波数
    vecFreq=[]
    #周波数：音名
    mapInterval=[]
    #ファイル名
    filename=""
    #生データ
    data=[]
    #サンプリング周期
    rate=0
    #時間軸
    time=[]
    #FFT処理後データ
    fftData=[]
    #周波数リスト
    fftFreq=[]

        #コンストラクタ
    def __init__(self,file):
        #音名マップ
        #音名の配列作成
        self.vecInterval = ["A0","A#0","B0"]
        for i in range(1,8):
            self.vecInterval.append("C" + str(i))
            self.vecInterval.append("C#" + str(i))
            self.vecInterval.append("D" + str(i))
            self.vecInterval.append("D#" + str(i))
            self.vecInterval.append("E" + str(i))
            self.vecInterval.append("F" + str(i))
            self.vecInterval.append("F#" + str(i))
            self.vecInterval.append("G" + str(i))
            self.vecInterval.append("G#" + str(i))
            self.vecInterval.append("A" + str(i))
            self.vecInterval.append("A#" + str(i))
            self.vecInterval.append("B" + str(i))
        self.vecInterval.append("C8")
        #音程の周波数の配列作成
        self.vecFreq.append(27.5)
        semtiones = pow(2,1/12)
        for i in range(0,87):
            self.vecFreq.append(self.vecFreq[i]*semtiones)
        #二つの配列で「周波数:音名」dictを作成
        self.mapInterval = dict(zip(self.vecFreq,self.vecInterval))
        #print(self.mapInterval)
        
        #ファイル読み込み
        self.filename = file
        
        #音源読み込み
        self.rate, self.data = scipy.io.wavfile.read(self.filename)

        #横軸（時間）を作成
        self.time = np.arange(0,self.data.shape[0]/self.rate,1/self.rate)    #(0, 行数/サンプリング周波数, 1/サンプリング周波数)
        
        #FFT
        self.fftData = np.abs(np.fft.rfft(self.data))
        self.fftFreq = np.fft.fftfreq(self.fftData.shape[0],1.0/self.rate)
        #print(self.fftData)
        #print(self.fftFreq)

    #FFTを処理した波形を表示
    def returnNamePeak(self,peak):

        #ピーク値を取得
        fft_max_data = signal.argrelmax(self.fftData,order=peak)

        #最もゲインの大きいピークの周波数を返す
        maxPeakFreq = self.getPeakFreq(self.fftFreq[fft_max_data],self.fftData[fft_max_data])

        #その周波数に最も近い音名を返す
        if maxPeakFreq == 0.0:
          return "X"
        else:
          intervalName = self.searchInterval(maxPeakFreq)
          #print(intervalName)
          #print(type(intervalName))
          #print(self.fftFreq[fft_max_data])
          #print(type(self.fftFreq[fft_max_data]))
          return intervalName
    
   #searchInterval(周波数)
    def searchInterval(self,freq):
        """
        @freq  :音程を知りたい周波数
        @return:音程を返す
        """
        #平均率で最も近い周波数を検索
        nearfreq = self.getNearestValue(self.vecFreq,freq)
        #その音名
        nameInterval = self.mapInterval[nearfreq]
        return nameInterval
        
    #最も近い値を返す
    def getNearestValue(self,list, num):
        """
        概要: リストからある値に最も近い値を返却する関数
        @param list: データ配列
        @param num: 対象値
        @return 対象値に最も近い値
        """
        # リスト要素と対象値の差分を計算し最小値のインデックスを取得
        idx = np.abs(np.asarray(list) - num).argmin()
        return list[idx]
        
    #最もゲインの大きいピークの周波数を返す(周波数配列、ゲイン配列)
    def getPeakFreq(self,peakFreq,peakGain):
      #zipでタプル配列を作り、peakGainををkey,peakFreqをvalueとした辞書の作成
        mapMaxPeak = dict(zip(peakGain,peakFreq))
        #print(peakGain)
        #print(mapMaxPeak)
        
        try:
          maxPeakValue = np.amax(peakGain)
          #print(type(mapMaxPeak[maxPeakValue]))
          #print(mapMaxPeak[maxPeakValue])
          return mapMaxPeak[maxPeakValue]
        except ValueError:
          return 0.0
        
        """
        if(peakGain.size == 0):
          return 0
        else:
          maxPeakValue = np.amax(peakGain)
          return mapMaxPeak[maxPeakValue]
        """
          



class Peak:
  def __init__(self,dir_name):
    self.dir_name=dir_name
    self.peak_list=self.peak_dir(self.dir_name)
    #print(self.peak_list)
  
  def peak_dir(self,dir):
      peak_list=[]
      path_list = glob.glob(dir + '*.wav')       # 指定されたディレクトリ内の全てのwavファイルを取得
      #print(path_list)

      for name in path_list:
        #print('filename:',name)
        temp = GetMonoInterval(name)
        tempInterval = temp.returnNamePeak(800)
        peak_list.append(tempInterval)

      #print(peak_list)
      return peak_list

#mono = GetMonoInterval("/content/drive/MyDrive/data_output/10000.wav")
#mono = GetMonoInterval("/content/drive/MyDrive/project4/music_file/no.wav")
#monoInterval, monoFrec = mono.returnNamePeak(1000)
#print(monoInterval)