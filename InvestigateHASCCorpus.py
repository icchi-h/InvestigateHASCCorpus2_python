#!/usr/bin/env python
# coding: utf-8

"""
__doc__
HASC Corpusに含まえる各ファイル数や人数などを調査するプログラム
"""
import csv
import glob
import os
import sys
import numpy as np

print(__doc__)
__author__ = "Haruyuki Ichino"
__version__ = "0.1"
__date__ = "2016/05/21"

# データ格納ディレクトリ
inputDir = './data/'
# 結果の出力ファイル
outputFile = './result.txt'

# Const
InvestigateTimeFlag = True
# InvestigateTimeFlag = False


# ==========================================================
# 関数
# ==========================================================

def getFileTime(file):
    """
    概要: ファイルに含まれるデータ時間を返却する関数
    @param file:fileオブジェクト
    @return 時間[s]
    """

    # csvファイルからデータの読み込み
    data = np.loadtxt(file, delimiter=",")
    # print("(行,列) =", data.shape)

    # 最初の0が続く部分を削除
    idx_rm0 = 0
    while data[0, 1] == 0:  # 一番上のx軸の値
        data = np.delete(data, 0, axis=0)
        idx_rm0 += 1
    # print("Delete 0 value lines =", idx_rm0)

    # 有効なデータ(行)数のチェック
    dataLines = data.shape[0]  # ファイルデータの最下部のインデックス
    # print("Total lines =", dataLines)
    TotalTime = data[dataLines - 1, 0] - data[0, 0]

    return TotalTime


# ==========================================================
# 0. 準備
# ==========================================================

# 入力HASCデータの調査
# dataディレクトリの存在確認
if not os.path.isdir(inputDir):
    print("dataディレクトリが存在してないで")
    sys.exit(1)

activityLabel = []  # 行動管理list
activityCount = 0  # 行動数

# 行動の種類をactions_lsitに追加し, 行動数をAction_countに入れる
activitys = os.listdir(inputDir)
for activity in activitys:
    actionDir = inputDir + activity + '/'

    if not os.path.isdir(actionDir):
        continue

    activityLabel.append(activity)
    activityCount += 1

print("Activity count =", activityCount)
print("Activity label =", activityLabel)
print()

# ファイル出力の準備
f = open(outputFile, "w")

# ==========================================================
# 1.データの読み込み
# ==========================================================

# カウンター
totalAccCount = 0
totalGyroCount = 0
totalMagCount = 0
totalLabelCount = 0
totalMetaCount = 0
totalPersonCount = 0
totalAccTime = 0
totalGyroTime = 0
totalMagTime = 0
activityAccCount = 0
activityGyroCount = 0
activityMagCount = 0
activityLabelCount = 0
activityMetaCount = 0
activityPersonCount = 0
activityAccTime = 0
activityGyroTime = 0
activityMagTime = 0

