import pynput
from time import sleep

letters_dictionary = {}

working = False


def check_letter(key):
    global letters_dictionary
    key = str(key)
    if letters_dictionary.get(key) is None:
        letters_dictionary[key] = 1
    else:
        letters_dictionary[key] += 1

    letters_dictionary['total'] += 1


def on_press(key):
    if key == 'Key.esc':
        global working
        working = False

    check_letter(key)



def on_release(key):
    if not working:
        return False


def on_move(x, y):
    return


def on_click(x, y, button, pressed):
    check_letter(button)


def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))

mouse = None
keyboard = None

def start():
    global letters_dictionary, working, keyboard, mouse
    letters_dictionary = {'total': 0, 'Button.left': 0, 'Button.right': 0}
    working = True

    mouse = pynput.mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll)
    mouse.start()


    keyboard = pynput.keyboard.Listener(
                on_press=on_press,
                on_release=on_release)
    keyboard.start()


def stop():
    global working, keyboard, mouse
    working = False
    keyboard.stop()
    mouse.stop()
    return  {'total': letters_dictionary['total'],
             'right':letters_dictionary['Button.left'],
             'left':letters_dictionary['Button.right']}


if __name__ == '__main__':
    print('START')
    start()
    sleep(5)
    print(stop())
    print('END')
