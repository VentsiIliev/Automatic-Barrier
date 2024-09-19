import string

import cv2
import easyocr
from PIL import Image
from pytesseract import pytesseract

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    # 'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    # '6': 'G',
                    '5': 'S'}
# def license_complies_format(text):
#     """
#     Check if the license plate text complies with the required format.
#
#     Args:
#         text (str): License plate text.
#
#     Returns:
#         bool: True if the license plate complies with the format, False otherwise.
#     """
#     if len(text) != 7:
#         return False
#
#     if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
#             (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
#             (text[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
#             (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
#             (text[4] in string.ascii_uppercase or text[4] in dict_int_to_char.keys()) and \
#             (text[5] in string.ascii_uppercase or text[5] in dict_int_to_char.keys()) and \
#             (text[6] in string.ascii_uppercase or text[6] in dict_int_to_char.keys()):
#         return True
#     else:
#         return False

import re


# def license_complies_format(text):
#     """
#     Check if the license plate text complies with the Bulgarian license plate format.
#
#     Args:
#         text (str): License plate text.
#
#     Returns:
#         bool: True if the license plate complies with the format, False otherwise.
#     """
#     # Define the regex pattern for allowed Bulgarian license plate format
#     pattern = r"^[ABEKMHOPCTYX]{1,2}[0123456789]{4}[ABEKMHOPCTYX]{2}$"
#
#     # Return True if the text matches the pattern, otherwise return False
#     return bool(re.match(pattern, text))


def format_license(text):
    """
    Format the license plate text by converting characters using the mapping dictionaries.

    Args:
        text (str): License plate text.

    Returns:
        str: Formatted license plate text.
    """

    # if len(text) != 7:
    #     return text

    license_plate_ = ''
    mapping = {0: dict_int_to_char, 1: dict_int_to_char, 4: dict_int_to_char, 5: dict_int_to_char, 6: dict_int_to_char,
               2: dict_char_to_int, 3: dict_char_to_int}
    for j in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        if text[j] in mapping[j].keys():
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]

    return license_plate_


# def read_license_plate(license_plate_crop):
#     """
#     Read the license plate text from the given cropped image.
#
#     Args:
#         license_plate_crop (PIL.Image.Image): Cropped image containing the license plate.
#
#     Returns:
#         tuple: Tuple containing the formatted license plate text and its confidence score.
#     """
#
#     detections = reader.readtext(license_plate_crop)
#
#     for detection in detections:
#         bbox, text, score = detection
#         text = text.upper().replace(' ', '')
#         text = text.replace('O', '0')
#         print(text, score)
#         if license_complies_format(text):
#             return text, score
#             # return format_license(text), score
#
#     return None, 0


def get_car(license_plate, vehicle_track_ids):
    """
    Retrieve the vehicle coordinates and ID based on the license plate coordinates.

    Args:
        license_plate (tuple): Tuple containing the coordinates of the license plate (x1, y1, x2, y2, score, class_id).
        vehicle_track_ids (list): List of vehicle track IDs and their corresponding coordinates.

    Returns:
        tuple: Tuple containing the vehicle coordinates (x1, y1, x2, y2) and ID.
    """
    x1, y1, x2, y2, score, class_id = license_plate

    foundIt = False
    for j in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[j]

        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_indx = j
            foundIt = True
            break

    if foundIt:
        return vehicle_track_ids[car_indx]

    return -1, -1, -1, -1, -1

# def find_largest_(image):
#     """
#     Find the largest white rectangle in the image.
#
#     Args:
#         image (np.array): Image.
#
#     Returns:
#         tuple: Coordinates of the largest white rectangle.
#     """
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # Apply a binary threshold to get a binary image
#     _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
#     # cv2.imshow("binary",binary)
#     # cv2.waitKey(0)
#     # Find contours
#     contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     # draw contours
#     # cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
#     # Find the largest contour
#     largest_contour = max(contours, key=cv2.contourArea)
#     cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 2)
#     cv2.imshow("largest_contour", image)
#     cv2.waitKey(0)
#     # Get the bounding rectangle of the largest contour
#     x, y, w, h = cv2.boundingRect(largest_contour)
#
#     return x, y, x + w, y + h
