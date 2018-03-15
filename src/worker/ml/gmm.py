#利用gmm模型对球场像素分类
# -*- coding:utf-8 -*-
import cv2
import numpy as np
import glob,os
from sklearn.mixture import GaussianMixture
from sklearn.externals import joblib
import time
if __name__=="__main__":
    #依次打开所有训练图像，计算主色
    #定义一个二维数组
    start = time.time()
    cbcrArray=np.array([[0,0]])
    for files in glob.glob("img//*.jpg"):
        filepath, filename = os.path.split(files)
        filterame, exts = os.path.splitext(filename)
        img = cv2.imread(files)
        #抽取主色区域
        rows, cols, _ = img.shape
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        y, cr, cb = cv2.split(ycrcb)  # y是灰度
        hist, xbins, ybins = np.histogram2d(cr.ravel(), cb.ravel(), [240, 240], [[0, 240], [0, 240]])
        # 得到最大值的index
        index = hist.argmax()
        # 主峰p1
        cr = int(index / 240)
        cb = index % 240
        # 求连通域
        # 求出和主峰对应的cb 和 cr相连通的区域
        # 二值化、不考虑低亮度区域
        ret1, threshold = cv2.threshold(y, 127, 255, cv2.THRESH_BINARY)
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
                    #加入训练数据
                    if crmin < mycr < crmax and cbmin < mycb < cbmax:
                        data = [mycr, mycb]
                        cbcrArray = np.row_stack((cbcrArray, data))
    #去掉第一个数据
    cbcrArray=np.delete(cbcrArray,0,0)
    clf = GaussianMixture(n_components=3)
    clf.fit(cbcrArray)
    end = time.time()
    #保存模型
    joblib.dump(clf, "train_model.m")
    print("运行时间为:",end-start)