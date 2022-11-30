import cv2
import numpy as np
from matplotlib import pyplot as plt

from collect_data import read_img

img = read_img('chess_board_3.png')

print("aaaaaaaaaaaaaaaaaaaaaa")
# Specify input and output coordinates that is used
# to calculate the transformation matrix
input_pts = np.float32([[8,128],[380,125],[189,12],[45,11]])
output_pts = np.float32([[10,10],[10,300],[200,300],[200,10]])

# Compute the perspective transform M
M = cv2.getPerspectiveTransform(input_pts,output_pts)

# Apply the perspective transformation to the image
out = cv2.warpPerspective(img,M,(img.shape[1], img.shape[0]),flags=cv2.INTER_LINEAR)

# Display the transformed image
cv2.imshow(str(img), out)
cv2.waitKey(0)


# cv2.warpPerspective(image, matrix, (width, height))
# https://theailearner.com/tag/cv2-getperspectivetransform/

# https://www.youtube.com/watch?v=tFNJGim3FXw&t=1841s YOLOV5



