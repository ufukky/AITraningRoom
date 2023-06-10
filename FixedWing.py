import cProfile
import io
from pstats import SortKey
import pstats
import socket
import time
import os
from FixedWingPackage import CratePayload
from SimulationManager import SimulaitonManager
from UDP import UDP
from threading import Thread
import json

class FixedWing:
    def __init__(self,simulationManager:SimulaitonManager,mainLogic,payloadHandleLogic):
        self.active = True
        self.simulationManager = simulationManager
        self.mainSubs = self.simulationManager.Subscribe("FixedwingMain",self.FixedWingMainSubscriber)

        self.mainLogic = mainLogic
        if(self.mainLogic == None):
            self.mainLogic = self.defaulMainFuncToBeImplemented
        self.mainLogicThread = Thread(target=self.mainLogic,daemon=True)
        self.mainLogicThread.start()
        self.payloadHandleLogic = payloadHandleLogic

        self.waitForCommand = {"state":False,"command":""}

        self._attitude = [0,0,0,0,0,0]
        self._control = [0,0,0]

        self.sendPrf = cProfile.Profile()

    def atitude_get(self):
        return self._attitude
    def atitude_set(self,value):
        self._attitude = value
        self.SendPayload(type="command",command="setAttitude",
                         info="todo:id",parameters=[self._attitude])
        
    attitude = property(atitude_get,atitude_set)

    def control_get(self):
        return self._control
    def control_set(self,value):
        self._control = value
        self.SendPayload(type="command",command="setControl",
                         info="todo:id",parameters=self._control)
        
    control = property(control_get,control_set)

    def getTargetSpecs(self):
        self.SendPayload(type="command",command="getTargetSpecs",waitForAnswer=True)
    def getAttitude(self):
        self.SendPayload(type="command",command="getAttitude",waitForAnswer=True)

    def iterate(self):
        self.SendPayload(type="command",command="iterate")

    def defaulMainFuncToBeImplemented(self):
        while self.active:
            print("Implement")

    def FixedWingMainSubscriber(self,payload):
        self.payloadHandleLogic(payload)

    def isWaitingForCommand(self):
        if self.waitForCommand["state"]:
            return True
        else:
            return False
    isWaitingForCommand = property(isWaitingForCommand)

    
    def SendPayload(self,type = "",command="",info="",parameters = None,waitForAnswer = False):
        self.sendPrf.enable()
        if waitForAnswer:
            self.waitForCommand = {"state":True,"command":command}
        payload = CratePayload(type=type,command=command,info=info,parameters=parameters)
        self.simulationManager.Send(json.dumps(payload),self.mainSubs)
        t = time.time()
        if waitForAnswer:
            while self.isWaitingForCommand:
               pass
        
        self.sendPrf.disable()

        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(self.sendPrf, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        

    def Close(self):
        self.active = False
        self.mainLogicThread.join()

    def commandAnswerReciver(self,commandPayload):
        commandPayload = json.loads(commandPayload)
        if not self.waitForCommand["state"]:
            return
        if self.waitForCommand["command"] in commandPayload["command"]:
            if commandPayload["command"] == "getAttitude":
                self._attitude = commandPayload["parameters"]
            if commandPayload["command"] == "getTargetSpecs":
                self._targetSpecs = commandPayload["parameters"]
            self.waitForCommand = {"state":False,"command":""}
            
        


