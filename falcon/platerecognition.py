import cv2
import numpy as np
import matplotlib.pyplot as plt
 
###############################
######  theme: 车牌识别   ######
######   author: 行歌     ######
######   time: 2018.3.23  ######
################################
 
def predict(imageArr):
    """
    这个函数通过一系列的处理，找到可能是车牌的一些矩形区域
    输入： imageArr是原始图像的数字矩阵
    输出：gray_img_原始图像经过高斯平滑后的二值图
          contours是找到的多个轮廓
    可以继续改进让它适应菱形！！！
    """
    img_copy = imageArr.copy()
    gray_img = cv2.cvtColor(img_copy , cv2.COLOR_BGR2GRAY)
    gray_img_ = cv2.GaussianBlur(gray_img, (5,5), 0, 0, cv2.BORDER_DEFAULT)
    kernel = np.ones((23, 23), np.uint8)#调节kernal size
    img_opening = cv2.morphologyEx(gray_img, cv2.MORPH_OPEN, kernel)
    img_opening = cv2.addWeighted(gray_img, 1, img_opening, -1, 0)
    # 找到图像边缘
    ret, img_thresh = cv2.threshold(img_opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(cv2.THRESH_OTSU)
    print("cv2.THRESH_BINARY")
    img_edge = cv2.Canny(img_thresh, 100, 200)
    # # 使用开运算和闭运算让图像边缘成为一个整体
    kernel = np.ones((10, 10), np.uint8)
    img_edge1 = cv2.morphologyEx(img_edge, cv2.MORPH_CLOSE, kernel)
    img_edge2 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, kernel)
    # # 查找图像边缘整体形成的矩形区域，可能有很多，车牌就在其中一个矩形区域中
    contours, hierarchy = cv2.findContours(img_edge2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return img_edge2,contours

def  chose_licence_plate(contours,Min_Area = 2000):
    """
    这个函数根据车牌的一些物理特征（面积等）对所得的矩形进行过滤
    输入：contours是一个包含多个轮廓的列表，其中列表中的每一个元素是一个N*1*2的三维数组
    输出：返回经过过滤后的轮廓集合
    
    拓展：
    （1） OpenCV自带的cv2.contourArea()函数可以实现计算点集（轮廓）所围区域的面积，函数声明如下：
            contourArea(contour[, oriented]) -> retval
        其中参数解释如下：
            contour代表输入点集，此点集形式是一个n*2的二维ndarray或者n*1*2的三维ndarray
            retval 表示点集（轮廓）所围区域的面积
    （2） OpenCV自带的cv2.minAreaRect()函数可以计算出点集的最小外包旋转矩形，函数声明如下：
             minAreaRect(points) -> retval      
        其中参数解释如下：
            points表示输入的点集，如果使用的是Opencv 2.X,则输入点集有两种形式：一是N*2的二维ndarray，其数据类型只能为 int32
                                    或者float32， 即每一行代表一个点；二是N*1*2的三维ndarray，其数据类型只能为int32或者float32
            retval是一个由三个元素组成的元组，依次代表旋转矩形的中心点坐标、尺寸和旋转角度（根据中心坐标、尺寸和旋转角度
                                    可以确定一个旋转矩形）
    （3） OpenCV自带的cv2.boxPoints()函数可以根据旋转矩形的中心的坐标、尺寸和旋转角度，计算出旋转矩形的四个顶点，函数声明如下：
             boxPoints(box[, points]) -> points
        其中参数解释如下：
            box是旋转矩形的三个属性值，通常用一个元组表示，如（（3.0，5.0），（8.0，4.0），-60）
            points是返回的四个顶点，所返回的四个顶点是4行2列、数据类型为float32的ndarray，每一行代表一个顶点坐标              
    """
    temp_contours = []
    for contour in contours:
        if cv2.contourArea( contour ) > Min_Area:
            temp_contours.append(contour)
    car_plate = []
    for temp_contour in temp_contours:
        rect_tupple = cv2.minAreaRect( temp_contour )
        rect_width, rect_height = rect_tupple[1]
        if rect_width < rect_height:
            rect_width, rect_height = rect_height, rect_width
        aspect_ratio = rect_width / rect_height
        # 车牌正常情况下宽高比在2 - 5.5之间
        if aspect_ratio > 2 and aspect_ratio < 5.5:
            car_plate.append( temp_contour )
            rect_vertices = cv2.boxPoints( rect_tupple )
            rect_vertices = np.int0( rect_vertices )
    return  car_plate
 
 
 
def license_segment( car_plates ):
    """
    此函数根据得到的车牌定位，将车牌从原始图像中截取出来，并存在当前目录中。
    输入： car_plates是经过初步筛选之后的车牌轮廓的点集 
    输出:   "card_img.jpg"是车牌的存储名字
    """
    #print(car_plates)
    if len(car_plates)<10:
        for car_plate in car_plates:
            row_min,col_min = np.min(car_plate[:,0,:],axis=0)
            row_max, col_max = np.max(car_plate[:, 0, :], axis=0)
            cv2.rectangle(img, (row_min,col_min), (row_max, col_max), (0,255,0), 2)
            card_img = img[col_min:col_max,row_min:row_max,:]
            cv2.imshow("img", img)
        cv2.imwrite( "card_img.jpg", card_img)
        cv2.imshow("card_img.jpg", card_img)
        cv2.waitKey(30000)
        cv2.destroyAllWindows()
    return  "card_img.jpg"


def imread_photo(filename,flags = cv2.IMREAD_COLOR ):
    """
    该函数能够读取磁盘中的图片文件，默认以彩色图像的方式进行读取
    输入： filename 指的图像文件名（可以包括路径）
          flags用来表示按照什么方式读取图片，有以下选择（默认采用彩色图像的方式）：
              IMREAD_COLOR 彩色图像
              IMREAD_GRAYSCALE 灰度图像
              IMREAD_ANYCOLOR 任意图像
    输出: 返回图片的通道矩阵
    """
    return  cv2.imread(filename,flags)
    
 
 
 
if __name__ == "__main__":
    img = cv2.imread('/Users/falcon/Desktop/学习/毕业设计/test1.jpg',flags = cv2.IMREAD_COLOR)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img_,contour=predict(img)
    car=chose_licence_plate(contour)
    license_segment(car)
    cv2.imshow('img',gray_img)
    cv2.imshow('gray_img', gray_img_)
    cv2.waitKey(30000)
    # cv2.destroyAllWindows()
