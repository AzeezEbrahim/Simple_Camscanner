import cv2, numpy as np
from PIL import Image

def preProcessing(img):
    """ A function used to pre-process images to make it suitable to work with.
        
        Parameters: img (matrix): matrix image
        Returns: imgThres(matrix): Processed matrix image
    """
    # 1 - Convert to grey level
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # 2 - Denoise image 
    imgBlur = cv2.fastNlMeansDenoising(imgGray, h=10)  
    # imgBlur2 = cv2.GaussianBlur(imgGray,(5,5),1)  # another way of denoising

    # 3 - Removing unnecessary details such as writing
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    morph = cv2.morphologyEx(imgBlur, cv2.MORPH_CLOSE,kernel,iterations=5)

    # 4 - Edge detection using canny
    imgCanny = cv2.Canny(morph,75,200)
    # imgCanny2 = cv2.Canny(imgBlur,75,200) # without morph

    # 5- Extra preprocessing Dilation and Erosion( Mostly we don't needs them )
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=1)
    imgThres = cv2.erode(imgDial,kernel,iterations=1)
    
    # write output images for testing
    # cv2.imwrite("output/imgGray.jpg", imgGray)
    # cv2.imwrite("output/imgBlur.jpg", imgBlur)
    # cv2.imwrite("output/morph.jpg", morph)
    # cv2.imwrite("output/imgCanny.jpg", imgCanny)
    # cv2.imwrite("output/imgDial.jpg", imgDial)
    # cv2.imwrite("output/imgThres.jpg", imgThres)

    return imgThres

def cornerDetector(img ):
    """ A function used to highlight all the contours in the image and 
        find the corners of the biggest one.
        
        Parameters: img (matrix): matrix image
        Returns: corners(Array): return the biggest contours corner pixel points
    """
    # biggest contours corner points saved in an array
    corners = np.array([])
    # initalize the max area
    maxArea = 0
    # calling method find contours to find all contours in the image
    contours,_ = cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # loop through each contour in the image
    for cnt in contours:
        # svae its area size
        area = cv2.contourArea(cnt)
        # if area smaller than 6k ignore it 
        if area > 6000:
            # if we want to see all contours uncomment this
            # cv2.drawContours(imgCopy, cnt, -1, (0, 0, 255), 2)
            # Calculate the contour curves length we need it for approximation points (the bigger the accurate)
            epsilon  = 0.05*cv2.arcLength(cnt,True)
            # An approximation of the edges points ( corner points)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            # if this contour has bigger area and it has 4 points edges ( meaning it is a square such as paper)
            if area > maxArea and len(approx) == 4:
                corners = approx
                maxArea = area
    return corners

def sortCorners(corners):
    """ A function used to reorder the corners point to
        match the exact order required for the wrapper function.
        
        Parameters: corners (array): corners of the paper
        Returns: sortedCorners(array): returns sortedd array of corners pixel points
    """
    # Just reshaping before manuplations 
    corners = corners.reshape((4,2))
    # create empty new corners
    sortedCorners = np.zeros((4,1,2),np.int32)
    # sum each corner width + height => smallest is at the top left[0,0]
    # biggest will be bottom right [width, height]
    # we want to make the corner like this order [[0, 0], [width, 0], [0, height], [width, height]]
    add = corners.sum(1)
    # smallest
    sortedCorners[0] = corners[np.argmin(add)]
    # biggest
    sortedCorners[3] = corners[np.argmax(add)]
    # The difference between width - height for the remaining points:
    #  if the result (height - width) is negative(minimum) => will be at [width, 0]
    #  if the result (height - width) is positive(maximum) => will be at [0, height]
    diff = np.diff(corners,axis=1)
    sortedCorners[1]= corners[np.argmin(diff)]
    sortedCorners[2] = corners[np.argmax(diff)]
    
    return sortedCorners

def warper(img, corners, width, height):
    """ A function used to transform the document into fully flat in x and y directions.
        
        Parameter: img (matrix): matrix image
        Parameter: corners (array): corners of the paper

        Returns: corners(array): fully flat in x and y image
    """
    # Calling sort corner to satisfy wrapper function 
    corners = sortCorners(corners)
    # set the points
    points1 = np.float32(corners)
    points2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    # Wrapper transform computer transform matrix
    matrix = cv2.getPerspectiveTransform(points1, points2)
    # result
    result = cv2.warpPerspective(img, matrix, (width, height))

    # if we want to better cut the noise edges
    # imgCropped = result[10:result.shape[0]-10, 10:result.shape[1]-10]
    # imgCropped = cv2.resize(imgCropped,(width,height))

    return result

# Output images size
width = 960
height = 1280
# Reading input images
img = cv2.imread("emm.jpg")

# resizing image (for better quality)
img = cv2.resize(img, (width,height))

# Take a copy image for drawing edges
imgCopy = img.copy()

# Process image before detecting
processedImg = preProcessing(img)

# Get corners points
corners = cornerDetector(processedImg)

# Draw a circle in the contour edges ( corner of the paper)
cv2.drawContours(imgCopy, corners, -1, (0, 0, 255), 40)

# Wrap the image into flat x, y directions
imgWarped = warper(img, corners, width, height)

# Convert to grey level
imgGray = cv2.cvtColor(imgWarped,cv2.COLOR_BGR2GRAY)

# Denoise image 
imgBlur = cv2.fastNlMeansDenoising(imgGray, h=15)  
# imgBlur2 = cv2.GaussianBlur(imgGray,(5,5),1)  # another way of denoising

# Apply adaptive Threshold
adaptiveThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


# concatenate images Horizontally and resizing
Hori = np.concatenate((imgCopy, img), axis=1)
resHori = cv2.resize(Hori,(1400,600))

# Show images
cv2.imshow("imgWarped", resHori)
cv2.imshow("adaptiveThreshold", adaptiveThreshold)

# time to show image : 7s
cv2.waitKey(7000)

# image to PDF
# image_1 = Image.open(r'output\scanimage3\10.jpg')
# im_1 = image_1.convert('RGB')
# im_1.save(r'output\scanimage3\final_result.pdf')

# outputs images
# cv2.imwrite("output/imgWarped.jpg", imgWarped)
# cv2.imwrite("output/adaptiveThreshold.jpg", adaptiveThreshold)
# cv2.imwrite("output/imgCopy.jpg", imgCopy)

