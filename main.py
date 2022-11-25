from collections import defaultdict

import cv2
import numpy as np
from scipy import spatial, cluster


def show(img):
    cv2.imshow(str(img), img)
    cv2.waitKey(0)


def resize_img(img):

    imgScale = 1000 / img.shape[1]
    X, Y = img.shape[1] * imgScale, img.shape[0] * imgScale
    resized = cv2.resize(img, (int(X), int(Y)))
    return resized

def gray_blur(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.blur(gray, (5, 5))
    return gray_blur

# Read image and do lite image processing
def read_img(file):
    img = cv2.imread(str(file), 1)
    return img


# Canny edge detection
def canny_edge(img):

    c_edges = cv2.Canny(img, 90, 200)
    return c_edges


# Hough line detection
def hough_line(edges,img, min_line_length=100, max_line_gap=10):
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    h_lines = []
    v_lines = []

    for r_theta in lines:

        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr
        # Stores the value of cos(theta) in a
        a = np.cos(theta)

        # Stores the value of sin(theta) in b
        b = np.sin(theta)

        # x0 stores the value rcos(theta)
        x0 = a * r

        # y0 stores the value rsin(theta)
        y0 = b * r

        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
        x1 = int(x0 + 1000 * (-b))

        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
        y1 = int(y0 + 1000 * (a))

        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
        x2 = int(x0 - 1000 * (-b))

        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
        y2 = int(y0 - 1000 * (a))

        # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
        # (0,0,255) denotes the colour of the line to be
        # drawn. In this case, it is red.

        if theta < np.pi / 4 or theta > np.pi - np.pi / 4:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 80), 2)
            show(img)
            h_lines.append((r, theta))

        else:
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255 ), 2)
            show(img)
            v_lines.append((r, theta))

    # All the changes made in the input image are finally
    # written on a new image houghlines.jpg
    cv2.imwrite('linesDetected.jpg', img)

    return h_lines, v_lines, img




def polar2cartesian(rho: float, theta_rad: float, rotate90: bool = False):

    x = np.cos(theta_rad) * rho
    y = np.sin(theta_rad) * rho
    m = np.nan
    if not np.isclose(x, 0.0):
        m = y / x

    b = 0.0
    if m is not np.nan:
        b = y - m * x

    return m, b, x, y


img = read_img('chess_board_3.png')
show(img)
resized = resize_img(img)

show(resized)
gray_blur = gray_blur(resized)
show(gray_blur)
edges = canny_edge(gray_blur)
show(edges)
h_lines, v_lines , img = hough_line(edges, resized)
show(img)

points = line_intersections(h_lines, v_lines , img)

image = cv2.rectangle(img, (22,33), (199,290), (233,0,55), 2)
image = cv2.rectangle(img, (22,33), (900 ,290), (2,0,55), 2)

image = cv2.rectangle(img, (222,33), (199,290), (9,0,211), 2)

show(img)

dictionary = {}
for point in points:
    print(point)
    dictionary[str(int(point[0]))].append(point)

print(dictionary)






