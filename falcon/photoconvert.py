# encoding:utf-8

import dlib
import numpy as np
import cv2
def createcontour(rect):
    contour=[]
    contour.append((rect.left(),rect.top()))
    contour.append((rect.left(),rect.bottom()))
    contour.append((rect.right(),rect.top()))
    contour.append((rect.right(),rect.bottom()))
    print(contour)
    contour = np.array(contour, np.int32)
    contour = cv2.convexHull(contour)

    return contour
def rect_to_bb(rect): # 获得人脸矩形的坐标信息
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (x, y, w, h)

def resize(image, width=1200):  # 将待检测的image进行resize
    r = width * 1.0 / image.shape[1]
    dim = (width, int(image.shape[0] * r))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized
def get_landmarks(landmarks):
    points=[]
    for n in range(68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        points.append((x, y))
    return points
def detect():
    # image_file = "obama.jpg"
    image_file = "multi2.jpg"
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    detector = dlib.get_frontal_face_detector()
    image = cv2.imread(image_file)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)


    for (i, rect) in enumerate(rects):
        landmarks = predictor(image, rect)
        points = get_landmarks(landmarks)
        points = np.array(points, np.int32)
        convexhull = cv2.convexHull(points)
        contour=createcontour(rect)
        print(contour)
        for m in range(rect.top()+2, rect.bottom()-2):
            for n in range(rect.left()+2, rect.right()-2):
                if(cv2.pointPolygonTest(convexhull, (n,m), False)==1):
                    sum = [0, 0, 0]
                    for x in range(-2,3):

                        for y in range(-2, 3):
                            sum[0]+=list(image[m+x,n+y])[0]
                            sum[1] += list(image[m + x, n + y])[1]
                            sum[2] += list(image[m + x, n + y])[2]
                    sum[0]//=25
                    sum[1]//= 25
                    sum[2] //=25
                    # print(sum)
                    image[m,n]=tuple(sum)
#                 if(cv2.pointPolygonTest(convexhull, (n,m), False)==1):
#                     (b, g, r) = image[m, n]
#                     newb=155-b
#                     newg=183-g
#                     newr=240-r
#                     image[m, n]=(b+0.8*newb,g+0.8*newg,r+0.8*newr)

                    # if m % 5 == 0 and n % 5==0:
                    #     for i in range(5):
                    #         for j in range(5):
                    #             (b, g, r) = image[m, n]
                    #             image[i + m, j + n] = (b, g, r)

                # if m % 5 == 0 and n % 5==0and cv2.pointPolygonTest(convexhull, (m,n), False)==1 :  # 将10 * 10的方格内的像素颜色，设置与[m,n]点颜色相同

                    # for i in range(5):
                    #     for j in range(5):
                    #         (b, g, r) = image[m, n]
                    #         image[i + m, j + n] = (b, g, r)

    cv2.imwrite('obama3.png', image)
    cv2.imshow("Output", image)
    cv2.waitKey(0)

if __name__ == "__main__":

    detect()
