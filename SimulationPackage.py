import json

class SimulationPackage:
    def __init__(self,jsonString = "{}"):
        self.jsonString = jsonString
        self.simulationPackageJSON = json.loads(jsonString)
        if(self.simulationPackageJSON == None):
            self.state = "Invalid"
        else:
            self.state = "Valid"
            self.topic = self.simulationPackageJSON["topic"]
            self.payloadJson = self.simulationPackageJSON["payloadJson"]
            self.signature = self.simulationPackageJSON["signature"]