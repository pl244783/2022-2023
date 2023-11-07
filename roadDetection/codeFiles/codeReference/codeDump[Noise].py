import cv2

# Load the input image
img = cv2.imread('codeFiles/roadPictures/homePhoto2.jpg')

# Split the image in half horizontally
height, width, channels = img.shape
half_width = width // 2
left_half = img[:, :half_width]
right_half = img[:, half_width:]

# Calculate the noise level of each half
left_noise = cv2.meanStdDev(cv2.cvtColor(left_half, cv2.COLOR_BGR2GRAY))[1][0][0]
right_noise = cv2.meanStdDev(cv2.cvtColor(right_half, cv2.COLOR_BGR2GRAY))[1][0][0]

# Print the side with less noise
if left_noise < right_noise:
    print("Probable Left Turn")
else:
    print("Probable Right Turn")

img = cv2.resize(img, dsize = (900, 600))
cv2.imshow("Road Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()