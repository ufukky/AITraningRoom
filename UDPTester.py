import socket
import time
import os
from SimulationManager import SimulaitonManager
from UDP import UDP
from threading import Thread
import json


udp = UDP("127.0.0.1",8080,8080)

def reciveThrdFnc():
    _,outPackage = udp.GetNewPackage()
    if _:
        print(f"outPackage: {outPackage}")
    pass

reciveThrd = Thread(target=reciveThrdFnc,daemon=True)
reciveThrd.start()

t = time.time()
for i in range(100):
    udp.SendString(f"{i}")


