import cv2
from datetime import datetime

# Start camera (lower resolution for speed)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)   # width
cap.set(4, 480)   # height

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Function to mark attendance
def markAttendance(name):
    with open('attendance.csv', 'r+') as f:
        data = f.readlines()
        nameList = []

        for line in data:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            now = datetime.now()
            date = now.strftime('%d-%m-%Y')
            time = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{date},{time}')

while True:
    name = input("\nEnter student name (or type 'exit'): ").upper()

    if name == "EXIT":
        break

    print("Press 's' to mark attendance")

    marked = False
    frame_count = 0

    while True:
        success, img = cap.read()
        if not success:
            continue

        # Reduce load: process every 3rd frame
        frame_count += 1
        if frame_count % 3 != 0:
            cv2.imshow('Face Attendance', img)
            if cv2.waitKey(30) == ord('q'):
                break
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Faster detection settings
        faces = face_cascade.detectMultiScale(gray, 1.7, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)

            cv2.putText(img, name, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (255,255,255), 2)

        cv2.imshow('Face Attendance System', img)

        key = cv2.waitKey(30)

        if key == ord('s') and not marked:
            markAttendance(name)
            print(f"{name} attendance marked")
            marked = True
            break

        if key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()

cap.release()
cv2.destroyAllWindows()
