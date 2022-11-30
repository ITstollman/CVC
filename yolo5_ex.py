import matplotlib
import torch
from jedi.api.refactoring import inline
from matplotlib import pyplot as plt
import numpy as np
import cv2
import uuid
import os


model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

result =  model('eli.png')
# print(result)
print(result.xyxy)

labels = ['WB', 'WR']
