from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkCheckBox, CTkSlider, CTkImage, CTkScrollableFrame, CTkTabview, CTkEntry
from CTkListbox import *

import os
import re
from os.path import expanduser
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #shhh pygame
import subprocess
import keyboard
import pygame as pg
import json
import glob
import tkinter as tk
import tkinter.messagebox
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from pydub import AudioSegment

#reading in mp3 data
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from io import BytesIO

#downloading and separating without making window unresponsive
import threading
import demucs.separate
import shutil

import urllib.request
homedir = os.path.expanduser("~")

state=1
stem_list = []
note_objects=[]
mutevols=[0,0,0,0]
merging = False

root = CTk()
startstop_bridge = tk.IntVar()
startstop_bridge.set(0)
root.title('Stem Player')
root.protocol("WM_DELETE_WINDOW", lambda: close_window())

#downloading song data fields
model = "mdx_extra"
downloaded_song_path = "downloaded_songs"
separated_path = os.path.join("separated", model)

# Configure the grid
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# def create_config():
#     import platform
#     if not os.path.exists(homedir + "/stemplayerplayer_config.json"): ##create config if doesn't exist
#         default_config = {
#         "KEY_INSTRUMENTALS": "1",
#         "KEY_VOCALS": "2",
#         "KEY_BASS": "3",
#         "KEY_DRUMS": "4",
#         "KEYBINDS_ENABLED": 0,
#         }
#         if 'SPP_HOME' not in default_config:
#             if platform.system() == 'Windows':
#                 default_config["SPP_HOME"] = homedir + "\\stemplayer"
#             else:
#                 default_config["SPP_HOME"] = homedir + "/stemplayer"
#         tempjson = json.dumps(default_config, indent=2)
#         with open(homedir + "/stemplayerplayer_config.json", "w") as jsonfile:
#             jsonfile.write(tempjson)
#         # tempjson.close()

# create_config()
#load config
# with open(homedir + "/stemplayerplayer_config.json", encoding="utf-8") as config_file:
#     SPP_CONFIG = json.load(config_file)
#     KEY_INSTRUMENTALS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_INSTRUMENTALS"])[0]
#     KEY_VOCALS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_VOCALS"])[0]
#     KEY_BASS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_BASS"])[0]
#     KEY_DRUMS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_DRUMS"])[0]
#     KEYBINDS_ENABLED = SPP_CONFIG["KEYBINDS_ENABLED"]
#     SPP_HOME = SPP_CONFIG["SPP_HOME"]
#     if not os.path.exists(SPP_HOME):
#         os.makedirs(SPP_HOME)

# from stembridge import *

# def open_config():
#     import platform
#     global KEY_INSTRUMENTALS, KEY_VOCALS, KEY_BASS, KEY_DRUMS
#     if platform.system() == 'Windows':
#         subprocess.Popen("notepad.exe " + homedir + "/stemplayerplayer_config.json", creationflags=0x08000000) #flag for CREATE_NO_WINDOW
#     elif platform.system() == 'Linux':
#         subprocess.Popen("xdg-open " + homedir + "/stemplayerplayer_config.json")
#     elif platform.system() == 'Darwin':
#         subprocess.Popen("open " + homedir + "/stemplayerplayer_config.json")

#     '''
#     with open(homedir + "/stemplayerplayer_config.json", encoding="utf-8") as config_file: #reimport keybinds
#         SPP_CONFIG = json.load(config_file)
#         KEY_INSTRUMENTALS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_INSTRUMENTALS"])[0]
#         KEY_VOCALS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_VOCALS"])[0]
#         KEY_BASS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_BASS"])[0]
#         KEY_DRUMS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_DRUMS"])[0]
#         SPP_HOME = SPP_CONFIG["SPP_HOME"]
#     '''
        
def change_time_slider(value):
    pass

def time_and_scale():
    if note_objects:
        print(pg.mixer.music.get_pos())

def slider(value):
    i = instrumentals_Scale.get()
    v = vocals_Scale.get()
    b = bass_Scale.get()
    d = drums_Scale.get()

    if note_objects:    #suppress stupid error
        note_objects[0].set_volume(i)
        note_objects[1].set_volume(v)
        note_objects[2].set_volume(b)
        note_objects[3].set_volume(d)


# def toggle_keybinds():
#     print(onoff.get())

# def check_keybinds():
#     ##hell keybinds
#     if keyboard.is_pressed(KEY_INSTRUMENTALS) and onoff.get() == 1:
#         toggle_channel(1)
                
#     if keyboard.is_pressed(KEY_VOCALS)and onoff.get() == 1:
#         toggle_channel(2)

#     if keyboard.is_pressed(KEY_BASS) and onoff.get() == 1:
#         toggle_channel(3)
            
