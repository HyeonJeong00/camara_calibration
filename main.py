
import cv2
import numpy as np
import os
import glob
 
# Defining the dimensions of checkerboard
# CHECKERBOARD = (6,9)
CHECKERBOARD = (4,8)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
# Creating vector to store vectors of 3D points for each checkerboard image
objpoints = []
# Creating vector to store vectors of 2D points for each checkerboard image
imgpoints = [] 
 
 
# Defining the world coordinates for 3D points
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None
 
# Extracting path of individual image stored in a given directory
images = glob.glob('./images/*.jpg')
# images = glob.glob('img1.jpg')
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    # If desired number of corners are found in the image then ret = true
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
     
    """
    If desired number of corner are detected,
    we refine the pixel coordinates and display 
    them on the images of checker board
    """
    # 여기는 그냥 chessboard 좌표를 찍는 코드....
    if ret == True:
        objpoints.append(objp)
        # refining pixel coordinates for given 2d points.
        corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
         
        imgpoints.append(corners2)
 
        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
     
    # cv2.imshow('img',img)
    cv2.imwrite(f'output/img.jpg', img)

    cv2.waitKey(0)
 
cv2.destroyAllWindows()
 
h,w = img.shape[:2]
 
"""
Performing camera calibration by 
passing the value of known 3D points (objpoints)
and corresponding pixel coordinates of the 
detected corners (imgpoints)
"""
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
# 직접 calibrateCamera 식을 구현하면 됨. 

exmtx = []
for rvec, tvec in zip(rvecs, tvecs):
    R, _ = cv2.Rodrigues(rvec)
    extrinsic_matrix = np.hstack((R, tvec))
    exmtx.append(extrinsic_matrix)
exmtx = np.array(exmtx)
c = np.dot(R.T, tvec) * (-1)    # 행렬 내적
rotation_angle = (c[0]**2 + c[1]**2 + c[2]**2)**(1/2)
axis = []
axis.append(c[0]/rotation_angle)
axis.append(c[1]/rotation_angle)
axis.append(c[2]/rotation_angle)

output_file = "calibration_result.txt"
with open(output_file, "w") as f:
    f.write("Camera matrix (Intrinsic Parameters):\n")
    f.write(f"{mtx}\n\n")
    f.write("Camera matrix (Extrinsic Parameters):\n")
    f.write(f"{exmtx}\n\n")
    f.write("Distortion coefficients:\n")
    f.write(f"{dist}\n\n")
    f.write("Rotation vectors (rvecs):\n")
    f.write(f"{rvecs}\n\n")
    f.write("Translation vectors (tvecs):\n")
    f.write(f"{tvecs}\n\n")
    f.write("camera coordinate:\n")
    f.write(f"{c}\n\n")
    f.write("camera axis:\n")
    f.write(f"{axis}\n\n")
