import cv2
import numpy as np

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
def canny_edge(img, sigma=0.33):
    v = np.median(img)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(img, lower, upper)
    return edges


# Hough line detection
def hough_line(edges,img, min_line_length=100, max_line_gap=10):
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    print(img.shape)
    # The below for loop runs till r and theta values
    # are in the range of the 2d array
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

        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 80), 2)

    # All the changes made in the input image are finally
    # written on a new image houghlines.jpg
    cv2.imwrite('linesDetected.jpg', img)

    return lines, img

# Separate line into horizontal and vertical
def h_v_lines(lines):
    h_lines, v_lines = [], []
    for rho, theta in lines:
        if theta < np.pi / 4 or theta > np.pi - np.pi / 4:
            v_lines.append([rho, theta])
        else:
            h_lines.append([rho, theta])

    cv2.line(img, v_lines, (0, 0 , 80), 2)
    cv2.imshow('vec', img)


    return h_lines, v_lines


img = read_img('chess_board_3.png')
print(img.shape)
show(img)
resized = resize_img(img)

show(resized)
gray_blur = gray_blur(resized)
show(gray_blur)
edges = canny_edge(gray_blur)
show(edges)
lines, img = hough_line(edges, resized)
show(img)
# h_v_lines(lines)

#
# print(np.shape(img))
# print(np.shape(gray_blur))

