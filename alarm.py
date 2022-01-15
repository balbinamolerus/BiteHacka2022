import time, audioop
import pyaudio

# Initialisation for PyAudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 1

threshold = 10
reading = 0
previousreading = 0

# PyAudio Object
audio = pyaudio.PyAudio()

while True:
        stream = audio.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
        frames = []

        for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
                data = stream.read(70)
                frames.append(data)
                time.sleep(0.001)

        reading = audioop.max(data, 2)
        if reading - previousreading > threshold:
                print(reading)
        previousreading = reading

        stream.stop_stream()
        stream.close()

# Clearing the resources
stream.stop_stream()
stream.close()
audio.terminate()