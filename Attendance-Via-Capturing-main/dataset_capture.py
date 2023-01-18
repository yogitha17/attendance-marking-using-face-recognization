# Import OpenCV2 for image processing
import cv2
import os
from tkinter import *


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


# Top level window


class App:
    # 'what' and 'why' should probably be fetched in a different way, suitable to the app
    id = 0

    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Hello")
        self.label = Label(self.parent, text="Enter User Id")
        self.label.pack()
        self.entry = Entry(self.parent, width=50)
        self.entry.pack()
        self.button = Button(parent, text='OK', command=self.use_entry)
        self.button.pack()

    def use_entry(self):
        contents = self.entry.get()
        self.id = contents
        # do stuff with contents
        self.parent.destroy()  # if you must


root = Tk()
root.geometry("500x500")
r = App(root)
root.mainloop()
face_id = r.id
# print(r.id)

# Start capturing video
vid_cam = cv2.VideoCapture(0)

# Detect object in video stream using Haarcascade Frontal Face
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialize sample face image
count = 0

assure_path_exists("dataset/")

# Start looping
while (True):

    # Capture video frame
    _, image_frame = vid_cam.read()

    # Convert frame to grayscale
    gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

    # Detect frames of different sizes, list of faces rectangles
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    # Loops for each faces
    for (x, y, w, h) in faces:
        # Crop the image frame into rectangle
        cv2.rectangle(image_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Increment sample face image
        count += 1
        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

        # Display the video frame, with bounded rectangle on the person's face
        cv2.imshow('frame', image_frame)

    # To stop taking video, press 'q' for at least 100ms
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

    # If image taken reach 100, stop taking video
    elif count >= 50:
        print("Successfully Captured")
        break

# Stop video
vid_cam.release()

# Close all started windows
cv2.destroyAllWindows()