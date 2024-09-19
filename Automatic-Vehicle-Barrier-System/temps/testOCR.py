import os

import cv2

from utils import util

# Get a list of all files in the directory
image_files = os.listdir('../assets/images/plates')


# Process each image file
def process(img):
    pass
    # img = cv2.resize(img, (640, 480))
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


license_plates = []
for image_file in image_files:
    # Check if the file is an image
    if image_file.endswith('.jpg') or image_file.endswith('.png'):
        # Construct the full image path
        image_path = os.path.join('../assets/images/plates', image_file)

        # Load the image
        img = cv2.imread(image_path)
        results = util.read_license_plate(img)
        results = [image_file, results[0], results[1]]
        license_plates.append(results)

print(license_plates)