#     if keyboard.is_pressed(KEY_DRUMS) and onoff.get() == 1:
#         toggle_channel(4)
#     root.after(1, check_keybinds)

def toggle_channel(toToggle):
    #print("hello from togglechannel")
    if note_objects:  #suppress stupid error pt 2
        if toToggle == 1:
            print ("1")
            if note_objects[0].get_volume() != 0.0:
                mutevols[0] = note_objects[0].get_volume()
                note_objects[0].set_volume(0.0)
            elif note_objects[0].get_volume() == 0.0:
                note_objects[0].set_volume(mutevols[0])
            print(note_objects[0].get_volume())
            # while keyboard.is_pressed(KEY_INSTRUMENTALS):
            #     keyboard.block_key(KEY_INSTRUMENTALS)
            # keyboard.unhook_all()
        elif toToggle == 2:
            print ("2")
            if note_objects[1].get_volume() != 0.0:
                mutevols[1] = note_objects[1].get_volume()
                note_objects[1].set_volume(0.0)
            elif note_objects[1].get_volume() == 0.0:
                note_objects[1].set_volume(mutevols[1])
            print(note_objects[1].get_volume())
            # while keyboard.is_pressed(KEY_VOCALS):
            #     keyboard.block_key(KEY_VOCALS)
            # keyboard.unhook_all()
        elif toToggle == 3:
            print ("3")
            if note_objects[2].get_volume() != 0.0:
                mutevols[2] = note_objects[2].get_volume()
                note_objects[2].set_volume(0.0)
            elif note_objects[2].get_volume() == 0.0:
                note_objects[2].set_volume(mutevols[2])
            print(note_objects[2].get_volume())
            # while keyboard.is_pressed(KEY_BASS):
            #     keyboard.block_key(KEY_BASS)
            # keyboard.unhook_all()
        elif toToggle == 4:
            print ("4")
            if note_objects[3].get_volume() != 0.0:
                mutevols[3] = note_objects[3].get_volume()
                note_objects[3].set_volume(0.0)
            elif note_objects[3].get_volume() == 0.0:
                note_objects[3].set_volume(mutevols[3])
            print(note_objects[3].get_volume())
            # while keyboard.is_pressed(KEY_DRUMS):
            #     keyboard.block_key(KEY_DRUMS)
            # keyboard.unhook_all()
    else:
        return
        

def pause_play():
    global state
    if state==1:
        state=0
        print("Pausing!")
        pg.mixer.pause()
        pause_play_image = CTkImage(Image.open("play_icon.png"), size= (30,30))
    elif state==0:
        state=1
        print("Unpausing!")
        pg.mixer.unpause()
        pause_play_image = CTkImage(Image.open("pause_icon.png"), size= (30,30))

    pauseplay.configure(image=pause_play_image)

def close_window():
    global onoff
    # with open(homedir + "/stemplayerplayer_config.json") as json_file:
    #     jsontemp = json.load(json_file)
    # jsontemp['KEYBINDS_ENABLED'] = onoff.get()
    
    # with open(homedir + "/stemplayerplayer_config.json", 'w') as json_file:
    #     json.dump(jsontemp, json_file)
    pg.mixer.quit()
    pg.quit()
    root.destroy()
    exit()

def show_value(selected_option):
    # print(selected_option)
    # folder_path = "downloaded_songs"
    folder_path = os.path.join(separated_path,selected_option)
    # print(path)

    pg.mixer.stop()
    global note_objects
    global stem_list
    stem_list=[]

    if glob.glob(folder_path + "/*.mp3"):
        print("Using MP3...")
        # stem_list = glob.glob(folder_path + '/*[0-9].mp3')
        stem_filenames = ["drums.mp3", "bass.mp3", "other.mp3", "vocals.mp3"]
        stem_list = [folder_path+"/"+filename for filename in stem_filenames ]

        #get metadata
        #relies on original song being in the same folder
        #this will be called original
        original_path = folder_path+"/"+"original.mp3"
        if(os.path.isfile(original_path)):
            print("metadata found")
            tags = ID3(original_path)
            song = tags['TIT2']
            artist = tags['TPE1']
            lyrics = tags['USLT::XXX']
            album_art = tags['APIC:Cover'].data
            im = Image.open(BytesIO(album_art))

            #update values
            song_name_lab.configure(text = song)
            artist_name_lab.configure(text = artist)
            # lyric_label.configure(text = lyrics)
            album_cover_lab.configure(image=CTkImage(im, size= (300,300)))
        else:
            print("can't get metadata")
        
        a1Note = pg.mixer.Sound(stem_list[0])
        a2Note = pg.mixer.Sound(stem_list[1])
        a3Note = pg.mixer.Sound(stem_list[2])
        a4Note = pg.mixer.Sound(stem_list[3])

        if merging == False:
            a1Note.play()
            a2Note.play()
            a3Note.play()
            a4Note.play()
        note_objects = [a1Note, a2Note, a3Note, a4Note]
    else:
        print("Can't play this song")

