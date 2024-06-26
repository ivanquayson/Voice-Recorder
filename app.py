# import required libraries
import os.path

import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

import numpy as np
import time


# Normalize audio levels
def normalize(audio):
    max_val = np.max(np.abs(audio), axis=0)
    if max_val == 0:
        return audio
    return audio / max_val


# Sampling frequency
freq = 48000

# Get user input for audio duration
duration = int(input("Enter duration: "))

# Get user input for file name
file_name = input("Enter file name: ")

try:
    # Start recording with given frequency and duration values
    print("Recording...")
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)

    # Progress indicator for audio recording
    for i in range(duration):
        time.sleep(1)
        print(f"Recording...{i + 1}/{duration} seconds")

    # Record audio for a given number of seconds
    sd.wait()
    print("Recording complete.")

    # Normalize audio recording
    recording = normalize(recording)

    scipy_file = f"{file_name}_scipy_wav"
    wavio_file = f"{file_name}_wavio_wav"

    # Check if file already exists
    if os.path.exists(scipy_file) or os.path.exists(wavio_file):
        overwrite = input("File already exists. Overwrite existing file? (y/n): ")
        if overwrite.lower() != "y":
            print("Operation cancelled.")
            exit()
    else:
        # Save the recording using scipy.io.wavfile.write
        write(scipy_file, freq, recording)
        print(f"Saved using scipy.io.wavfile.write as {scipy_file}.")

        # Save the recording using wavio.write
        wv.write(wavio_file, recording, freq, sampwidth=2)
        print(f"Saved using wavio.write as {wavio_file}.")

except Exception as e:
    print(f"An error occurred: {e}")

"""
1. sounddevice: This library is used to record and play sound. It provides access to
audio input and output devices.
2.scipy.io.wavfile.write: This function is used to save audio data as a WAV file.
3. wavio.write: Another function to save audio data as a WAV file, allowing for more control
over the file parameters like sample width.
4. freq: 44.1 kHz or 48 kHz is sufficient. These frequencies provide good audio quality and are
widely supported by audio hardware and software
5. duration: This specifies how long the recording will last, set to 5 seconds.
6. sd.rec(int(duration * freq), samplerate=freq, channels=2): This starts recording audio.
        int(duration * freq): The total number of samples to record. This is calculated by
        multiplying the duration (in seconds) by the sampling frequency (samples per second).
7. samplerate=freq: The sampling frequency.
8. channels=2: Specifies stereo recording (2 channels).
9. sd.wait(): Pauses the script until the recording is complete.
10. print("Recording complete."): Notifies the user that the recording is finished.
11. sampwidth=2: Specifies the sample width (16 bits per sample).
"""
