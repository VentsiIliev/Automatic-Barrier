


class LicensePlate:
    def __init__(self, reg_text, plate_score,license_plate_text_score, plate_region_image):
        self.reg_text = reg_text
        self.score = plate_score
        self.license_plate_text_score = license_plate_text_score
        self.plate_region = plate_region_image

    def __str__(self):
        # Return a list of values, not a string
        return [self.reg_text, f"{self.score:.1f}", f"{self.license_plate_text_score:.1f}"]

    def __eq__(self, other):
        return self.reg_text == other.reg_text

    def __hash__(self):
        return hash(self.plate)
