import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import sounddevice as sd
import time

# Load audio
seconds = 10
input_custom_time_filename = "mp3_input/bass_NEICD_clean.mp3"
y, sr = librosa.load(input_custom_time_filename)

y = y[:seconds * sr]
duration = len(y) / sr

# Plot waveform
plt.ion()  # interactive mode
fig, ax = plt.subplots(figsize=(12, 4))
librosa.display.waveshow(y, sr=sr, ax=ax)
ax.set_title("Waveform with Synced Playhead")
playhead = ax.axvline(0, color='red')

plt.show()

# Start audio playback in background
sd.play(y, sr)

# Sync playhead with real time
start_time = time.time()
while sd.get_stream().active:
    elapsed = time.time() - start_time
    if elapsed > duration:
        break
    playhead.set_xdata([elapsed])
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.01)  # update ~100 fps

sd.wait()
plt.ioff()
