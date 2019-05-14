import face_recognition
import cv2
import time
from base64 import b64encode


def is_user_here():
    cap = cv2.VideoCapture(0)
    beg_time = time.time()
    while time.time() - beg_time < 5:
        _, frame = cap.read()
        rgb_frame = frame[:, :, ::-1]
        # img = face_recognition.load_image_file(frame)
        face_location = face_recognition.face_locations(rgb_frame)
        if len(face_location) != 0:
            cap.release()
            return {'is_here': True, 'photo': b''}
    cap.release()
    return {'is_here': False, 'photo': b64encode(frame)}


if __name__ == '__main__':
    print(is_user_here())