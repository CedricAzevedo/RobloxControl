from pywinauto import Application as app
import pydirectinput as pdi # pip install pydirectinput-rgx
from time import sleep
import datetime


# Building the functions
def detectingWindow(maximize_window=True):
    try:
        program = app().connect(title='Roblox', found_index=0)
        roblox_window = program.window(title='Roblox')

        global roblox_window_info
        roblox_window_info = roblox_window.client_rect()
       
        if maximize_window:
            roblox_window.set_focus()
            roblox_window.maximize()

        while roblox_window.exists(timeout=10):
            return True
    except:
        return None


def walk(direction='w', walk_duration=1.0, _pause=False):
    pdi.keyDown(direction, _pause=_pause)
    sleep(walk_duration)
    pdi.keyUp(direction,  _pause=_pause)

# sprint_toggle it means enable and disable, like a switch or a button.
# two_keys it means press twice time the same button to enable sprint.
def sprintwalk(sprint_key='ctrl', sprint_toggle=True, two_keys=False, direction=('w', 'a', 's', 'd'), walk_duration=1.0, _interval=0.00002):
    if sprint_toggle:
        pdi.press(sprint_key)
        try:
            walk(direction[0], walk_duration)
        except:
            raise ValueError('Invalid Direction')
        pdi.press(sprint_key)
    elif two_keys == True:
        pdi.press(sprint_key, interval=_interval, _pause=False)
        walk(sprint_key, walk_duration,  _pause=False)
    else:
        pdi.keyDown(sprint_key)
        sleep(0.3)
        try:
            walk(direction[0], walk_duration)
        except:
            raise ValueError("Invalid Direction")
        pdi.keyUp(sprint_key)


def selectItem(item_position:list, delay_between=0.25):
    for item in item_position:
        pdi.write(f'{item}', interval=delay_between)


def useItem(button=('left', 'middle', 'right'), quantity=1, x=None, y=None, delay_in_use=0.0):
    pdi.click(button=button[0],clicks=quantity, x=x, y=y, interval=delay_in_use)


def pressKey(keys:list, delay_to_start=0.0, delay_in_use=0.25):
    for i in keys:
        sleep(delay_to_start)
        pdi.press(i, interval=delay_in_use)

# Sometimes can not work properly
def openInventory():
    x = roblox_window_info.right - 30
    y = roblox_window_info.top + 40

    sleep(1)
    pdi.moveTo(x=x, y=y, disable_mouse_acceleration=False)
    sleep(0.1)
    pdi.click(clicks=2)
    sleep(0.3)
    pdi.moveTo(x=x-10, y=y+170, disable_mouse_acceleration=False)
    sleep(0.3)
    pdi.moveTo(x=x-11, y=y+170, disable_mouse_acceleration=False)
    sleep(0.1)
    pdi.click(clicks=1)


def controlInventory(_from:list, action=['Put','Take']):
    # middle of hotbar: 840 987
    hotbar_spacing = 65
    x, y = roblox_window_info.mid_point()
    y = roblox_window_info.bottom

    def toPut(*_from):
        x = 546;y = 987 # Item 1

        for items in _from:
            for item in items:
                if item > 1:
                    sleep(0.5)
                    pdi.moveTo(x=x + (hotbar_spacing * item), y=y)
                    sleep(0.5)
                    pdi.mouseDown()
                    pdi.moveTo(x=x, y=y + (hotbar_spacing * item))
                    sleep(0.5)
                    pdi.mouseUp()
                else:
                    sleep(0.5)
                    pdi.mouseDown()
                    sleep(0.5)
                    pdi.moveTo(x=x, y=y + (hotbar_spacing * item))
                    sleep(0.5)
                    pdi.mouseUp()


    def toTake(*_from):
        x = 546;y = 700 # Item 1

        for items in _from:
            for item in items:
                print(item)
                if item > 1:
                    sleep(0.5)
                    pdi.mouseDown()
                    sleep(0.5)
                    target_x = x+(hotbar_spacing * (item - 1)) # Calcular a posição correta baseada no índice do item
                    pdi.moveTo(x=target_x, y=y + 294)
                    sleep(0.5)
                    pdi.mouseUp()
                    sleep(0.5)
                    pdi.moveTo(x=x, y=y)  # Retornar à posição original
                    sleep(0.5)
                else:
                    sleep(0.5)
                    pdi.mouseDown()
                    sleep(0.5)
                    pdi.moveTo(x=x, y=y+294)
                    sleep(0.5)
                    pdi.mouseUp()
                    sleep(0.5)
                    pdi.moveTo(x=x, y=y) # Back to original position
                    sleep(0.5)


    if action[0] == True:
        pdi.moveTo(x=546, y=987)
        toPut(_from)
    else:
        pdi.moveTo(x=546, y=700)
        toTake(_from)


def closeInventory():
    pdi.press('escape')


def jump(key=' ', quantity=1):
    if pdi.isValidKey(key):
        pdi.keyDown(key)
        sleep(quantity/2)
        pdi.keyUp(key)

#def cameraMove()

# Need to add lambda for each command inside of commands
def loop(time:float, commands:list):
  end_time = datetime.datetime.now() + datetime.timedelta(seconds=time)
  while datetime.datetime.now() < end_time:
    for command in commands:
      command()


# Test the functions

