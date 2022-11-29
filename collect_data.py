import math
import random

import cv2
import numpy as np
# from scipy import spatial, cluster
from matplotlib import pyplot as plt


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
def canny_edge(img, sigma = 0.33):
    v = np.median(img)

    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(img, lower, upper)
    c_edges = cv2.Canny(img, 190, 200)
    return edged

# Hough line detection
def hough_line(edges,img, min_line_length=100, max_line_gap=10):
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    h_lines = {}
    v_lines = {}

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
        print("x1", x1, "////////", "y1", y1, "/////", "x2", x2, "//////", "y2", y2)
        exists = False

        if theta < np.pi / 4 or theta > np.pi - np.pi / 4:

            print("v")

            for line in v_lines.values():

                if math.isclose(line[0][0], x1, abs_tol=50) or \
                        math.isclose(line[1][0], x2, abs_tol=50     ):

                    print("exists v",line[0][0], line[1][0])
                    exists = True

            if not exists:
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255 ), 2)
                show(img)
                v_lines[(r,theta)] = [(x1, y1), (x2, y2)]

        else:

            # for line in h_lines:
            print("h")
            for line in h_lines.values():
                if math.isclose(line[0][1], y1, abs_tol=50) or \
                        math.isclose(line[1][1], y2, abs_tol=50):
                    print("exists h", "y1", line[0][1], "y2", line[1][1])
                    exists = True

            if not exists:
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 80), 2)
                show(img)
                # h_lines.append((r, theta))
                h_lines[(r, theta)] = [(x1, y1), (x2, y2)]


    # All the changes made in the input image are finally
    # written on a new image houghlines.jpg
    cv2.imwrite('linesDetected.jpg', img)

    return h_lines, v_lines, img


# Find the intersections of the lines
def line_intersections(h_lines, v_lines, img):
    points = []
    for r_h, t_h in h_lines:
        for r_v, t_v in v_lines:
            a = np.array([[np.cos(t_h), np.sin(t_h)], [np.cos(t_v), np.sin(t_v)]])
            b = np.array([r_h, r_v])
            inter_point = np.linalg.solve(a, b)
            points.append(inter_point)

            cv2.circle(img, (int(inter_point[0]), int(inter_point[1])), radius=5, color=(255, 0, 0  ), thickness=-1)
            show(img)
    return np.array(points)


img = read_img('AFRICAֹ_2.jpeg')
show(img)
resized = resize_img(img)

show(resized)
gray_blur = gray_blur(img)

show(gray_blur)
show(gray_blur)
edges = canny_edge(gray_blur)
show(edges)
h_lines, v_lines, img2 = hough_line(edges, img)
show(img2)

points = line_intersections(h_lines.keys(), v_lines.keys() , img2)

# image = cv2.rectangle(img, (22, 33), (199, 290), (233, 0, 55), 2)
# image = cv2.rectangle(img, (22, 33), (900, 290), (2, 0, 55), 2)
#
# image = cv2.rectangle(img, (222, 33), (199, 290), (9, 0, 211), 2)

show(img)

dictionary = {}

print(points[0])
arrX = []
arrY = []

print("THE POINTS  ")
for point in points:
    arrX.append(point[0])
    arrY.append(point[1])

arrX.sort()
arrX_coor = [arrX[0], arrX[9], int(arrX[18]), int(arrX[27]), int(arrX[36]),
             int(arrX[45]), int(arrX[54]), int(arrX[63]), int(arrX[72])]
arrY.sort()
arrY_coor = [arrY[0], arrY[9], int(arrY[18]), int(arrY[27]), int(arrY[36]),
             int(arrY[45]), int(arrY[54]), int(arrY[63]), int(arrY[72])]


print("arrX_coor", arrX_coor)
print("arrY_coor", arrY_coor)

print(arrX_coor[0], arrY_coor[0])


clean_img = img.copy()
squares = {}
square_num = 1
for i in range(8):
    for j in range(8):
        cv2.rectangle(img, (int(arrX_coor[j]), int(arrY_coor[i])),
                      (int(arrX_coor[j+1]) , int(arrY_coor[i+1])),
                      (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 5)


        cv2.arrowedLine(img, (int(arrX_coor[j]), int(arrY_coor[i])), (int(arrX_coor[j])+20, int(arrY_coor[i])+20 ), (233, 0, 55), 2)

        new_square = [int(arrX_coor[j]), int(arrY_coor[i]),
                      int(arrX_coor[j+1]), int(arrY_coor[i+1])]
        squares[square_num] = new_square
        print("square_num", square_num)

        cropped = clean_img[int(arrY_coor[i]): int(arrY_coor[i+1]), int(arrX_coor[j]): int(arrX_coor[j+1])]
        # cv2.imwrite('./raw_data/alpha_data_image' + str(square) + '.jpeg', cropped)
        cv2.imwrite('cropped' + str(square_num) + '.jpeg', cropped)

        square_num += 1
        show(img)
show(img)
print(squares)
# cv2.arrowedLine(img, (int(arrX_coor[j]), int(arrY_coor[i])), (int(arrX_coor[j]) + 20, int(arrY_coor[i]) + 20),
#                 (233, 0, 55), 2)


cv2.arrowedLine(img, (int(squares[2][0]), int(squares[2][1])), (int(squares[60][0]), int(squares[60][1])),
                (122, 0, 255), 10)
show(img)

print( (int(squares[2][0]), int(squares[2][1])), (int(squares[60][0]), int(squares[60][1])),
                (122, 0, 255), 10)

print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
cv2.arrowedLine(img, (int(squares[18][0]), int(squares[18][1])), (int(squares[29][0]), int(squares[29][1])),
                (0, 0, 20), 14)
show(img)

cv2.arrowedLine(img, (int(squares[45][0]), int(squares[45][1])), (int(squares[10][0]), int(squares[10][1])),
                (0, 277, 255), 2)
show(img)


# cv2.arrowedLine(img, int(squares[2][0]), int(squares[2][1]), int(squares[2][0]), int(squares[2][1]),
#                 (233, 0, 55), 2)
# cv2.arrowedLine(img, int(squares[2][0]), int(squares[2][1]), int(squares[2][0]), int(squares[2][1]),
#                 (233, 0, 55), 2)
# cv2.arrowedLine(img, int(squares[2][0]), int(squares[2][1]), int(squares[2][0]), int(squares[2][1]),
#                 (233, 0, 55), 2)
# cv2.warpPerspective(image, matrix, (width, height))
# https://theailearner.com/tag/cv2-getperspectivetransform/

#ways to get the dataset bigger
#rotation
# image = cv2.rotate(src, cv2.ROTATE_90_COUNTERCLOCKWISE)

#crop the image a little bit diffrently, for example - higher, righter and so.
