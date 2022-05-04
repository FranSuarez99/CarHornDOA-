from cmath import sqrt
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
time1, time2, time3 = 0, 0, 0
#start streams
p=pyaudio.PyAudio()
stream1=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,input_device_index=1,
                frames_per_buffer=CHUNK)
stream2=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,input_device_index=6,
                frames_per_buffer=CHUNK)
stream3=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,input_device_index=3,
                frames_per_buffer=CHUNK)
def audioFunc1():
    global data1, syncP1, sync1, stream1, time1
    print("audioFunc1")
    for i in range(500):
        #print("audio1",i)
        t1 = time.time()
        data1 = np.frombuffer(stream1.read(CHUNK, exception_on_overflow = False),dtype=np.int16)
        if len(data1) != 0:
            maxIndex1 = data1.index(max(data1))
            time1 = (1/4/1024)*maxIndex1
            time1 = time1+t1
            syncP1 = True
            sync1 = True
        while syncP1:
            a = 1
    # close the stream gracefully
    stream1.stop_stream()
    stream1.close()
    p.terminate()

def audioFunc2():
    global data2, syncP2, sync2, stream2, time2
    print("audioFunc2")
    for i in range(500):
        #print("audio2",i)
        t2 = time.time()
        data2 = np.frombuffer(stream2.read(CHUNK, exception_on_overflow = False),dtype=np.int16)
        if len(data2) != 0:
            maxIndex1 = data1.index(max(data1))
            time2 = (1/4/1024)*maxIndex1
            time2 = time2+t2
            syncP2 = True
            sync2 = True
        while syncP2:
            a = 1
    # close the stream gracefully
    stream2.stop_stream()
    stream2.close()
    p.terminate()

def audioFunc3():
    global data3, syncP3, sync3, stream3, time3
    print("audioFunc3")
    for i in range(500):
        #print("audio3",i)
        t3 = time.time()
        data3 = np.frombuffer(stream3.read(CHUNK, exception_on_overflow = False),dtype=np.int16)
        if len(data3) != 0:
            maxIndex1 = data1.index(max(data1))
            time3 = (1/4/1024)*maxIndex1
            time3 = time3+t3
            syncP3 = True
            sync3 = True
        while syncP3:
            a = 1
    # close the stream gracefully
    stream3.stop_stream()
    stream3.close()
    p.terminate()

def DOA(t1, t2, t3):
    ans = None
    times = [t1, t2, t3]
    if len(set(times)) != len(times):
        if t1 == t2:
            if t3 < t1:
                ans = 330
            else:
                ans = 150
        else:
            if t1 == t3:
                if t2 < t1:
                    ans = 200
                else:
                    ans = 30
            else:
                if t1 < t2:
                    ans = 90
                else:
                    ans = 270
    micPairs = [t1-t2, t1-t3, t2-t3]
    tau = min((abs(x), x) for x in micPairs)
    ABp = (tau * soundSpeed)^2
    x = sqrt(-(ABp*(ABp-4*(micDist^2)))/(4*(4*(micDist^2)-ABp)))
    y1 = sqrt((ABp/4)-(micDist^2)+((x^2)*((4*(micDist^2))/(ABp)-1)))
    y2 = -y1
    m = y1/x
    angle = np.arctan(m)
    if angle >= 0:
        ans = 90-angle
    else:
        ans = -90-angle
    return ans

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