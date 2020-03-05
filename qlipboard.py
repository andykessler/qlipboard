import pyperclip
import keyboard
import time
from collections import deque
from enum import Enum

class ClipMode(Enum):
    QUEUE = 1
    STACK = 2
    NORMAL = 3

# Script specific hotkeys
queue_hotkey = 'alt+1' # FIFO list
stack_hotkey = 'alt+2' # LIFO list
normal_hotkey = 'alt+3' # Single
purge_hotkey = 'alt+v' # Clear clipboard memory. TODO consider purge single, purgle all

# Standard copy paste hotkeys
# TODO check cross platform compatability
copy_hotkey = 'ctrl+c'
paste_hotkey = 'ctrl+v'
cut_hotkey = 'ctrl+x'

# first time after coming from normal mode
maiden_flag = True

def queue_command():
    global clip_mode
    print('queue mode')
    clip_mode = ClipMode.QUEUE
    memory.clear()

def stack_command():
    global clip_mode
    print('stack mode')
    clip_mode = ClipMode.STACK
    memory.clear()

def normal_command():
    global clip_mode, maiden_flag
    print('normal mode')
    maiden_flag = True
    clip_mode = ClipMode.NORMAL
    memory.clear()

def purge_command():
    print('purge')
    memory.clear()

# COPY COMMANDS

# TODO Consider logging all copies in case of accidental memory loss
def copy_command():
    global maiden_flag
    print('copy')
    # if maiden_flag:
    #    maiden_flag = False
    #    return
    if(clip_mode is ClipMode.NORMAL): 
        return
    # FIXME Try to find a way without sleep.
    # Need sleep to give host system time to update the clipboard
    # Without it will currently copy the clip before.
    time.sleep(0.1)
    clip = pyperclip.paste()
    print(clip)
    copy = get_copy_function()
    copy(clip)
    if len(memory) != 0:
        next_clip = memory.pop()
        pyperclip.copy(next_clip)
        memory.append(next_clip)
        
def get_copy_function():
    copy_switch = {
        ClipMode.QUEUE: copy_to_queue,
        ClipMode.STACK: copy_to_stack,
        ClipMode.NORMAL: copy_normal
    }
    return copy_switch[clip_mode]

def copy_to_queue(clip):
    print('copy to queue')
    memory.appendleft(clip)

def copy_to_stack(clip):
    print('copy to stack')
    memory.append(clip)

def copy_normal(clip):
    print('copy normal')

# PASTE COMMANDS

def paste_command():
    print('paste')
    paste = get_paste_function()
    paste()

def get_paste_function():
    paste_switch = {
        ClipMode.QUEUE: paste_from_queue,
        ClipMode.STACK: paste_from_stack,
        ClipMode.NORMAL: paste_normal
    }
    return paste_switch[clip_mode]

def paste_from_queue():
    print('paste from queue')
    clip = memory.pop() if len(memory) != 0 else ''
    print(clip)
    pyperclip.copy(clip)

def paste_from_stack():
    print('paste from stack')
    clip = memory.pop() if len(memory) != 0 else ''
    print(clip)
    pyperclip.copy(clip)

def paste_normal():
    print('paste normal')

# TODO Consider setting maxlen (system memory limitation)
memory = deque()
clip_mode = ClipMode.QUEUE

keyboard.add_hotkey(copy_hotkey, copy_command)
keyboard.add_hotkey(paste_hotkey, paste_command)
keyboard.add_hotkey(queue_hotkey, queue_command)
keyboard.add_hotkey(stack_hotkey, stack_command)
keyboard.add_hotkey(normal_hotkey, normal_command)
keyboard.add_hotkey(purge_hotkey, purge_command)
keyboard.wait()
