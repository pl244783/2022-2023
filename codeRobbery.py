# #TESTING DOES NOT WORK
#opencv documentation is useless lmao

# # import cv2
# # import numpy as np

# # inputImage = cv2.imread("bent.jpg")
# # inputImageGray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
# # edges = cv2.Canny(inputImageGray,150,200,apertureSize = 3)
# # minLineLength = 0
# # maxLineGap = 0
# # lines = cv2.HoughLinesP(edges,cv2.HOUGH_PROBABILISTIC, np.pi/180, 30, minLineLength,maxLineGap)

# # for x in range(0, len(lines)):
# #     for x1,y1,x2,y2 in lines[x]:
# #         #cv2.line(inputImage,(x1,y1),(x2,y2),(0,128,0),2, cv2.LINE_AA)
# #         pts = np.array([[x1, y1 ], [x2 , y2]], np.int32)
# #         cv2.polylines(inputImage, [pts], True, (0,255,0), 2)

# # img = cv2.resize(inputImage, dsize=(500,500))
# # cv2.imshow('edge', img)
# # cv2.waitKey(0)

# #GRAHHHHHH

# # rework this to work with working.py, do it only with uh curves, it'd be funny
# # importread('bent2.jpg')

# # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#2.HoughLinesP(edgthing but uh different ig
# # parallel_curves j][0]
# #         if abs(curve1[1] - curve2[1]) < 5 and abs(curve1[3] - curve2[3]) < 5:
# #             parallel_curves.append((curve1, curve2))


# # #questionable, but we'll see
# # for curve in parallel_curves:
# #     cv2.lineurve[0][0]+curve[1][0])//2, (curve[0][1]+curve[1][1])//2), ((curve[0][2]+curve[1][2])//2, (curve[0][3]+curve[1][3])//2), (0, 0, 255), 2)

# # realImg = cv2.resize(img, dsize=(500,500))
# # cv2.imshow('Result', realImg)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()  

# #probably will work with id
# #i lit did the same thing  

# import cv2
# import numpy as np

# img = cv2.imread('bent2.jpg')

# # Convert thecircl] - circle2[0]) < 10 and np.abs(circle1[1] - circle2[1]) < 10 and np.abs(circle1[2] - circle2[2]) < 10:
#             parallel_circles.append((circle1, circle2))
#             print(circle1, circle2)

# for circle in parallel_circles:
#     cv2.circle(img, (ci[1][0], circle[1][1]), circle[1][2], (0, 255, 0), 2)

# img =y(0)
# cv2.destroyAllws()
# # #exact same thing but for circle detec?

# #actually i'll rewrite this alter

# import cv2
# import numpy as np
# AHH TGRASH GRAHAHAHAHHAHHHHH

# # Load tayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # Apply Gaussian blur to reduce noise
# gray_blu
# # Apply Hough C
# curves = cv2.HoughLines(edges, rho=1, theta=np.pi/180, threshold=100)

# # Draw detage
# for curve i00*(a)))
#     cv2.line(img, pt1, pt2, (0, 0, 255), 2)

# # Display the result
# img = cv2.resize(img, dsize = (500,500))
# cv2.imshow('Result', img)
# cv2.waitKey(0)
# # cv2.destroyAllWindows()

# import cv2
# import numpy as np
  
# img = cv2.imread('bent2.jpg')

# # Convert the photo to grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # Apply Canny edge detection
# edges = cv2.Canny(gray, 50, 150, apertureSize=3)
  
# # Grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
# # Find Canny edges
# edged = cv2.Canny(gray, 30, 200)

# # Finding Contours
# # Use a copy of the image e.g. edged.copy()
# # since findContours alters the image
# contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  
# print("Number of Contours found = " + str(len(contours)))
  
# # Draw all contours
# # -1 signifies drawing all contours
# for x in contours:
#     print(x)
# cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

# image = cv2.resize(image, dsize=(600,600)) 
# cv2.imshow('Contours', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#https://www.geeksforgeeks.org/find-and-draw-contours-using-opencv-python/
# --> geeksforgeeks idk to this 

# edges = cv2.Canny(gray, 20, 300, apertureSize=3)


# contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# for cnt in contours:
#     epsilon = 0.01*cv2.arcLength(cnt,True)
#     approx = cv2.approxPolyDP(cnt,epsilon,True)
    
#     # If the ox) > 4:
#     #     coin
#     # Draw the contour on the image
#     cv2.drawContours(img,[cnt],0,(0,0,255),2)

#contour detection could work
#nice it works
#time to lobotomize it for what i need

# import numpy as np
# import cv2 as cv
# im = cv.imread('bent2.jpg')
# imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
# ret, thresh = cv.threshold(imgray, 127, 255, 0)
# im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

#honkers
import numpy as np
import cv2

img = cv2.imread('bent2.jpg')

# Convert the photo to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

#maybe put this in an if statement
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#i love inefficienices!!!!!
for x in contours:
    print(x)
cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

img = cv2.resize(img, dsize=(500,500))
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

