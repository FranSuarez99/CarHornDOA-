import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time
import sounddevice as sd
print(sd.query_devices())#print all soud devices, the index will be used on the stream

soundSpeed = 343
hornFreq = 420
hornTime = 0
n = 8

plt.ion()#enable the use of animated plots
plt.plot(0,0)

np.set_printoptions(suppress=True) # don't use scientific notation

CHUNK = 1024# number of data points to read at a time
RATE = 4096 # time resolution of the recording device (Hz)
#RATE = CHUNK

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,input_device_index=1,
              frames_per_buffer=CHUNK) #input_device_index needs to be the same as the mic

# create a numpy array holding a single read of audio data
for i in range(500): #to it a few times just to see
    #data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    data = np.frombuffer(stream.read(CHUNK, exception_on_overflow = False),dtype=np.int16)
    #data = np.array(list(stream.read(CHUNK)),'int16')
    #data = data * np.hanning(len(data)) # smooth the FFT by windowing data
    #the hanning is disabled to avoid resolution loss
    fft = abs(np.fft.fft(data).real)
    fft = fft[:int(len(fft)/2)] # keep only first half
    freq = np.fft.fftfreq(CHUNK,1.0/RATE)
    freq = freq[:int(len(freq)/2)] # keep only first half
    freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1
    print("peak frequency: %d Hz"%freqPeak)#peak frequency of the whole fft
    if (freqPeak<450)and(freqPeak>390):#its the peak freuqncy in a horn range?
        hornTime += 1
        if hornTime > n:#have the horn been the peak frquency for the last n CHUNK/RATE seconds? 
            print("Long Horn")#this will be an extra haptic output so the user knows 
        carSpeed = -(((soundSpeed*hornFreq)/freqPeak)-soundSpeed)#relative speed of the horn source and the observer in m/s
        carSpeedKM = carSpeed*(3.6)#turns m/s to km/h
        print("CARSPEED")
        print(carSpeedKM)#this will be a parameter that affects the tipe of haptic feedback the user recives
    else:
        hornTime = 0#if thre is no horn even for a moment, the timer is set to 0 again

    # uncomment this if you want to see what the freq vs FFT looks like
    plt.plot(freq,fft)
    plt.axis([390,450,None,None])
    plt.pause(0.05)#this pause is only for the plot and has nothing to do with the haptic feedback
plt.ioff()
plt.show()
# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()
