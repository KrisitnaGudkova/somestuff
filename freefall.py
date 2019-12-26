import math
import numpy as np
import holoviews as hv
from holoviews import opts
hv.extension('bokeh')

m = 1.0
k = 0.15
g = 9.8
angle = [0, math.pi/10, math.pi/5, 3*math.pi/10, 2*math.pi/5, math.pi/2]
speed = [0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
time = [0.01*i for i in range(50)]

def curve1(angle, speed):
    xvals = [(m*speed*math.cos(angle)/k)*(1 - math.exp(-k*t/m)) for t in time]
    yvals = [(m*speed*math.sin(angle)/k + g*m*m/(k*k))*(1 - math.exp(-k*t/m)) - g*m*t/k for t in time]
    return hv.Curve((xvals, yvals)).redim.range(yvals=(0, None))

def curve2(angle, speed):
    xvals = [(m/k)*math.log(m/(m-k*speed*math.cos(angle)*t)) for t in time]
    Vy = np.zeroes(50)
    yvals = np.zeroes(50)
    Vy[0] = speed*math.sin(angle)
    yvals[0] = 0
    for i in range(1, 50):
        Vy[i] = ((-m*g - k*Vy[i-1]*Vy[i-1])*0.01)/m + Vy[i-1]
        yvals[i] = Vy[i-1]*0.01 + yvals[i-1]
    return hv.Curve((xvals, yvals)).redim.range(yvals=(0, None))

curve_dict_1 = {(p,f):curve1(p,f) for p in angle for f in speed}
curve_dict_2 = {(p,f):curve2(p,f) for p in angle for f in speed}
hmap1 = hv.HoloMap(curve_dict_1, kdims=['angle', 'speed'])
hmap2 = hv.HoloMap(curve_dict_2, kdims=['angle', 'speed'])
hmap1 + hmap2
