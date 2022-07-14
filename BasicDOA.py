from cmath import sqrt
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time
import math
#import threading
from threading import Thread
#import sounddevice as sd
#print(sd.query_devices())#print all soud devices, the index will be used on the stream

#CHUNK = 1024# number of data points to read at a time
#RATE = 4096 # time resolution of the recording device (Hz)
#RATE = CHUNK

tukeyW = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.24644660940672594, 0.5999999999999999, 0.9535533905932737, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9535533905932737, 0.5999999999999999, 0.24644660940672594, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

CHUNK = 12000# number of data points to read at a time
RATE = 48000# time resolution of the recording device (Hz)
#RATE has to be 48000 for compatibility issues with some sound drivers, including that of the Raspberry Pi 3
soundSpeed = 343.2
micDist = 0.33/2#distance between mics over 2
maxDOA = micDist / float(soundSpeed)
hornFreq = 420#target frequency
hornTime = 0
n = 8#number of samples before a horn is considered a long horn
data1, data2, data3 = [], [], []
sync1, sync2, sync3 = False, False, False
syncP1, syncP2, syncP3 = False, False, False
time1, time2, time3 = 0, 0, 0
#start streams
p=pyaudio.PyAudio()
stream1=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,input_device_index=1,
                frames_per_buffer=CHUNK)#stream for mic 1, input_device_index should be that of mic 1
stream2=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,input_device_index=5,
                frames_per_buffer=CHUNK)#stream for mic 2, input_device_index should be that of mic 2
stream3=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,input_device_index=7,
                frames_per_buffer=CHUNK)#stream for mic 3, input_device_index should be that of mic 3
def audioFunc1():#thread for mic 1
    global data1, syncP1, sync1, stream1, time1
    print("audioFunc1")
    for i in range(500):
        #print("audio1",i)
        time1 = time.time()
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

def audioFunc2():#thread for mic 2
    global data2, syncP2, sync2, stream2, time2
    print("audioFunc2")
    for i in range(500):
        #print("audio2",i)
        time2 = time.time()
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

def audioFunc3():#thread for mic 3
    global data3, syncP3, sync3, stream3, time3
    print("audioFunc3")
    for i in range(500):
        #print("audio3",i)
        time3 = time.time()
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
"""
def DOA(t1, t2, t3):
    t1, t2, t3
    ans = None
    times = [t1, t2, t3]
    if len(set(times)) != len(times):3 if there are two or more equal time reads
        if t1 == t2:
            if t3 < t1:
                ans = 330
            else:
                ans = 150
        else:
            if t1 == t3:
                if t2 < t1:
                    ans = 210
                else:
                    ans = 30
            else:
                if t1 < t2:
                    ans = 90
                else:
                    ans = 270
    micPairs = [abs(t1-t2), abs(t1-t3), abs(t2-t3)]
    tau = float(min(micPairs))
    ABp = (tau * soundSpeed)**2.0
    #x = math.sqrt(-(ABp*(ABp-4.0*(micDist**2.0)))/(4.0*(4.0*(micDist**2.0)-ABp)))#x coordinate of the sound source
    x = 1#asumming the sound source to be 1 meter away on the x coordinate gives a good aproximation
    y1 = math.sqrt((ABp/4.0)-(micDist**2.0)+((x**2.0)*((4.0*(micDist**2.0))/(ABp)-1.0)))#y coordinate of the sound source
    y2 = -y1#gives the negative in case the y coordinate is on the other side
    m = y1/x#
    angle = np.arctan(m)
    if angle >= 0:
        ans = 90-np.degrees(angle)
    else:
        ans = -90-np.degrees(angle)
    return ans#returns the angle in degrees
"""
def auxProcessing(data):
    fft = abs(np.fft.fft(data).real)
    fft = fft[:int(len(fft)/2)]
    freq = np.fft.fftfreq(CHUNK,1.0/RATE)
    freq = freq[:int(len(freq)/2)]
    freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1
    #print("peak frequency: %d Hz"%freqPeak)#peak frequency of the whole fft
    if (freqPeak<450)and(freqPeak>390):#its the peak frequency in a horn range?
        hornTimer = True
        if hornTime > n and hornTimer:#have the horn been the peak frquency for the last n CHUNK/RATE seconds? 
            print("Long Horn")#this will be an extra haptic output so the user knows 
        carSpeed = -(((soundSpeed*hornFreq)/freqPeak)-soundSpeed)#relative speed of the horn source and the observer in m/s
        carSpeedKM = carSpeed*(3.6)#turns m/s to km/h
        #print("CARSPEED")
        #print(carSpeedKM)#this will be a parameter that affects the tipe of haptic feedback the user recives
    else:
        hornTimer = False#if thre is no horn even for a moment, the timer is set to 0 again
        carSpeedKM = None
    #newFft = fft*tukeyW
    #newData = np.fft.ifft(newFft)

    return carSpeedKM, hornTimer, freqPeak, fft

def processing():
    global data1, data2, data3, syncP1, syncP2, syncP3, sync1, sync2, sync3, hornTime, time1, time2, time3
    print("processing")
    for i in range(99999999999999999):
        if sync1 and sync2 and sync3:
            sync1 = False
            sync2 = False
            sync3 = False

            carSpeedKM1, hornTime1, freq1, fft1 = auxProcessing(data1)
            carSpeedKM2, hornTime2, freq2, fft2 = auxProcessing(data2)
            carSpeedKM3, hornTime3, freq3, fft3 = auxProcessing(data3)

            if hornTime1 or hornTime2 or hornTime3:
                hornTime += 1
                micMag = [fft1[int(freq1)], fft2[int(freq2)], fft3[int(freq3)]]#volume of the peak frequency of each microphone
                micCar = [carSpeedKM1, carSpeedKM2, carSpeedKM3]#speed detected by each micriphone on the same order as micMag
                maxIndex = np.argmax(micMag)#takes the position on the arry with the max value , which is the same as the mic with the loudest detected car horn sound
                print("Horn on mic",maxIndex)
                print("Car speed:",micCar[maxIndex])#prints speed of the loudest detected car horn sound
                if hornTime >= n:#detection of a long horn
                    print("long horn")
                """
                print("Data1")
                print(fft1[int(freq1)])
                print("Data2")
                print(fft2[int(freq2)])
                print("Data3")
                print(fft3[int(freq3)])
                """
            else:#if no car horn sound is detected, the counter resets
                hornTime = 0

            #angle = DOA(timer1, timer2, timer3)

            syncP1 = False
            syncP2 = False
            syncP3 = False

if __name__ == '__main__':
    Thread(target = audioFunc1).start()
    Thread(target = audioFunc2).start()
    Thread(target = audioFunc3).start()
    Thread(target = processing).start()