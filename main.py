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

    W = 1000
    height, width, depth = img.shape
    imgScale = W / width
    newX, newY = img.shape[1] * imgScale, img.shape[0] * imgScale
    resized = cv2.resize(img, (int(newX), int(newY)))
    show(resized)
    return resized


# Hough line detection
def hough_line(edges, min_line_length=100, max_line_gap=10):
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    print(lines)
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
    show(img)

    return lines



def captur_img(img):

    img = cv2.imread(str(img), 1)
    show(img)

    return img



img = captur_img('chess_board_2.png')
resized = normlize_img_size(img)
gray_blur = gray_blur(resized)
canny_edge = canny_edge(gray_blur)
hough_line = hough_line(canny_edge)
