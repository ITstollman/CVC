import math
import random

import cv2
import np as np
import numpy as np
# from scipy import spatial, cluster
from matplotlib import pyplot as plt


def creat_squars(img):
    squares = {}
    square_num = 1
    for i in range(8):
        for j in range(8):
            print("THE NEW SQR IS")
            print("i", i, "j", j)

            print("[int(rows[i+1][j][0]),    int(rows[i+1][j][1])]", [int(rows[i + 1][j][0]), int(rows[i + 1][j][1])])
            print("[int(rows[i+][j][0]),    int(rows[i][j][1])]", [int(rows[i][j][0]), int(rows[i][j][1])])
            print("[int(rows[i][j+1][0]),    int(rows[i][j+1][1])]", [int(rows[i][j + 1][0]), int(rows[i][j + 1][1])])
            print("[int(rows[i+1][j+1][0]),    int(rows[i+1][j+1][1])]",
                  [int(rows[i + 1][j + 1][0]), int(rows[i + 1][j + 1][1])])

            new_square = [[int(rows[i + 1][j][0]), int(rows[i + 1][j][1])],
                          [int(rows[i][j][0]), int(rows[i][j][1])],
                          [int(rows[i][j + 1][0]), int(rows[i][j + 1][1])],
                          [int(rows[i + 1][j + 1][0]), int(rows[i + 1][j + 1][1])]]

            cv2.circle(img, (int(rows[i + 1][j][0]), int(rows[i + 1][j][1])), radius=5, color=(22, 0, 0), thickness=-1)
            print("first")
            show(img)
            cv2.circle(img, (int(rows[i][j][0]), int(rows[i][j][1])), radius=5, color=(22, 100, 0), thickness=-1)
            print("second")
            show(img)

            cv2.circle(img, (int(rows[i][j + 1][0]), int(rows[i][j + 1][1])), radius=5, color=(0, 0, 122), thickness=-1)
            print("third")
            show(img)

            cv2.circle(img, (int(rows[i + 1][j + 1][0]), int(rows[i + 1][j + 1][1])), radius=5, color=(2, 22, 222),
                       thickness=-1)
            print("FORTH")
            show(img)

            print("i", i, "j", j)
            print("new_square", new_square)

            rectangle = np.array([new_square], np.int32)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            rectangleImage = cv2.polylines(img, [rectangle], True, color, thickness=7)

            show(rectangleImage)

            perspective_sqr = perspective(img,
                                          [int(rows[i + 1][j][0]), int(rows[i + 1][j][1])],
                                          [int(rows[i][j][0]), int(rows[i][j][1])],
                                          [int(rows[i][j + 1][0]), int(rows[i][j + 1][1])],
                                          [int(rows[i + 1][j + 1][0]), int(rows[i + 1][j + 1][1])])

            show(perspective_sqr)

            squares[square_num] = new_square
            print("square_num", square_num)

            cv2.imwrite('perspective_sqr' + str(square_num) + '.jpeg', perspective_sqr)

            square_num += 1
            show(img)
    show(img)
    print(squares)

    cv2.arrowedLine(img, (int(squares[2][0][0]), int(squares[2][0][1])),
                    (int(squares[60][0][0]), int(squares[60][0][1])),
                    (122, 0, 255), 10)
    return squares

def perspective(img, pt_A, pt_B, pt_C, pt_D):

    width_AD = np.sqrt(((pt_A[0] - pt_D[0]) ** 2) + ((pt_A[1] - pt_D[1]) ** 2))
    width_BC = np.sqrt(((pt_B[0] - pt_C[0]) ** 2) + ((pt_B[1] - pt_C[1]) ** 2))
    maxWidth = max(int(width_AD), int(width_BC))

    height_AB = np.sqrt(((pt_A[0] - pt_B[0]) ** 2) + ((pt_A[1] - pt_B[1]) ** 2))
    height_CD = np.sqrt(((pt_C[0] - pt_D[0]) ** 2) + ((pt_C[1] - pt_D[1]) ** 2))
    maxHeight = max(int(height_AB), int(height_CD))

    input_pts = np.float32([pt_A, pt_B, pt_C, pt_D])
    output_pts = np.float32([[0, 0],
                             [0, maxHeight - 1],
                             [maxWidth - 1, maxHeight - 1],
                             [maxWidth - 1, 0]])

    # Compute the perspective transform M
    M = cv2.getPerspectiveTransform(input_pts, output_pts)

    out = cv2.warpPerspective(img, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)

    return out

def sort_points(points):
    sorter = lambda x: (x[1], x[0])
    sorted_l = sorted(points, key=sorter)
    print(sorted_l)

    one = sorted_l[0:9]
    two = sorted_l[9:18]
    three = sorted_l[18:27]
    four = sorted_l[27:36]
    five = sorted_l[36:45]
    six = sorted_l[45:54]
    seven = sorted_l[54:63]
    eight = sorted_l[63:72]
    nine = sorted_l[72:81]
    print("eight", eight)
    rows = [one, two, three, four, five, six, seven, eight, nine]
    return rows


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


img = read_img('chess_board_3.png')
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

show(img)

rows = sort_points(points)

squars = creat_squars(img)

show(img)



# cv2.warpPerspective(image, matrix, (width, height))
# https://theailearner.com/tag/cv2-getperspectivetransform/

#ways to get the dataset bigger
#rotation
# image = cv2.rotate(src, cv2.ROTATE_90_COUNTERCLOCKWISE)

#crop the image a little bit diffrently, for example - higher, righter and so.