def download_into_new_dir(dir, url):
    progress_lbl.configure(text = "Downloading")
    
    current_wd = os.getcwd()
    os.chdir(dir) # change working directory

    #call splotdl downloading from url
    os.system(f"spotdl {url}") # saves as mp3 this will have the metadata encoded into it 

    os.chdir(current_wd) # change working directory back to original

def unseparated_mp3():
    progress_lbl.configure(text = "Separating")
    #get list of all separated directories
    separated = [directory for directory in os.listdir(separated_path) if os.path.isdir(os.path.join(separated_path,directory))]
    #get list of all downloaded songs (mp3)
    downloaded_songs = [song[:-4] for song in os.listdir(downloaded_song_path) if song.endswith(".mp3")]

    #get all songs which don't appear in separated directories
    non_separated = list(set(downloaded_songs) - set(separated))
    non_separated = [song+".mp3" for song in non_separated]
    
    return(non_separated)

def separate(mp3_filename):
    mp3_path = os.path.join(downloaded_song_path, mp3_filename)
    demucs.separate.main(["--mp3", "-n", model, mp3_path])

def separate_all_songs(all_unseparated):
    for song in all_unseparated:
        separate(song)

def copy_to_new_folder(song_name):
    song_dir_path = os.path.join(separated_path, song_name, "original.mp3")

    if not os.path.isfile(song_dir_path):
        #copy
        original_song_path = os.path.join(downloaded_song_path,song_name+".mp3")
        shutil.copyfile(original_song_path, song_dir_path)

def copy_original_all_songs():
    all_separated = [directory for directory in os.listdir(separated_path) if os.path.isdir(os.path.join(separated_path,directory))]
    for song in all_separated:
        copy_to_new_folder(song)

def download_and_separate_threaded(text):
    download_into_new_dir("downloaded_songs", text)
    unseparated = unseparated_mp3()
    separate_all_songs(unseparated)
    copy_original_all_songs()

    progress_lbl.configure(text = "Finished")

def download_and_separate():
    text = new_song_url.get()  # Get the text from the Entry widget
    if text:  # Check if the text is not empty
        threading.Thread(target=download_and_separate_threaded, args=(text,), daemon=True).start()
        
        new_song_url.delete(0, tk.END)  # Clear the Entry widget


pg.mixer.init()

frame_picture = CTkFrame(root)
# frame_picture.pack(pady=20, padx=20)

#image
# album_cover = CTkImage(Image.open("sushi_for_breakfast_album_art.jpeg"), size= (300,300))
album_cover = CTkImage(Image.open("grey_square.jpg"), size= (300,300))
album_cover_lab = CTkLabel(frame_picture, text="", image=album_cover)
# album_cover_lab.grid(row=0,column=0, padx=10, pady=10)
album_cover_lab.pack(padx = 10, pady = 10)

#song name
song_name_lab = CTkLabel(frame_picture, text = "Song", font=("Arial", 16))
# song_name_lab.grid(row=1,column=0, padx=10, pady=10)
song_name_lab.pack(padx = 10, pady = 5)

#artist name 
artist_name_lab = CTkLabel(frame_picture, text="Artist", font=("Arial", 14, "bold"))
# artist_name_lab.grid(row=2,column=0, padx=10, pady=10)
artist_name_lab.pack(padx = 10, pady = 5)

# #time slider
# time_slider = CTkSlider(frame_picture, from_=0.0, to=1.0, orientation=HORIZONTAL, command=change_time_slider)
# time_slider.grid(row=3,column=0)
# time_slider.set(0)

pause_icon = CTkImage(Image.open("pause_icon.png"), size= (30,30))
pauseplay = CTkButton(frame_picture, text="", font=("Arial", 12, "bold"), command=lambda: pause_play(), image=pause_icon)
# pauseplay.grid(row=3, column=0, padx=10, pady=10)
pauseplay.pack(padx = 10, pady = 10)

# get_time = CTkButton(frame_picture, text = "time", command=time_and_scale)
# get_time.grid(row=5, column=0)

#frame for stem sliders
frame = CTkFrame(root)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=3)
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_rowconfigure(3 , weight=1)
# frame.pack(pady=5)

instrumentals_label = CTkLabel(frame, text="Drums", font=("Arial", 12, "bold"))
instrumentals_label.grid(row=0, column=0)
# instrumentals_label.pack(side = tk.LEFT)


