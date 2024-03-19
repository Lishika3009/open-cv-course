import cv2

# Load the pre-trained face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the pre-trained face recognition model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("model.yml")

# Function to recognize faces
def recognize_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        
        # Perform face recognition
        id_, confidence = recognizer.predict(roi_gray)
        
        if confidence >= 45 and confidence <= 85:
            print("Confidence:", confidence)
            print("ID:", id_)
            
            # Draw a rectangle around the face
            color = (255, 0, 0)  # BGR
            stroke = 2
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, stroke)
            
            # Put text with recognized ID
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = "Unknown"
            if id_ == 1:
                name = "John Doe"
            elif id_ == 2:
                name = "Jane Smith"
            cv2.putText(frame, name, (x, y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
    return frame

# Initialize video capture from webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = recognize_faces(frame)
    
    # Display the frame
    cv2.imshow('Face Recognition', frame)
    
    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
