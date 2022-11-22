import cv2


print (cv2.__version__)



def captur_img(img):

    img = cv2.imread(str(img), 1)
    cv2.imshow('current img', img)
    cv2.waitKey(0)


captur_img('chess_board_1.png')