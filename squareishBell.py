import numpy as np
import matplotlib.pyplot as plt

def tukey(n, a, N):
    ans = 0.0
    if 0 <= abs(n) and abs(n) <= (a*N/2.0):
        #print(1)
        ans = 1.0
    else:
        #print(2)
        if (a*N/2.0) <= abs(n) and abs(n) <= (N/2+N/20):
            ans = 0.5*(1.0+np.cos(np.pi*((abs(n)-(a*N/2.0))/(2*(1-a)*N/2.0))))
    return ans

def tukeyT(N, a):
    ans = []
    for n in range(-N,N):
        ans.append(tukey(n, a, N))
    return ans
tukeyArr = tukeyT(40, 0.9)
tukeyArrX = range(int(-len(tukeyArr)/2)+420, int(len(tukeyArr)/2)+420)
#plt.title("tukey")
#plt.plot(tukeyArrX, tukeyArr, color="red")
#plt.show()

j = 0
tukeyW = [0]*1024
tukeyWx = range(1024)
for i in range(1024):#puts the tukey window on the 1024 array, with the rectangular part from 400 to 440
    if i >= 380 and i <= 459:
        tukeyW[i] = tukeyW[i]+tukeyArr[j]
        if tukeyW[i] > 1:
            tukeyW[i] -= 0.1
        j += 1

print(tukeyW)
plt.title("tukey")
plt.plot(tukeyWx, tukeyW, color="red")
plt.show()



