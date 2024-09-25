import cv2
import numpy as np
import time

# Open Camera object
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def nothing(x):
    pass

# Creating a window for HSV track bars
cv2.namedWindow('HSV_TrackBar')

# Creating trackbars for HSV values
cv2.createTrackbar('Hue Min', 'HSV_TrackBar', 0, 179, nothing)
cv2.createTrackbar('Hue Max', 'HSV_TrackBar', 15, 179, nothing)
cv2.createTrackbar('Saturation Min', 'HSV_TrackBar', 50, 255, nothing)
cv2.createTrackbar('Saturation Max', 'HSV_TrackBar', 255, 255, nothing)
cv2.createTrackbar('Value Min', 'HSV_TrackBar', 50, 255, nothing)
cv2.createTrackbar('Value Max', 'HSV_TrackBar', 255, 255, nothing)

# Creating trackbars for blur and morphological operations
cv2.createTrackbar('Blur Kernel Size', 'HSV_TrackBar', 3, 20, nothing)  # Kernel size for blur
cv2.createTrackbar('Dilation Kernel Size', 'HSV_TrackBar', 11, 30, nothing)  # Kernel size for dilation
cv2.createTrackbar('Erosion Kernel Size', 'HSV_TrackBar', 5, 30, nothing)  # Kernel size for erosion

while True:
    # Measure execution time
    start_time = time.time()

    # Capture frames from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale for processing
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Convert to BGR
    frame_bgr = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2BGR)

    # Get the current values from trackbars
    blur_kernel_size = cv2.getTrackbarPos('Blur Kernel Size', 'HSV_TrackBar') * 2 + 1
    dilation_kernel_size = cv2.getTrackbarPos('Dilation Kernel Size', 'HSV_TrackBar')
    erosion_kernel_size = cv2.getTrackbarPos('Erosion Kernel Size', 'HSV_TrackBar')

    # Blur the image
    blur = cv2.blur(frame_bgr, (blur_kernel_size, blur_kernel_size))

    # Convert to HSV color space
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Get HSV thresholds from trackbars
    h_min = cv2.getTrackbarPos('Hue Min', 'HSV_TrackBar')
    h_max = cv2.getTrackbarPos('Hue Max', 'HSV_TrackBar')
    s_min = cv2.getTrackbarPos('Saturation Min', 'HSV_TrackBar')
    s_max = cv2.getTrackbarPos('Saturation Max', 'HSV_TrackBar')
    v_min = cv2.getTrackbarPos('Value Min', 'HSV_TrackBar')
    v_max = cv2.getTrackbarPos('Value Max', 'HSV_TrackBar')

    # Create a binary mask based on the current HSV values
    mask = cv2.inRange(hsv, np.array([h_min, s_min, v_min]), np.array([h_max, s_max, v_max]))

    # Kernel matrices for morphological transformation
    kernel_square = np.ones((erosion_kernel_size, erosion_kernel_size), np.uint8)
    kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilation_kernel_size, dilation_kernel_size))

    # Perform morphological transformations to filter out the background noise
    dilation = cv2.dilate(mask, kernel_ellipse, iterations=1)
    erosion = cv2.erode(dilation, kernel_square, iterations=1)
    filtered = cv2.medianBlur(erosion, 5)

    # Find contours of the filtered frame
    contours, hierarchy = cv2.findContours(filtered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours is not None and len(contours) > 0:
        # Find Max contour area (Assume that hand is in the frame)
        max_area = 0
        ci = -1
        for i in range(len(contours)):
            area = cv2.contourArea(contours[i])
            if area > max_area:
                max_area = area
                ci = i

        if ci != -1:
            cnts = contours[ci]
            # Find convex hull
            hull = cv2.convexHull(cnts)
            # Draw contours
            cv2.drawContours(frame, [hull], -1, (255, 255, 255), 2)

            # Find moments of the largest contour
            moments = cv2.moments(cnts)
            if moments['m00'] != 0:
                cx = int(moments['m10'] / moments['m00'])  # cx = M10/M00
                cy = int(moments['m01'] / moments['m00'])  # cy = M01/M00
                centerMass = (cx, cy)
                cv2.circle(frame, centerMass, 7, (100, 0, 255), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'Center', tuple(centerMass), font, 1, (255, 255, 255), 2)

    # Display results
    cv2.imshow('Blur', blur)
    cv2.imshow('Dilation', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('HSV', hsv)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
