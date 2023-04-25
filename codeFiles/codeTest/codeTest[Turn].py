import cv2
import numpy as np

window_name = 'Image'
image = cv2.imread('codeFiles/roadPictures/homePhoto2.jpg')

# Polygon corner points coordinates
pts = np.array([[200, 300], [200, 245], [200, 170], [150, 125], [75, 100]], np.int32)
 
isClosed = False
color = (0, 255, 0)
thickness = 8
 
image = cv2.polylines(image, [pts], isClosed, color, thickness)
 
# Displaying the image
image = cv2.resize(image, dsize=(900, 600))
cv2.imshow('image', image)
cv2.waitKey(10000)
cv2.destroyAllWindows()