from ultralytics import YOLO
import cv2

cap = cv2.VideoCapture(1)
modelPath = "license_plate_detector.pt"
model_pretrained = YOLO(modelPath, task="detect", verbose=False,mode="preict")
model_pretrained.info(verbose=True)
print(model_pretrained.task)

while True:
    ret, frame = cap.read()

    if ret:
        # detect & track objects
        results = model_pretrained.track(frame, show=True, persist=True)

        # print(results.boxes.id)
        print(results)
        # print("results -> ",results)

        # plot results
        # composed = results[0].plot()

        # save video
