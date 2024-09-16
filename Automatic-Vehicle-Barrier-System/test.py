#find the largest white rectangle in image
import cv2


def find_largest_(image):
    """
    Find the largest white rectangle in the image.

    Args:
        image (np.array): Image.

    Returns:
        tuple: Coordinates of the largest white rectangle.
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to get a binary image
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow("binary",binary)
    cv2.waitKey(0)
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    #draw contours
    # cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Get the bounding rectangle of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)

    return x, y, x + w, y + h

image = cv2.imread('assets/results/license_plate_crop.jpg')
x1, y1, x2, y2 = find_largest_(image)
#draw the rectangle on the image
cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
cv2.imshow('image', image)
cv2.waitKey(0)
cv2.imwrite('assets/results/license_plate_crop_largest.jpg', image)