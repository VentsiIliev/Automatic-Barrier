import cv2


class LicensePlateRecognizer:

    def __init__(self, license_plate_detector, license_plate_reader, confidence_threshold=0.5):
        self.license_plate_detector = license_plate_detector
        self.license_plate_reader = license_plate_reader
        self.confidence_threshold = confidence_threshold

    def recognize(self, image):
        # Recognize license plate
        results = self.license_plate_detector.detect(image)[0]
        if results is None or len(results) == 0:
            return None

        filtered_results = []
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score < self.confidence_threshold:
                continue
            filtered_results.append(result)

        if len(filtered_results) == 0:
            return None

        for license_plate in filtered_results:
            x1, y1, x2, y2, score, class_id = license_plate
            license_plate_region = image[int(y1):int(y2), int(x1):int(x2)]
            result = self.license_plate_reader.read(license_plate_region)
            license_plate_text, text_score = result
            # if text_score < self.confidence_threshold:
            #     continue

            # draw bbox for license plate
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        return license_plate_text
