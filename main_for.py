import cv2
import numpy as np
import os
import glob

# Defining the dimensions of checkerboard
CHECKERBOARD = (4, 8)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Creating vector to store vectors of 3D points for each checkerboard image
objpoints = []
# Creating vector to store vectors of 2D points for each checkerboard image
imgpoints = [] 

# Defining the world coordinates for 3D points
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

# Extracting path of individual image stored in a given directory
images = glob.glob('./images/*.jpg')

# Create output directory if not exists
if not os.path.exists("output"):
    os.makedirs("output")

# Process each image
for idx, fname in enumerate(images):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(
        gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    
    if ret:
        objpoints.append(objp)
        # Refining pixel coordinates for given 2D points
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)

        # Save the visualized image
        output_image = f'output/visualized_img_{idx}.jpg'
        cv2.imwrite(output_image, img)

        # Perform camera calibration for this image
        h, w = img.shape[:2]
        _, mtx, dist, rvecs, tvecs = cv2.calibrateCamera([objp], [corners2], gray.shape[::-1], None, None)

        # Calculate extrinsic matrix
        rvec, tvec = rvecs[0], tvecs[0]
        R, _ = cv2.Rodrigues(rvec)
        extrinsic_matrix = np.hstack((R, tvec))
        c = np.dot(R.T, tvec) * (-1)
        rotation_angle = np.linalg.norm(c)
        axis = c / rotation_angle

        # Save results to a file for this image
        output_file = f"output/calibration_result_{idx}.txt"
        with open(output_file, "w") as f:
            f.write(f"Results for image: {fname}\n\n")
            f.write("Camera matrix (Intrinsic Parameters):\n")
            f.write(f"{mtx}\n\n")
            f.write("Camera matrix (Extrinsic Parameters):\n")
            f.write(f"{extrinsic_matrix}\n\n")
            f.write("Distortion coefficients:\n")
            f.write(f"{dist}\n\n")
            f.write("Rotation vector (rvec):\n")
            f.write(f"{rvec}\n\n")
            f.write("Translation vector (tvec):\n")
            f.write(f"{tvec}\n\n")
            f.write("Camera coordinate:\n")
            f.write(f"{c}\n\n")
            f.write("Camera axis:\n")
            f.write(f"{axis}\n\n")

        print(f"Processed and saved results for image: {fname}")

cv2.destroyAllWindows()
