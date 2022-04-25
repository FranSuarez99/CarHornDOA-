import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time
import threading
from threading import Thread
#import sounddevice as sd
#print(sd.query_devices())#print all soud devices, the index will be used on the stream

#CHUNK = 1024# number of data points to read at a time
#RATE = 4096 # time resolution of the recording device (Hz)
#RATE = CHUNK

CHUNK = 12000
RATE = 48000

soundSpeed = 343.2
micDist = 0.33
maxDOA = micDist / float(soundSpeed)
hornFreq = 420
hornTime = 0
n = 8
data1, data2, data3 = [], [], []
sync1, sync2, sync3 = False, False, False
syncP1, syncP2, syncP3 = False, False, False

#start streams
p=pyaudio.PyAudio()
stream1=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,input_device_index=1,
                frames_per_buffer=CHUNK)
stream2=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,input_device_index=6,
                frames_per_buffer=CHUNK)
stream3=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,input_device_index=3,
                frames_per_buffer=CHUNK)
def audioFunc1():
    global data1, syncP1, sync1, stream1
    print("audioFunc1")
    for i in range(500):
        #print("audio1",i)
        data1 = np.frombuffer(stream1.read(CHUNK, exception_on_overflow = False),dtype=np.int16)
        if len(data1) != 0:
            syncP1 = True
            sync1 = True
        while syncP1:
            a = 1
    # close the stream gracefully
    stream1.stop_stream()
    stream1.close()
    p.terminate()

def audioFunc2():
    global data2, syncP2, sync2, stream2
    print("audioFunc2")
    for i in range(500):
        #print("audio2",i)
        data2 = np.frombuffer(stream2.read(CHUNK, exception_on_overflow = False),dtype=np.int16)
        if len(data2) != 0:
            syncP2 = True
            sync2 = True
        while syncP2:
            a = 1
    # close the stream gracefully
    stream2.stop_stream()
    stream2.close()
    p.terminate()

def audioFunc3():
    global data3, syncP3, sync3, stream3
    print("audioFunc3")
    for i in range(500):
        #print("audio3",i)
        data3 = np.frombuffer(stream3.read(CHUNK, exception_on_overflow = False),dtype=np.int16)
        if len(data3) != 0:
            syncP3 = True
            sync3 = True
        while syncP3:
            a = 1
    # close the stream gracefully
    stream3.stop_stream()
    stream3.close()
    p.terminate()

def DOA(d1, d2, d3, f):
    X1 = abs(np.fft.fft(d1).real)
    X2 = abs(np.fft.fft(d2).real)
    X3 = abs(np.fft.fft(d3).real)

    print("conj")
    print(np.angle(X1*np.conj(X2)))
    print(np.angle(X2*np.conj(X3)))
    

    ph_diff_12 = np.angle(X1*np.conj(X2))
    ph_diff_23 = np.angle(X2*np.conj(X3))

    tdoa_12 = ph_diff_12/(2*np.pi*f)
    tdoa_23 = ph_diff_23/(2*np.pi*f)

    weight = abs(X2)
    weight = weight/sum(weight)
    mean_tdoa_12 = sum(tdoa_12*weight)
    mean_tdoa_23 = sum(tdoa_23*weight)

    return [mean_tdoa_12, mean_tdoa_23]

def processing():
    global data1, data2, data3, syncP1, syncP2, syncP3, sync1, sync2, sync3
    print("processing")
    for i in range(99999999999999999):
        #print("processing",i)
        if sync1 and sync2 and sync3:
            sync1 = False
            sync2 = False
            sync3 = False
            #print("processing",i)
            fft = abs(np.fft.fft(data1).real)
            fft = fft[:int(len(fft)/2)] # keep only first half
            freq = np.fft.fftfreq(CHUNK,1.0/RATE)
            freq = freq[:int(len(freq)/2)] # keep only first half
            freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1
            #print("peak frequency: %d Hz"%freqPeak)#peak frequency of the whole fft
            if (freqPeak<450)and(freqPeak>390):#its the peak freuqncy in a horn range?
                hornTime += 1
                if hornTime > n:#have the horn been the peak frquency for the last n CHUNK/RATE seconds? 
                    print("Long Horn")#this will be an extra haptic output so the user knows 
                carSpeed = -(((soundSpeed*hornFreq)/freqPeak)-soundSpeed)#relative speed of the horn source and the observer in m/s
                carSpeedKM = carSpeed*(3.6)#turns m/s to km/h
                #print("CARSPEED")
                #print(carSpeedKM)#this will be a parameter that affects the tipe of haptic feedback the user recives
                ans = DOA(data1,data2,data3,freqPeak)
                print(ans)
            else:
                hornTime = 0#if thre is no horn even for a moment, the timer is set to 0 again
            syncP1 = False
            syncP2 = False
            syncP3 = False

if __name__ == '__main__':
    Thread(target = audioFunc1).start()
    Thread(target = audioFunc2).start()
    Thread(target = audioFunc3).start()
    Thread(target = processing).start()