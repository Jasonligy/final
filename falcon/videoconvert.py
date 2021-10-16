# encoding:utf-8
import time
import dlib
import numpy as np
import cv2
from PIL import Image
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
def detect(image):
    # image_file = "obama.jpg"

    predictor = dlib.shape_predictor("D:\cisc\GAN\code\shape_predictor_68_face_landmarks.dat")
    detector = dlib.get_frontal_face_detector()
    # image = cv2.imread(image_file)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)


    for (i, rect) in enumerate(rects):
        landmarks = predictor(image, rect)
        points = get_landmarks(landmarks)
        points = np.array(points, np.int32)
        convexhull = cv2.convexHull(points)
        contour=createcontour(rect)
        print(contour)
        for m in range(rect.top(), rect.bottom()):
            for n in range(rect.left(), rect.right()):
                if(cv2.pointPolygonTest(convexhull, (n,m), False)==1):
                    if m % 5 == 0 and n % 5==0:
                        for i in range(5):
                            for j in range(5):
                                (b, g, r) = image[m, n]
                                image[i + m, j + n] = (b, g, r)

                # if m % 5 == 0 and n % 5==0and cv2.pointPolygonTest(convexhull, (m,n), False)==1 :  # 将10 * 10的方格内的像素颜色，设置与[m,n]点颜色相同

                    # for i in range(5):
                    #     for j in range(5):
                    #         (b, g, r) = image[m, n]
                    #         image[i + m, j + n] = (b, g, r)
        # (x, y, w, h) = rect_to_bb(rect)
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.putText(image, "Face： {}".format(i + 1), (x - 10, y - 10), cv2.FONT_ )                                                                                       HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # cv2.drawContours(image, [contour], -1, (0, 0, 255), 3)
        cv2.drawContours(image, [convexhull], -1, (0, 0, 255), 1)
    return image

if __name__ == "__main__":
    video_path      = "videoshort.mp4"
    video_save_path = "video2.mp4"
    video_fps = 25.0
    capture = cv2.VideoCapture(video_path)
    if video_save_path != "":
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        out = cv2.VideoWriter(video_save_path, fourcc, video_fps, size)

    fps = 0.0
    i=0
    while (True):
        i+=1
        t1 = time.time()
        # 读取某一帧
        ref, frame = capture.read()
        # # 格式转变，BGRtoRGB
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # # 转变成Image
        # frame = Image.fromarray(np.uint8(frame))
        # 进行检测
        frame =detect(frame)
        # RGBtoBGR满足opencv显示格式
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # fps = (fps + (1. / (time.time() - t1))) / 2
        # print("fps= %.2f" % (fps))
        # frame = cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        #
        # # cv2.imshow("video",frame)
        c = cv2.waitKey(1) & 0xff
        if video_save_path != "":
            out.write(frame)
        print(i)
        if c == 27:
            capture.release()
            break
    capture.release()
    out.release()
    cv2.destroyAllWindows()

