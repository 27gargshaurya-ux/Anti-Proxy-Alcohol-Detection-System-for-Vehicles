import cv2
import serial
import time
import face_recognition
import numpy as np

# Set up the serial connection
arduino_port = 'COM11'  # Update this to your actual Arduino port
baud_rate = 9600

try:
    arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2)  # Give some time for the connection to initialize
    print(f"Connected to Arduino on {arduino_port}")
except Exception as e:
    print(f"Error: {e}")
    arduino = None

def is_object_detected():
    global arduino
    if arduino is not None:
        if arduino.in_waiting > 0:  # Check if there's data available
            try:
                message = arduino.readline().decode('utf-8').strip()  # Read the line from Arduino
                print(f"Arduino Message: '{message}'")  # Debug: Print the received message
                # Check specifically for "NO_ALCOHOL" to start face matching
                return message == "NO_ALCOHOL"
            except Exception as e:
                print(f"Error reading from Arduino: {e}")
    return False

def capture_image(camera):
    ret, frame = camera.read()
    if ret:
        print("Image successfully captured.")
        return frame
    else:
        print("Failed to capture image from camera.")
        return None

def recognize_face(captured_image):
    rgb_image = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    print(f"Face locations: {face_locations}")  # Debug: Print detected face locations

    if len(face_encodings) == 0:
        print("No face detected.")
        return None
    return face_encodings[0], face_locations

def compare_faces(known_face_encoding, current_face_encoding, threshold=0.6):
    distance = np.linalg.norm(known_face_encoding - current_face_encoding)  # Calculate Euclidean distance
    print(f"Distance: {distance}")  # Debug: Print the distance
    return distance < threshold  # Compare with the threshold

def draw_text_and_rectangle(frame, text, box_color, face_locations):
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, box_color, 2, cv2.LINE_AA)

def main():
    global arduino
    captured_face_encoding = None
    capture_camera_index = 0
    match_camera_index = 1

    # Keep the cameras open
    capture_camera = cv2.VideoCapture(capture_camera_index)
    match_camera = cv2.VideoCapture(match_camera_index)

    if not capture_camera.isOpened():
        print("Error: Capture camera could not be opened.")
        return

    if not match_camera.isOpened():
        print("Error: Match camera could not be opened.")
        return

    while True:
        # Continuously check for object detection status
        if is_object_detected():
            print("Alcohol not detected! Starting the matching process...")
            max_attempts = 3
            attempt = 0
            image = None

            while attempt < max_attempts:
                image = capture_image(capture_camera)
                if image is not None:
                    break
                attempt += 1
                time.sleep(1)  # Wait a bit before the next attempt

            if image is not None:
                cv2.imshow("Captured Image", image)  # Show captured image
                time.sleep(1)  # Show for 1 second
                print("Clicking photo...")
                time.sleep(0.5)

                captured_face_info = recognize_face(image)
                if captured_face_info is not None:
                    captured_face_encoding, face_locations = captured_face_info
                    print("Face captured! Starting matching process...")
                    arduino.write(b'MATCHED\n')

                    draw_text_and_rectangle(image, "Face Captured!", (0, 255, 0), face_locations)
                    cv2.imshow("Face Recognition", image)
                    cv2.waitKey(2000)

                    while True:
                        print("Waiting for new image for matching...")
                        time.sleep(10)  # Wait for a while before capturing again
                        current_image = capture_image(match_camera)
                        if current_image is not None:
                            current_face_info = recognize_face(current_image)

                            if current_face_info is None:
                                print("No face detected in live image.")
                                arduino.write(b'RELAY_OFF\n')
                                draw_text_and_rectangle(current_image, "No Face Detected!", (0, 0, 255), [])
                                cv2.imshow("Face Recognition", current_image)
                                cv2.waitKey(2000)
                                break

                            current_face_encoding, current_face_locations = current_face_info
                            if compare_faces(captured_face_encoding, current_face_encoding, threshold=0.5):
                                print("Faces match! Activating relay.")
                                arduino.write(b'RELAY_ON\n')  # Turn on the relay on match
                                draw_text_and_rectangle(current_image, "Match Found!", (0, 255, 0), current_face_locations)
                            else:
                                print("No match found. Turning relay off.")
                                arduino.write(b'RELAY_OFF\n')  # Turn off the relay on no match
                                draw_text_and_rectangle(current_image, "No Match!", (0, 0, 255), current_face_locations)

                            cv2.imshow("Face Recognition", current_image)
                            cv2.waitKey(2000)
                else:
                    print("No face detected. Waiting for new alcohol test.")
                    arduino.write(b'RELAY_OFF\n')
            else:
                print("Failed to capture image after multiple attempts.")
        else:
            print("Alcohol detected or no blow detected. Waiting...")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if arduino is not None:
        arduino.close()
    capture_camera.release()
    match_camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
