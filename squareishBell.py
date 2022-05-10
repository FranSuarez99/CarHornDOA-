import numpy as np
import matplotlib.pyplot as plt

"""
def hann(n,M):
    #return 0.54-0.46*np.cos((2*np.pi*n)/M-1)
    return -np.cos((2*np.pi*n)/M-1)

def hannW(M):
    ans = []
    for n in range(M*2):
        ans.append(hann(n,M))
    return ans
ans = hannW(1000)
print("ans")
#print(ans)
ansY = range(1000*2)
plt.title("Line graph")
plt.plot(ansY, ans, color="red")
plt.show()
"""
def tukey(n, a, N):
    ans = 0.0
    if 0 <= abs(n) and abs(n) <= (a*N/2.0):
        #print(1)
        ans = 1.0
        #ans = 0.5 * (1-(np.cos((2.0*np.pi*n)/a*N)))
    else:
        #print(2)
        if (a*N/2.0) <= abs(n) and abs(n) <= (N/2+N/20):
            ans = 0.5*(1.0+np.cos(np.pi*((abs(n)-(a*N/2.0))/(2*(1-a)*N/2.0))))
        else:
            e = 0
            #print(3)
    return ans

def tukeyT(N, a):
    ans = []
    for n in range(-N,N):
        ans.append(tukey(n, a, N))
    return ans
tukeyArr = tukeyT(40, 0.9)
#print(tukeyArr)
tukeyArrX = range(int(-len(tukeyArr)/2)+420, int(len(tukeyArr)/2)+420)
plt.title("tukey")
plt.plot(tukeyArrX, tukeyArr, color="red")
plt.show()
j = 0
print(len(tukeyArr))
tukeyW = [0.1]*1024
tukeyWx = range(1024)
for i in range(1024):
    if i >= 380 and i <= 459:
        tukeyW[i] = tukeyW[i]+tukeyArr[j]
        if tukeyW[i] > 1:
            tukeyW[i] -= 0.1
        j += 1


plt.title("tukey")
plt.plot(tukeyWx, tukeyW, color="red")
plt.show()



