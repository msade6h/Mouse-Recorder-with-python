import pyautogui
import keyboard
import time
from pynput import mouse
import tkinter as tk
from tkinter import messagebox


record_duration = 10
mouse_events = []


def on_move(x, y):
    mouse_events.append(('move', x, y, time.time()))

def on_click(x, y, button, pressed):
    event_type = 'click_down' if pressed else 'click_up'
    mouse_events.append((event_type, x, y, time.time()))

def start_recording():
    global mouse_events
    mouse_events = []

    print("Recording mouse movement. Move the mouse around and click...")
    listener = mouse.Listener(on_move=on_move, on_click=on_click)
    listener.start()

    start_time = time.time()
    while time.time() - start_time <= record_duration:
        if keyboard.is_pressed('q'):
            print("Recording stopped by user.")
            break
        time.sleep(0.01)

    listener.stop()
    print("Mouse movement and clicks recorded.")
    messagebox.showinfo("Info", "Mouse movement and clicks recorded.")

def start_replaying():
    print("Replaying mouse movement and clicks...")
    pyautogui.FAILSAFE = False  
    if not mouse_events:
        messagebox.showwarning("Warning", "No mouse events recorded.")
        return

    start_time = mouse_events[0][3]
    while True:
        if keyboard.is_pressed('q'):
            print("Program stopped by user.")
            break
        for event in mouse_events:
            event_type, x, y, event_time = event
            delay = event_time - start_time
            start_time = event_time
            if event_type == 'move':
                pyautogui.moveTo(x, y, duration=0)
            elif event_type == 'click_down':
                pyautogui.mouseDown(x, y)
            elif event_type == 'click_up':
                pyautogui.mouseUp(x, y)
            if keyboard.is_pressed('q'):
                print("Program stopped by user.")
                return

def stop_program():
    root.destroy()


root = tk.Tk()
root.title("Mouse Recorder")

record_button = tk.Button(root, text="Start Recording", command=start_recording)
record_button.pack(pady=10)

replay_button = tk.Button(root, text="Start Replaying", command=start_replaying)
replay_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_program)
stop_button.pack(pady=10)

info_label = tk.Label(root, text="Press 'q' to stop recording/replaying.         sade6h@gmail.com | instagram : msadeghkarimi ")
info_label.pack(pady=10)

root.mainloop()