instrumentals_Scale = CTkSlider(frame, from_=0.0, to=1.0, orientation=HORIZONTAL, command=slider)
instrumentals_Scale.grid(row=0, column=1)
# instrumentals_Scale.pack(side = tk.RIGHT)
instrumentals_Scale.set(1.0)

vocals_label = CTkLabel(frame, text="Bass", font=("Arial", 12, "bold"))
vocals_label.grid(row=1, column=0)
# vocals_label.pack(side = tk.LEFT)

vocals_Scale = CTkSlider(frame, from_=0.0, to=1.0, orientation=HORIZONTAL, command=slider)
vocals_Scale.grid(row=1, column=1)
# vocals_Scale.pack(side = tk.RIGHT)
vocals_Scale.set(1.0)

bass_label = CTkLabel(frame, text="Accompaniment", font=("Arial", 12, "bold"))
bass_label.grid(row=2, column=0)
# bass_label.pack(side = tk.LEFT)

bass_Scale = CTkSlider(frame, from_=0.0, to=1.0, orientation=HORIZONTAL, command=slider)
bass_Scale.grid(row=2, column=1)
# bass_Scale.pack(side = tk.RIGHT)
bass_Scale.set(1.0)

drums_label = CTkLabel(frame, text="Vocals", font=("Arial", 12, "bold"))
drums_label.grid(row=3, column=0)
# drums_label.pack(side = tk.LEFT)

drums_Scale = CTkSlider(frame, from_=0.0, to=1.0, orientation=HORIZONTAL, command=slider)
drums_Scale.grid(row=3, column=1)
# drums_Scale.pack(side = tk.RIGHT)
drums_Scale.set(1.0)

#select song 
select_song_frame = CTkFrame(root)

select_tab =  CTkTabview(select_song_frame)
select_tab.add("Select Song")
select_tab.add("Add Song")
select_tab.set("Select Song")

# select_tab.grid(row = 0, column = 0)
select_tab.pack()

# select_tab.tab("Select Song").grid_rowconfigure(0, weight=1)
# select_tab.tab("Select Song").grid_columnconfigure(0, weight=1)

listbox = CTkListbox(select_tab.tab("Select Song"), command=show_value)
# listbox.pack(fill="both", expand=True, padx=10, pady=10)
# listbox.grid(row = 0, column = 0, padx=10, pady=10)
listbox.pack(fill="both", expand=True, padx=10, pady=10)
# new_song_folder_path = "separated"
mp3_songs = [directory for directory in os.listdir(separated_path) if os.path.isdir(os.path.join(separated_path,directory))]

for i, song in enumerate(mp3_songs):
    listbox.insert(i, song)

#import song
new_song_url = CTkEntry(select_tab.tab("Add Song"))
new_song_url.pack(fill=tk.X, padx=10, pady=10)  # Pack Entry to fill horizontally with padding

import_button = CTkButton(select_tab.tab("Add Song"), text="Import", command=download_and_separate)
import_button.pack(fill=tk.X, padx=10, pady=5)  # Pack Button to fill horizontally with padding

progress_lbl = CTkLabel(select_tab.tab("Add Song"), text="Enter URL")
progress_lbl.pack(fill=tk.X, padx=10, pady=5)

frame_picture.grid(row=0, column=0, rowspan=2, sticky="nsew", padx = 10, pady = 10)
frame.grid(row=0, column=1, sticky="nsew", padx = 10, pady = 10)
select_song_frame.grid(row=1, column=1, sticky="nsew", padx = 10, pady = 10)


# keybindsbutton = CTkButton(frame2, text="Edit config", font=("Arial", 12, "bold"), command=lambda: open_config())
# keybindsbutton.grid(row=3, column=3, sticky=W)

# mergebutton = CTkButton(frame2, text="Merge Stems", font=("Arial", 12, "bold"), command=lambda: merge_stems())
# mergebutton.grid(row=4, column=2, pady=2)

#startbridge = Button(frame2, text="Bridge on/off", font=("Arial", 12, "bold"), command=lambda: start_bridge())
#startbridge.grid(row=4, column=2, pady=2)


# startbridge = CTkCheckBox(root,
#                              text='Bridge Enabled',
#                              command=lambda: start_bridge(startstop_bridge.get()),
#                              font=("Arial", 12, "bold"),
#                              variable=startstop_bridge,
#                              onvalue=1,
#                              offvalue=0)
# startbridge.pack()



onoff = tk.IntVar()         #Keybinds toggle box
# onoff.set(KEYBINDS_ENABLED)
# tgkb = CTkCheckBox(root,
#                       text='Keybinds Enabled',
#                       command=toggle_keybinds,
#                       font=("Arial", 12, "bold"),
#                       variable=onoff,
#                       onvalue=1,
#                       offvalue=0)
# # tgkb.pack()

# root.after(1, check_keybinds)
root.mainloop()
