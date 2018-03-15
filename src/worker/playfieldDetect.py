# -*- coding:utf-8 -*-
#球场检测
import cv2
import numpy as np
class playfieldDetect:
    @staticmethod
    #基于直方图的主色提取
    def dominantColorExtraction(img):
        rows, cols, _ = img.shape
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        y, cr, cb = cv2.split(ycrcb)  # y是灰度
        hist, xbins, ybins = np.histogram2d(cr.ravel(), cb.ravel(), [240, 240], [[0, 240], [0, 240]])
        # 得到最大值的index
        index = hist.argmax()
        # 主峰p1
        cr = int(index / 240)
        cb = index % 240
        # 二值化、不考虑低亮度区域（球场区域的亮度高）
        ret1, threshold = cv2.threshold(y, 155, 255, cv2.THRESH_BINARY)
        t = 0.1
        cbmin = cb * (1 - t)
        cbmax = cb * (1 + t)
        crmin = cr * (1 - t)
        crmax = cr * (1 + t)
        for row in range(rows):
            for col in range(cols):
                # 只考虑高亮度区域
                if threshold[row][col] == 255:
                    _, mycr, mycb = ycrcb[row][col]
                    if not (crmin < mycr < crmax and cbmin < mycb < cbmax):
                        threshold[row][col] = 0
        #masked = cv2.bitwise_and(img, img, mask=threshold)
        #返回掩码图
        return threshold