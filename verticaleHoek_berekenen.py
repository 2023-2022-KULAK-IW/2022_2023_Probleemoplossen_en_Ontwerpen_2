import numpy as np
from scipy.optimize import fsolve


"""
input:
"""
waterDebiet = 240 #l/h (240 is standaardwaarde), komt van waterflowsensor
afstandBeker = 10.44 #komt van webcam
volumeGepasseerd = 0 #ml, komt van waterflowsensor

"""
niet veranderlijk:
de meeste zijn wel nog te bepalen
"""
straal = 0.0015
hoogteDoos = 0.5
lengteArm = 0.32
l0 = 0.05  #lengte tussen aangrijpingspunt arm en camera

hoogteBeker = 0
volumeVullen = 0.0005 #m³
extra = 0.0001 #extar volume, zodat we niet te weinig hebben

"""
berekeningen:
"""
snelheid = (waterDebiet*2.78*10**(-7))/(np.pi*(straal**2))

def func(a):
    return [-afstandBeker + np.cos(a[0])*snelheid*a[1] + np.cos(a[0])*lengteArm - l0, -hoogteBeker + hoogteDoos + np.sin(a[0]) * lengteArm + np.sin(a[0])*snelheid*a[1] -1/2*9.81*(a[1]**2)]
opl = fsolve(func, [np.pi/2, 100], )
opl[0] = opl[0]*180/np.pi

"""
oplossing:
"""
oplossing = {'hoek': opl[0]}
print(oplossing)