import cv2

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Define the file name for the captured image
image_name = 'webcam_capture.jpg'

# Capture the image
ret, frame = cap.read()
if not ret:
    raise IOError("Cannot read frame from webcam")

# Save the image
cv2.imwrite(image_name, frame)

# Release the webcam
cap.release()

# Display the captured image
cv2.imshow('Captured Image', frame)
cv2.waitKey(0)

# Close the window
cv2.destroyAllWindows()