import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3
from pygame import mixer

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")

statusbar = ttk.Label(root, text="@Welcome to Muzix", relief=SUNKEN, anchor=W, font='Times 10 bold')
statusbar.pack(side=BOTTOM, fill=X)

# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# Create the submenu

subMenu = Menu(menubar, tearoff=0)

playlist = []


def browse_file():
    global play_song
    play_song = filedialog.askopenfilename()
    add_to_playlist(play_song)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, play_song)
    index += 1


menubar.add_cascade(label="...", menu=subMenu)
subMenu.add_command(label="Browse", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Muzix', 'This is a music player build using Python Tkinter')


subMenu =  Menu(menubar, tearoff=0)
menubar.add_cascade(label="?", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  # initializing the mixer

root.title("Muzix")
root.iconbitmap(r'img/Muzix.ico')

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=10, pady=10)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addbtn = ttk.Button(leftframe, text='+ Add', command=browse_file)
addbtn.pack(side=LEFT)


def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

delbtn = ttk.Button(leftframe, text='-Del', command = del_song)
delbtn.pack(side=RIGHT)

rightframe = Frame(root)
rightframe.pack(pady=10)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text='Total Length : --:--', font='Arial 10 bold')
lengthlabel.pack()

currenttimelabel = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused

    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Muzix could not find the file. Please check again.')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def restart_music():
    play_music()
    statusbar['text'] = "Music Restarted"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.5)
        volumeBtn.configure(image=volumePhoto)
        scale.set(50)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

playPhoto = PhotoImage(file='img/5.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=1, padx=10)

stopPhoto = PhotoImage(file='img/Stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=0, padx=10)

pausePhoto = PhotoImage(file='img/Pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

# Bottom Frame for volume, rewind, mute etc.

bottomframe = Frame(rightframe)
bottomframe.pack()

restartPhoto = PhotoImage(file='img/Restart.png')
restartBtn = Button(bottomframe, image=restartPhoto, command=restart_music)
restartBtn.grid(row=0, column=0, padx=15)

mutePhoto = PhotoImage(file='img/001-mute.png')
volumePhoto = PhotoImage(file='img/002-volume.png')
volumeBtn = Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(50)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.5)
scale.grid(row=0, column=2, pady=15, padx=5)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
