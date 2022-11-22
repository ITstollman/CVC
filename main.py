import cv2
import numpy as np

print (cv2.__version__)

def show(img):
    cv2.imshow(str(img), img)
    cv2.waitKey(0)

def gray_blur(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.blur(gray, (5, 5))
    show(gray_blur)
    return gray_blur

# Canny edge detection
def canny_edge(img):

    c_edges = cv2.Canny(img, 90, 200)
    show(c_edges)
    return c_edges


def normlize_img_size(img):

    scale_percent = 60  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    show(resized)
    return resized


def captur_img(img):

    img = cv2.imread(str(img), 1)
    show(img)

    return img



img = captur_img('chess_board_3.png')
resized = normlize_img_size(img)
gray_blur = gray_blur(resized)
canny_edge = canny_edge(gray_blur)


