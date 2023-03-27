import numpy as np
from scipy.optimize import fsolve

"""
input:
"""

waterDebiet = 3.95  # l/min (3.95 is standaardwaarde), komt van waterflowsensor
afstandBeker = 10.44  # komt van webcam
volumeGepasseerd = 0  # ml, komt van waterflowsensor

def hoekV(waterDebiet, afstandBeker):

    straal = 0.0029
    hoogtePlatform = 0.5
    lengteArm = 0.48
    afstandCamera = 0.02  # lengte tussen beginpunt arm en camera

    hoogteBeker = 0

    snelheid = (waterDebiet * 1.6667*10**(-5))/(np.pi * (straal ** 2))
    def func(a):
        return [-afstandBeker + np.cos(a[0]) * snelheid * a[1] + np.cos(a[0]) * lengteArm - afstandCamera,
                -hoogteBeker + hoogtePlatform + np.sin(a[0]) * lengteArm + np.sin(a[0]) * snelheid * a[1] - 1 / 2 * 9.81 * (a[1]**2)]

        opl = fsolve(func, [np.pi/2, 10])
        opl[0] = opl[0] * 180 / np.pi
        #opl[0]: hoek (in graden)
        return opl[0]


def stoppenPomp(volumeGepasseerd):
    volumeVullen = 0.0005  # m³
    extra = 0.0001  # extra volume, zodat we niet te weinig hebben
    if volumeGepasseerd >= volumeVullen + extra:
        return True



print(hoekV(waterDebiet, afstandBeker))