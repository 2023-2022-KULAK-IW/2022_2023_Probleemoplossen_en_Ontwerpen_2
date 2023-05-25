import numpy as np
from scipy.optimize import fsolve

def hoekV(afstandBeker):
    waterDebiet = 4  # l/min (3.95 is standaardwaarde), komt van waterflowsensor
    straal = 0.0015
    hoogtePlatform = 0.47
    lengteArm = 0.17
    afstandCamera = 0.1 # lengte tussen beginpunt arm en camera
    hoogteBeker = 0.4

    snelheid = (waterDebiet * 1.6667*10**(-5))/(np.pi * (straal ** 2))
    def func(a):
        return [-afstandBeker + np.cos(a[0]) * snelheid * a[1] + np.cos(a[0]) * lengteArm - afstandCamera,
                -hoogteBeker + hoogtePlatform + np.sin(a[0]) * lengteArm + np.sin(a[0]) * snelheid * a[1] - 1 / 2 * 9.81 * (a[1]**2)]

    opl = fsolve(func, [np.pi/2, 10] )
    opl[0] = opl[0] * 180 / np.pi
    #opl[0]: hoek (in graden)
    
    return opl[0]

print(hoekV(2000))

