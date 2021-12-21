import logging
import time
import math
from types import LambdaType
import numpy as np
from geopy.geocoders import Nominatim
import random


tm = time.localtime()
t = tm.tm_hour          #현재시각
T_0 = 23                #오후 11시
Te = 25                 #새벽 1시
T = abs(Te - T_0)       #범죄위험 시간대
Tc = 0.5*(T_0 + Te)
A = 3000                #목표지역구획 넓이

R = random()
P = 


geolocoder = Nominatim(user_agent= "South Korea")
def geocoding(address):                               #대상지역 위도 경도 받아오는 함수
    geo = geolocoder.geocode(address)
    global Lat
    Lat = geo.latitude
    global Long
    Long = geo.longitude


subject_location = geocoding("쌍용역")
subject_lat = Lat
subject_long = Long
c = np.array[subject_lat, subject_long]       #중앙 좌표



F = R * P * (1/4*T*abs(A)*(3.141592)**2) * np.exp(-((t-Tc)**2)/2*T**2) * np.exp(-(sum(x-c)**2)/2*A**2)


if F > 0 and R > 0 and abs(t-Tc) < 0 and abs(x-c) < 0:
    print("warning!!!! case 1")
elif F > 0 and R > 0 and abs(t-Tc) < 0 and abs(x-c) > 0:
    print("case 2")
elif F > 0 and R > 0 and abs(t-Tc) > 0 and abs(x-c) < 0:
    print("case 3")
elif F > 0 and R > 0 and abs(t-Tc) > 0 and abs(x-c) > 0:
    print("case 4")

elif F > 0 and R < 0 and abs(t-Tc) < 0 and abs(x-c) < 0:
    print("case 5")
elif F > 0 and R < 0 and abs(t-Tc) < 0 and abs(x-c) > 0:
    print("case 6")
elif F > 0 and R < 0 and abs(t-Tc) > 0 and abs(x-c) < 0:
    print("case 7")
elif F > 0 and R < 0 and abs(t-Tc) > 0 and abs(x-c) > 0:
    print("case 8")

elif F < 0 and R > 0 and abs(t-Tc) < 0 and abs(x-c) < 0:
    print("case 9")
elif F < 0 and R > 0 and abs(t-Tc) < 0 and abs(x-c) > 0:
    print("case 10")
elif F < 0 and R > 0 and abs(t-Tc) > 0 and abs(x-c) < 0:
    print("case 11")
elif F < 0 and R > 0 and abs(t-Tc) > 0 and abs(x-c) > 0:
    print("case 12")

elif F < 0 and R < 0 and abs(t-Tc) < 0 and abs(x-c) < 0:
    print("case 13")
elif F < 0 and R < 0 and abs(t-Tc) < 0 and abs(x-c) > 0:
    print("case 14")
elif F < 0 and R < 0 and abs(t-Tc) > 0 and abs(x-c) < 0:
    print("case 15")
elif F < 0 and R < 0 and abs(t-Tc) > 0 and abs(x-c) > 0:
    print("case 16")








