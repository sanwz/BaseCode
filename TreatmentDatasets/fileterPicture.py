#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -----------------------------------------------------
# @Filename    :fileterPicture.py
# @Notice    : Downloaded picture may be damaged , auto delete
#              the damaged picture
# @Time    :2021/04/06 09:17:25
# @Author    :sangwz
# @Version    :v1.0
# ----------------------------------------------------

from typing import Sized
import cv2
import numpy as np
import sys
import os
import logging
import shutil
import threading
from tqdm import tqdm


sem = threading.Semaphore(100)

def checkPictureDamaged(filename,rootPath = None):
    """
    check the picture whether being damaged,

    :param filename: the image name
    :rootPath : the image root path
    """
    with sem:
        if(rootPath):
            filename = os.path.join(rootPath, filename)
        if(filename.endswith(".jpg")): # if the image was damaged while downloading, check the end of the picture encoding 
            with open(filename, "rb") as file:
                file.seek(-2, 2)
                if file.read() != b'\xff\xd9':
                    return True
        img = cv2.imread(filename)
        if (os.path.exists(filename) == False): 
            raise ValueError("wrong path")
        if(img.all() != None):
            maxRows = img.shape[0]
            maxCols = img.shape[1]
            # print(maxRows, "-------", maxCols)
            # print(img.shape)
            # cv2.imshow("", img)
            # cv2.waitKey(0)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 文件下载完成，查看是否在300行内所有像素点的值都是一样的。
            for i in range(int(maxRows/2), maxRows-300, 300):
                if(((img[i:i+300,:] - img[i][0]) == 0).all()):
                    return True
            return False
        else:
            return True
    
def checkFilelist(rootPath, DamagedPath):
    """
    check the files in fileList
    :param rootPath: images root path
    :type rootPath: str
    :param DamagedPath: store damaged image
    :type DamagedPath: str
    """
    fileList = os.listdir(rootPath)
    if (os.path.exists(DamagedPath) == False):
        os.mkdir(DamagedPath)
        logging.info("Make the damaged images directory")
        
    for i in tqdm(range(len(fileList))):
        filename = fileList[i]
        if checkPictureDamaged(filename, rootPath=rootPath):
            newPath = os.path.join(DamagedPath, filename)
            oldPath = os.path.join(rootPath, filename)
            shutil.move(oldPath, newPath)
            print("remove the picture %s", filename)
            logging.info("remove the picture %s to %s"%(oldPath, newPath))
    
if __name__ == '__main__':
    rootPath = "F:\\Datasets\\MyCollection\\marineTraffic\\image"
    DamagedPath = "F:\\Datasets\\MyCollection\\marineTraffic\\Damaged"
    
    logging.basicConfig(filename=os.path.join(rootPath, "fileterPicture.log"),\
                        filemode="a+",format="%(asctime)s %(name)s:%(levelname)s:%(message)s", \
                        datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)
    checkFilelist(rootPath, DamagedPath)
    # checkPictureDamaged("./1027456.jpg")
    
