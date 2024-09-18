import re

from easyocr import easyocr
from yaml import reader


class LicensePlateReader:
    def __init__(self, validationPattern=""):
        self.reader = easyocr.Reader(['en'], gpu=False)
        self.validationPattern = validationPattern

    def read_license_plate(self, image):
        """
          Read the license plate text from the given cropped image.

          Args:
              license_plate_crop (PIL.Image.Image): Cropped image containing the license plate.

          Returns:
              tuple: Tuple containing the formatted license plate text and its confidence score.
          """

        detections = self.reader.readtext(image)

        for detection in detections:
            bbox, text, score = detection
            text = text.upper().replace(' ', '')
            text = text.replace('O', '0')
            print(text, score)
            if self.license_complies_format(text):
                return text, score
                # return format_license(text), score

        return None, 0

    def license_complies_format(self, text):
        """
        Check if the license plate text complies with the Bulgarian license plate format.

        Args:
            text (str): License plate text.

        Returns:
            bool: True if the license plate complies with the format, False otherwise.
        """
        # Define the regex pattern for allowed Bulgarian license plate format
        # pattern = r"^[ABEKMHOPCTYX]{1,2}[0123456789]{4}[ABEKMHOPCTYX]{2}$"

        # Return True if the text matches the pattern, otherwise return False
        return bool(re.match(self.validationPattern, text))
