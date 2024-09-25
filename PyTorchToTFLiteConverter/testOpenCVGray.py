import cv2
import numpy as np
import time

# Open Camera object (Uncomment if you want to use the camera)
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def nothing(x):
    pass

# Create a window for the trackbars
cv2.namedWindow('Trackbars')

# Create trackbars for threshold and kernel size
cv2.createTrackbar('Threshold', 'Trackbars', 100, 255, nothing)
cv2.createTrackbar('Kernel Size', 'Trackbars', 5, 20, nothing)  # Kernel size range from 1 to 20

# Load a sample image
# frame = cv2.imread("hand3.jpg")
while True:
    # Measure execution time
    start_time = time.time()

    # Capture frames from the camera (Uncomment if you want to use the camera)
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur the image
    blur = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    # Get the current threshold value from the trackbar
    threshold_value = cv2.getTrackbarPos('Threshold', 'Trackbars')

    # Get the current kernel size from the trackbar (must be odd)
    kernel_size = cv2.getTrackbarPos('Kernel Size', 'Trackbars') * 2 + 1
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # Use a simple binary threshold to create a mask
    _, thresh = cv2.threshold(blur, threshold_value, 255, cv2.THRESH_BINARY)

    # Perform morphological transformations to filter out noise
    dilation = cv2.dilate(thresh, kernel, iterations=1)
    erosion = cv2.erode(dilation, kernel, iterations=1)

    # Find contours of the filtered frame
    contours, hierarchy = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours and len(contours) > 0:
        # Find Max contour area (Assume that the object is in the frame)
        max_area = 0
        ci = -1
        for i, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                ci = i

        if ci != -1:
            cnts = contours[ci]

            # Draw the largest contour and its bounding rectangle
            x, y, w, h = cv2.boundingRect(cnts)
            cv2.rectangle(gray_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.drawContours(gray_frame, [cnts], -1, (255, 255, 255), 2)

            # Calculate the center of the contour
            moments = cv2.moments(cnts)
            if moments['m00'] != 0:
                cx = int(moments['m10'] / moments['m00'])
                cy = int(moments['m01'] / moments['m00'])
                cv2.circle(gray_frame, (cx, cy), 7, (100, 0, 255), 2)
                cv2.putText(gray_frame, 'Center', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Show the processed frame
    cv2.imshow('Processed Frame', gray_frame)

    # Show execution time
    execution_time = time.time() - start_time
    print(f"Execution Time: {execution_time:.2f} seconds")

    # Exit on pressing 'Esc'
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Clean up
# cap.release()  # Uncomment if using camera
cv2.destroyAllWindows()
