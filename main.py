import time
from FixedWing import FixedWing
import random
from SimulationManager import SimulaitonManager
import os


os.system("cls")
sim = SimulaitonManager(IP="127.0.0.1",PORT_RECIVE=8081,PORT_SEND=8080)
fixedWing = None
def mainLogic():
    while True:
        if fixedWing.waitForCommand["state"]:
            continue
        fixedWing.attitude = [random.randint(-100,100),0,0,0,0,0]
        fixedWing.control = [0.1,0.01]
        fixedWing.iterate()
        fixedWing.SendPayload(type="command",command="testCommand",info="todo:id",waitForAnswer=True)
        time.sleep(0.1)

def payloadHandle(payload):
    if fixedWing.isWaitingForCommand():
        fixedWing.commandAnswerReciver(payload)
        return
    else:
        print("Rouge Payload:"+payload)


fixedWing = FixedWing(sim,mainLogic,payloadHandle)

input("Press Enter to exit")
sim.Close()
fixedWing.Close()