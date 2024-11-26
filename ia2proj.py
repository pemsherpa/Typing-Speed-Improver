import tkinter as tk
from tkinter import ttk
import time
import threading
import random

root = tk.Tk()
root.title("Typing Speed")
root.geometry("800x600")
root.resizable(False, False)
texts = open("/Users/pemasherpa/Desktop/RVU/1st year/python/Tkinter/start.py", "r").read().split("\n")

frame = tk.Frame(root)

sample_label = tk.Label(frame, text=random.choice(texts), font=("Arial", 18), wraplength=600)
sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

input_entry = tk.Entry(frame, width=40, font=("Helvetica", 24))
input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
input_entry.config(highlightbackground="light blue", highlightcolor="light blue", highlightthickness=2)

speed_label = tk.Label(frame, text="Speed: \n0.00 cps\n0.00 cpm\n0.00 wps\n0.00 wpm", font=("Helvetica", 18))
speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=3, column=0, columnspan=2, padx=5, pady=10)


def start(event):
    global running
    global counter
    if not running:
        if event.keycode not in [16, 17, 18]:
            running = True
            t = threading.Thread(target=time_thread)
            t.start()
    if not sample_label.cget('text').startswith(input_entry.get()):
        input_entry.config(fg="red")
    else:
        input_entry.config(fg="black")
    if input_entry.get() == sample_label.cget('text'):
        running = False
        input_entry.config(fg="green")


def time_thread():
    global running
    global counter
    while running:
        time.sleep(0.1)
        counter += 0.1
        cps = len(input_entry.get()) / counter
        cpm = cps * 60
        wps = len(input_entry.get().split(" ")) / counter
        wpm = wps * 60
        speed_label.config(text=f"Speed: \n{cps:.2f} cps\n{cpm:.2f} cpm\n{wps:.2f} wps\n{wpm:.2f} wpm")
        update_progress()


def update_progress():
    global progress_bar
    text_length = len(sample_label.cget('text'))
    typed_length = len(input_entry.get())
    if sample_label.cget('text').startswith(input_entry.get()):
        progress = (typed_length / text_length) * 100
        progress_bar["value"] = progress


def reset():
    global running
    global counter
    running = False
    counter = 0
    speed_label.config(text="Speed: \n0.00 cps\n0.00 cpm\n0.00 wps\n0.00 wpm")
    sample_label.config(text=random.choice(texts))
    input_entry.delete(0, tk.END)
    input_entry.config(fg="black", highlightbackground="light blue", highlightcolor="light blue")
    progress_bar["value"] = 0


input_entry.bind("<KeyRelease>", start)

reset_button = tk.Button(frame, text="Reset", command=reset, font=("Helvetica", 24))
reset_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

frame.pack(expand=True)

counter = 0
running = False

root.mainloop()