# 行動ディレクトリでの処理
for activity in activitys:
    # .DS_Storeのチェック
    if activity == ".DS_Store":
        continue

    actionDir = inputDir + activity + '/'

    # ディレクトリじゃない場合はスキップ
    if not os.path.isdir(actionDir):
        continue

    print("=================================================")
    print(actionDir)
    print("=================================================")
    f.writelines("=================================================\n")
    f.writelines(actionDir + "\n")
    f.writelines("=================================================\n")

    # カウンターの初期化
    activityAccCount = 0
    activityGyroCount = 0
    activityMagCount = 0
    activityLabelCount = 0
    activityMetaCount = 0
    activityPersonCount = 0
    activityAccTime = 0
    activityGyroTime = 0
    activityMagTime = 0

    # 被験者別の処理
    persons = os.listdir(actionDir)
    print("person count =", len(persons))

    # カウンターの更新
    activityPersonCount += len(persons)

    for person in persons:
        # .DS_Storeのチェック
        if person == ".DS_Store":
            continue

        personDir = actionDir + person + '/'

        # ディレクトリじゃない場合はスキップ
        if not os.path.isdir(personDir):
            continue

        # print("============================================")
        # print(person)
        # print("============================================")

        # 各ファイルリストの作成
        accFiles = glob.glob(personDir + '*acc*')
        gyroFiles = glob.glob(personDir + '*gyro*')
        magFiles = glob.glob(personDir + '*mag*')
        metaFiles = glob.glob(personDir + '*meta*')
        labelFiles = glob.glob(personDir + '*label*')

        # カウンターの更新
        activityAccCount += len(accFiles)
        activityGyroCount += len(gyroFiles)
        activityMagCount += len(magFiles)
        activityMetaCount += len(metaFiles)
        activityLabelCount += len(labelFiles)

        # 時間調査フラグ
        if InvestigateTimeFlag:

            # 各加速度ファイルにアクセス
            for accFile in accFiles:
                activityAccTime += getFileTime(accFile)
            # 各gyroファイルにアクセス
            for gyroFile in gyroFiles:
                activityGyroTime += getFileTime(gyroFile)
            # 各magファイルにアクセス
            for magFile in magFiles:
                activityMagTime += getFileTime(magFile)

        # 各person処理の終了

    # 各行動に含まれるファイル数の表示
    print("Acc count = %d" % activityAccCount)
    print("Gyro count = %d" % activityGyroCount)
    print("Mag count = %d" % activityMagCount)
    print("Meta count = %d" % activityMetaCount)
    print("Label count = %d" % activityLabelCount)
    print()
    if InvestigateTimeFlag:
        # 各行動に含まれるファイルの時間を表示
        print("Acc file time %.1f[s] (%.1f[s]/person)" % (activityAccTime, activityAccTime / activityPersonCount))
        print("Gyro file time %.1f[s] (%.1f[s]/person)" % (activityGyroTime, activityGyroTime / activityPersonCount))
        print("Mag file time %.1f[s] (%.1f[s]/person)" % (activityMagTime, activityMagTime / activityPersonCount))
        print()

    # 各行動に含まれるファイル数を書き込み
    f.writelines("Acc count = %d\n" % activityAccCount)
    f.writelines("Gyro count = %d\n" % activityGyroCount)
    f.writelines("Mag count = %d\n" % activityMagCount)
    f.writelines("Meta count = %d\n" % activityMetaCount)
    f.writelines("Label count = %d\n" % activityLabelCount)
    f.writelines("\n")
    if InvestigateTimeFlag:
        # 各行動に含まれるファイルの時間を表示
        f.writelines("Acc file time %.1f[s] (%.1f[s]/person)\n" % (activityAccTime, activityAccTime / activityPersonCount))
        f.writelines("Gyro file time %.1f[s] (%.1f[s]/person)\n" % (activityGyroTime, activityGyroTime / activityPersonCount))
        f.writelines("Mag file time %.1f[s] (%.1f[s]/person)\n" % (activityMagTime, activityMagTime / activityPersonCount))
        f.writelines("\n")

    # カウンターの更新
    totalPersonCount += activityPersonCount
    totalAccCount += activityAccCount
    totalGyroCount += activityGyroCount
    totalMagCount += activityMagCount
    totalMetaCount += activityMetaCount
    totalLabelCount += activityLabelCount
    totalAccTime += activityAccTime
    totalGyroTime += activityGyroTime
    totalMagTime += activityMagTime

    # 各行動への処理の終了

# 全体のファイル数の表示
print("===================================================")
print("Summary")
print("===================================================")
print("Total person count = %d" % totalPersonCount)
print("Total acc count = %d" % totalAccCount)
print("Total gyro count = %d" % totalGyroCount)
print("Total mag count = %d" % totalMagCount)
print("Total meta count = %d" % totalMetaCount)
print("Total label count =  %d" % totalLabelCount)
print()
if InvestigateTimeFlag:
    print("Total acc file time %.1f[s] (%.1f[s]/person)" % (totalAccTime, totalAccTime / totalPersonCount))
    print("Total gyro file time %.1f[s] (%.1f[s]/person)" % (totalGyroTime, totalGyroTime / totalPersonCount))
    print("Total mag file time %.1f[s] (%.1f[s]/person)" % (totalMagTime, totalMagTime / totalPersonCount))

# 結果をファイル出力
f.writelines("==================================================\n")
f.writelines("Summary\n")
f.writelines("===================================================\n")
f.writelines("Total person count = %d\n" % totalPersonCount)
f.writelines("Total acc count = %d\n" % totalAccCount)
f.writelines("Total gyro count = %d\n" % totalGyroCount)
f.writelines("Total mag count = %d\n" % totalMagCount)
f.writelines("Total meta count = %d\n" % totalMetaCount)
f.writelines("Total label count =  %d\n" % totalLabelCount)
f.writelines("\n")
if InvestigateTimeFlag:
    f.writelines("Total acc file time %.1f[s] (%.1f[s]/person)\n" % (totalAccTime, totalAccTime / totalPersonCount))
    f.writelines("Total gyro file time %.1f[s] (%.1f[s]/person)\n" % (totalGyroTime, totalGyroTime / totalPersonCount))
    f.writelines("Total mag file time %.1f[s] (%.1f[s]/person)\n" % (totalMagTime, totalMagTime / totalPersonCount))

# ファイル出力の終了処理
f.close()
