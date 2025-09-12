from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
import numpy as np
import librosa

input_custom_time_filename = "mp3_input/bass_NGHYB_clean_20_seconds.mp3"
# sf.write(input_custom_time_filename, x_custom_time, sr)

# Load audio
y, sr = librosa.load(input_custom_time_filename)

# Plot waveform
fig, ax = plt.subplots(figsize=(12, 4))
librosa.display.waveshow(y, sr=sr, ax=ax)
ax.set_title("Waveform with Playhead")

# Add a vertical line for the playhead
playhead = ax.axvline(0, color='red')

# Playback duration
duration = len(y) / sr

# Start audio playback
sd.play(y, sr)

# Animation update: move the line according to time
def update(frame):
    t = frame / 100  # frame index → time (s), 100 fps
    playhead.set_xdata([t])
    return playhead,

ani = FuncAnimation(fig, update, frames=int(duration * 100),
                    interval=10, blit=True, repeat=False)

plt.show()

sd.wait()  # wait for playback to finish