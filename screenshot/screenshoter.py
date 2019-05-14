import pyautogui
from base64 import b64encode
from io import BytesIO


def get_screen_shot():
    image = pyautogui.screenshot()
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    encoded_image = b64encode(img_byte_arr)
    return encoded_image


if __name__ == "__main__":
    print(get_screen_shot())
