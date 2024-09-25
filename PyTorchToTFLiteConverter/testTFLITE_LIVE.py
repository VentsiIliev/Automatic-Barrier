import cv2
import tkinter
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import tensorflow as tf

# Here Input is 256*256*3
path = "hand_landmark_3d.tflite"
interpreter = tf.lite.Interpreter(model_path=path)  # ouput is 21*2
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Start capturing video from the webcam
cap = cv2.VideoCapture(1)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Resize and preprocess the frame
    frame = cv2.resize(frame, (256, 256), interpolation=cv2.INTER_AREA)
    frame_copy = frame.copy()  # Create a copy of the frame for drawing
    frame = np.expand_dims(frame, 0)
    frame = np.array(frame, dtype=np.float32)

    # Set the tensor and invoke the interpreter
    interpreter.set_tensor(input_details[0]['index'], frame)
    interpreter.invoke()

    # Get the output data
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Process the output data
    x = [output_data[0][i * 2] for i in range(21)]
    y = [output_data[0][i * 2 + 1] for i in range(21)]
    x = np.asarray(x, dtype=np.float32)
    y = np.asarray(y, dtype=np.float32)

    # Check if a hand is detected
    if np.any(x) and np.any(y):
        # Draw the landmarks on the frame
        for i in range(21):
            cv2.circle(frame_copy, (int(x[i]), int(y[i])), 5, (0, 255, 0), -1)

        # Draw lines between adjacent landmarks
        adjacent_landmarks = [(0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
                              (0, 5), (5, 6), (6, 7), (7, 8),  # Index finger
                              (0, 9), (9, 10), (10, 11), (11, 12),  # Middle finger
                              (0, 13), (13, 14), (14, 15), (15, 16),  # Ring finger
                              (0, 17), (17, 18), (18, 19), (19, 20)]  # Little finger

        for start, end in adjacent_landmarks:
            cv2.line(frame_copy, (int(x[start]), int(y[start])), (int(x[end]), int(y[end])), (0, 255, 0), 2)

    # Display the frame with the drawn landmarks and skeleton
    cv2.imshow('Hand Landmarks', frame_copy)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()