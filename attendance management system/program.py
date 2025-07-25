# Import required libraries
import face_recognition  # For face detection and recognition
import cv2  # For capturing video and displaying frames
import numpy as np  # For numerical operations
import csv  # For writing attendance data to CSV
import os  # For file and folder operations
import time  # For adding delay
from datetime import date, datetime  # For getting current date and time

# Start capturing video from the default webcam (0)
video_capture = cv2.VideoCapture(0)

# Load Vishal's image from file
vishal_image = face_recognition.load_image_file(r"D:\B-Tech AIML\Third Year\mini project\attendance management system\photos\vishal.jpg")
vishal_encoding = face_recognition.face_encodings(vishal_image)[0]  # Create facial encoding for Vishal

# Load Yash's image from file
yash_image = face_recognition.load_image_file(r"D:\B-Tech AIML\Third Year\mini project\attendance management system\photos\yash.png")
yash_encoding = face_recognition.face_encodings(yash_image)[0]  # Create facial encoding for Yash

# List of all known face encodings
known_face_encodings = [vishal_encoding, yash_encoding]  # All stored face encodings
# Corresponding names for the known faces
known_face_names = ["vishal", "yash"]  # Names should be in the same order as encodings

# Copy the names for attendance tracking
students = known_face_names.copy()  # List of students yet to be marked present

# Initialize face detection variables
face_locations = []  # To store locations of faces in the current frame
face_encodings = []  # To store encodings of faces in the current frame
face_names = []  # To store names of detected faces
s = True  # Toggle variable (optional use)

# Get current date in YYYY-MM-DD format
current_date = date.today().strftime("%Y-%m-%d")  # Used to name the attendance CSV file

# Set directory path where attendance CSV will be stored
output_dir = r"D:\B-Tech AIML\Third Year\mini project\attendance management system\attendance_logs"
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

# Full path for today's attendance file
file_path = os.path.join(output_dir, f"{current_date}.csv")

# Open the CSV file for writing attendance
with open(file_path, 'w+', newline='') as f:  # 'w+' creates the file if not exists
    lnwriter = csv.writer(f)  # Create a CSV writer object
    lnwriter.writerow(["Name", "Time"])  # Write the header row in CSV
    f.flush()  # Force immediate write to disk

    while True:  # Infinite loop to process video frames
        ret, frame = video_capture.read()  # Capture one frame from webcam
        if not ret:
            print("Failed to capture frame from camera. Exiting...")  # If camera fails
            break

        # Resize frame to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR (OpenCV format) to RGB (face_recognition format)
        rgb_small_frame = small_frame[:, :, ::-1]

        if s:  # Only process every frame if s is True
            # Find all faces and their encodings in the current frame
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []  # Clear previous names

            for face_encoding in face_encodings:  # Loop through each face detected
                # Compare face with known encodings
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"  # Default name if no match
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)  # Distance measure
                best_match_index = np.argmin(face_distances)  # Index of closest match

                if matches[best_match_index]:  # If a known face matched
                    name = known_face_names[best_match_index]  # Get the corresponding name

                face_names.append(name)  # Add the name to the list for display

                # If the recognized face is in student list (not marked yet)
                if name in students:
                    students.remove(name)  # Remove from students (to avoid duplicate marking)
                    current_time = datetime.now().strftime("%H:%M:%S")  # Get current time
                    lnwriter.writerow([name, current_time])  # Write name and time to CSV
                    f.flush()  # Ensure data is written immediately
                    print(f"{name} marked present at {current_time}")  # Debug print
                    time.sleep(1)  # Wait 1 second before processing next frame

        # Display rectangles and names on video frame
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations to match original frame size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            # Draw label background rectangle
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            # Write the name text over the rectangle
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Show the video frame with the boxes and names
        cv2.imshow("Attendance System", frame)

        # Break loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # Exit the loop

# Release webcam and close all OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
