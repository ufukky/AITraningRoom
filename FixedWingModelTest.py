import time
import random
import numpy as np
from FixedWing import FixedWing
from SimulationManager import SimulaitonManager
from sklearn.neural_network import MLPRegressor
import os
from TrainingCore import TrainingCore

import cProfile, pstats, io
from pstats import SortKey

os.system("cls")
sim = SimulaitonManager(IP="127.0.0.1",PORT_RECIVE=8081,PORT_SEND=8080)
nn = TrainingCore.load_model_latest()

def mainLogic():
    while True:
        fixedWing.getAttitude()
        fixedWing.getTargetSpecs()
        '''
        inputNN = np.asarray([[fixedWing._targetSpecs[0],fixedWing._targetSpecs[1],fixedWing._targetSpecs[2],
                              fixedWing.attitude[0],fixedWing.attitude[1],fixedWing.attitude[2]]])
        pred = nn.predict(inputNN)

        fixedWing.control=pred[0].tolist()
        '''
        fixedWing.control = [0,0]
        fixedWing.iterate()
        
        
def payloadHandle(payload):
    if fixedWing.isWaitingForCommand:
        fixedWing.commandAnswerReciver(payload)
        return
    else:
        print("Rouge Payload:"+payload)

fixedWing = FixedWing(sim,mainLogic,payloadHandle)

input("Press Enter to exit")
sim.Close()
fixedWing.Close()