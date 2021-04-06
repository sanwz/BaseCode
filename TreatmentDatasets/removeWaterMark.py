from sys import flags
import cv2
import os
import numpy as np
import matplotlib as plt
import logging
from numpy.lib.function_base import select

from tqdm.cli import main

logging.basicConfig(filename= "fileterPicture.log",\
                        filemode="a+",format="%(asctime)s %(name)s:%(levelname)s:%(message)s", \
                        datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)

class RmWaterMark():
    def __init__(self, img) -> None:
        self.img = img
        self.winSize_width = img.shape[1]


    def rmWhiteWM(self, threshold):
        height, width, depth = self.img.shape[:3]
        thresh = cv2.inRange(self.img, np.array([threshold for i in range(3)]), np.array([255 for _ in range(3)]))
        kernel = np.ones((8, 8), np.uint8)
        hi_mask = cv2.dilate(thresh, kernel, iterations=1)
        self.specular = cv2.inpaint(self.img, hi_mask, 5, flags=cv2.INPAINT_TELEA)
    
    def show(self, Mode):
        """
        show the image by the Mode paragram, if you set Mode as "all", show all picture; "before" :show the initial picture;
        "after": show the dealed picture

        :param Mode: Mode
        :type Mode: str
        """
        if(self.img.shape[0]>800):
            self.img = cv2.resize(self.img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
            self.specular = cv2.resize(self.specular, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
        if(Mode == "all"):
            cv2.moveWindow("before", 400, 100)
            cv2.imshow("before", self.img)
            cv2.moveWindow("after", 400, 100)
            cv2.imshow("after", self.specular)
            cv2.waitKey()
        elif (Mode == "before"):
            cv2.imshow("before", self.img)
            cv2.waitKey()
        elif (Mode == "after"):
            cv2.imshow("after", self.specular)
            cv2.waitKey()
        else:
            raise ValueError("Mode paragram is wrong, 'all','before' or 'after'")

    def save(self, rootPath):
        """
        save the image after dealed

        :param rootPath: the filepath to save finished picture
        :type rootPath: str
        """
        pass
    def get_result(self):
        return self.specular
        

if __name__ == '__main__':
    img = cv2.imread("./1000011.jpg")
    rmWM = RmWaterMark(img)
    rmWM.rmWhiteWM(244)
    rmWM.show("all")