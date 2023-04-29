import cv2
import numpy as np
from keras.models import model_from_json
#import serial


emotion_dict = {0: "Worst Service", 1: "Disgusted", 2: "Bad Service", 3: "Good Service", 4: "Average", 5: "Not Good", 6: "Very Good Service"}

# load json and create model
json_file = open('./model/emotion_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)

# load weights into new model
emotion_model.load_weights("./model/emotion_model.h5")
print("Loaded model from disk")

# pass here your video path

cap = cv2.VideoCapture(0)

#open serial port to communicate with Arduino
#ser = serial.Serial('/dev/tty.usbmodem11301', 9600)


while True:
    # Find haar cascade to draw bounding box around face
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))
    if not ret:
        break
    face_detector = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces available on camera
    num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=2, minNeighbors=5)

    # take each face available on the camera and Preprocess it
    for (x, y, w, h) in num_faces:
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
        roi_gray_frame = gray_frame[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

        # predict the emotions
        emotion_prediction = emotion_model.predict(cropped_img)
        maxindex = int(np.argmax(emotion_prediction))
        emotion = emotion_dict[maxindex]
        cv2.putText(frame, emotion_dict[maxindex], (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # control Arduino light based on the detected emotion
        #if emotion == "Angry":
        #    ser.write('A'.encode())
        #elif emotion == "Happy":
        #    ser.write('H'.encode())
#
        #elif emotion == "Neutral":
        #    ser.write('N'.encode())

    cv2.imshow('Service Rating', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
