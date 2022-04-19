# 导入模块
import numpy as np
import os
import cv2


# 计算多张，并保存到csv文件中
def Calculate_percentage(img_path='/data/Rock/330-2.jpg'):
    img = cv2.imread(img_path, 1)  # 三通道读取
    gray = img[:, :, ::-1]  # BGR to RGB
    # cv2.threshold (源图片, 阈值, 填充色, 阈值类型)
    ret, thresh2 = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)  # 小于150的像素为0，大于150的像素为255

    # 将二值化后的图转成numpy格式
    dist_transform = np.array(thresh2)
    h, w, _ = dist_transform.shape  # 取出维度
    # print("维度为：",dist_transform.shape)

    # 取出三通道
    img_R = dist_transform[:, :, 0]
    img_G = dist_transform[:, :, 1]
    img_B = dist_transform[:, :, 2]


    # 要求绿色和黄色部分。黄色部分由红色和绿色结合而成
    # 因此所求区域为：像素绿色通道部分为255，且该像素位置蓝色通道为0。此时红色通道为255时显示为黄色；为0时显示为绿色
    # G通道与B通道求交集。再将绿色通道减区交集，得到的区域即为所求区域
    img_G[img_G > 0] = 1  # 将255化为1
    img_B[img_B > 0] = 1
    GB = img_G + img_B
    GB = GB == 2  # 取出共同部分--交集，也就是都是G和B都是1的部分
    img_final = img_G - GB
    result = np.sum(img_final) / (h * w)  # 计算百分比
    result_per = "{:0.4f}".format(result * 100)
    # print("百分比为：{:0.4f}%".format(result*100))
    return result_per

# OTSU算法代码，尝试寻找最优阈值
'''
import math
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

threshold_values = {}
h = [1]

def Hist(img):
   row, col = img.shape 
   y = np.zeros(256)
   for i in range(0,row):
      for j in range(0,col):
         y[img[i,j]] += 1
   x = np.arange(0,256)
   plt.bar(x, y, color='b', width=5, align='center', alpha=0.25)
   plt.show()
   return y


def regenerate_img(img, threshold):
    row, col = img.shape 
    y = np.zeros((row, col))
    for i in range(0,row):
        for j in range(0,col):
            if img[i,j] >= threshold:
                y[i,j] = 255
            else:
                y[i,j] = 0
    return y



def countPixel(h):
    cnt = 0
    for i in range(0, len(h)):
        if h[i]>0:
           cnt += h[i]
    return cnt


def wieght(s, e):
    w = 0
    for i in range(s, e):
        w += h[i]
    return w


def mean(s, e):
    m = 0
    w = wieght(s, e)
    for i in range(s, e):
        m += h[i] * i

    return m/float(w)


def variance(s, e):
    v = 0
    m = mean(s, e)
    w = wieght(s, e)
    for i in range(s, e):
        v += ((i - m) **2) * h[i]
    v /= w
    return v


def threshold(h):
    cnt = countPixel(h)
    for i in range(1, len(h)):
        vb = variance(0, i)
        wb = wieght(0, i) / float(cnt)
        mb = mean(0, i)

        vf = variance(i, len(h))
        wf = wieght(i, len(h)) / float(cnt)
        mf = mean(i, len(h))

        V2w = wb * (vb) + wf * (vf)
        V2b = wb * wf * (mb - mf)**2

        fw = open("/data/trace.txt", "a")
        fw.write('T='+ str(i) + "\n")

        fw.write('Wb='+ str(wb) + "\n")
        fw.write('Mb='+ str(mb) + "\n")
        fw.write('Vb='+ str(vb) + "\n")

        fw.write('Wf='+ str(wf) + "\n")
        fw.write('Mf='+ str(mf) + "\n")
        fw.write('Vf='+ str(vf) + "\n")

        fw.write('within class variance='+ str(V2w) + "\n")
        fw.write('between class variance=' + str(V2b) + "\n")
        fw.write("\n")

        if not math.isnan(V2w):
            threshold_values[i] = V2w


def get_optimal_threshold():
    max_V2w = max(threshold_values.values())#itervalues())
    optimal_threshold = [k for k, v in threshold_values.items() if v == max_V2w]#
    print('optimal threshold', optimal_threshold[0])
    return optimal_threshold[0]


# image = Image.open('/data/image/341-2.jpg').convert("L")
# img = np.asarray(image)
img = cv2.imread('/data/image/323-2.jpg')
img = np.asarray(img)
plt.imshow(img)
plt.show()
gray = img[:,:,::-1]#BGR to RGB
# ret,thresh = cv2.threshold(gray, 150 ,150, cv2.THRESH_BINARY)
new_img = gray[:,:,1]#RGB中的G

old_img = regenerate_img(new_img,150)
plt.imshow(old_img)
plt.show()

# h = Hist(new_img)
# # print(h)
# threshold(h)
# op_thres = get_optimal_threshold()

# res = regenerate_img(new_img, op_thres)
# plt.imshow(res)
# plt.show()
# plt.savefig("/data/otsu_341-2.jpg")
'''