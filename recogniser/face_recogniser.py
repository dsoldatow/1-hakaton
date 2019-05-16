import face_recognition
import cv2
import time
from base64 import b64encode
import os


def make_photo():
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    rgb_frame = frame[:, :, ::-1]
    cap.release()
    cv2.imwrite("photo.png", frame)
    with open("photo.png", 'rb') as fin:
        img_data = fin.read()
        encoded_img = b64encode(img_data).decode()
    os.remove("photo.png")
    return encoded_img

def is_user_here():
    cap = cv2.VideoCapture(0)
    beg_time = time.time()
    while time.time() - beg_time < 5:
        _, frame = cap.read()
        rgb_frame = frame[:, :, ::-1]
        # img = face_recognition.load_image_file(frame)
        face_location = face_recognition.face_locations(rgb_frame)
        cv2.imwrite("photo.png", frame)
        with open("photo.png", 'rb') as fin:
            img_data = fin.read()
            encoded_img = b64encode(img_data).decode()
        os.remove("photo.png")
        if len(face_location) != 0:
            cap.release()
            return {'is_here': True, 'photo': ''}
    cap.release()
    return {'is_here': False, 'photo': encoded_img}


if __name__ == '__main__':
    print(is_user_here())