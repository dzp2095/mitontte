#将视频处理之后发回界面线程处理
# -*- coding:utf-8 -*-

import numpy
import cv2
from src.worker.edgeDetect import edgeDetect
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ImageQt import ImageQt

class videoHandleThread(QtCore.QThread):

    #发送处理完的一帧回界面
    sendFrameSignal = QtCore.pyqtSignal(QPixmap)

    def __init__(self,filename,framSize,parent=None):
        self.filename=filename
        super(videoHandleThread, self).__init__(parent)
        #帧大小
        self.framSize=framSize
        self.goOn=True
    def run(self):
        cap = cv2.VideoCapture(self.filename)
        while (cap.isOpened()):
            if self.goOn:
                ret, frame = cap.read()
                frame=edgeDetect.cannyDetect(frame)
                #转换为QPixmap
                frameImage=Image.fromarray(frame)
                frameImage=frameImage.resize((self.framSize.width(),self.framSize.height()))
                framePixmap = QPixmap.fromImage(ImageQt(frameImage))
                framePixmap.scaled(self.framSize)
                self.sendFrameSignal.emit(framePixmap)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
            #暂停，100毫秒之后再检查
            else:
                self.msleep(100)
        cap.release()
        cv2.destroyAllWindows()

    #主界面大小改变
    def onReceiveVideoLabelResize(self,size):
        self.framSize=size

    def onReceivePauseSignal(self):
        self.goOn=not self.goOn