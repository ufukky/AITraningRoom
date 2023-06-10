from SimulationPackage import SimulationPackage

from UDP import UDP
from threading import Thread
import json
import time

class SimulaitonManager:
    def __init__(self,IP = "127.0.0.1",PORT_RECIVE = 8080,PORT_SEND = 8081):
        self.active = True
        self.ip = IP
        self.port_recive = PORT_RECIVE
        self.port_send = PORT_SEND
        
        self.udp = UDP(self.ip,self.port_recive,self.port_send)
        self.mainThread = Thread(target=self.mainThreadFnc,daemon=True)
        self.mainThread.start()

        self.subscriptions = []
        
    def mainThreadFnc(self):
        while self.active:
            self.IncomingPackageController()

    def Subscribe(self,topic,call):
        _sub = Subscribtion(topic,call)
        if not self.subscriptions.__contains__(_sub):
            self.subscriptions.append(_sub)
        return _sub

    def IncomingPackageController(self):
        _,package = self.udp.GetNewPackage()
        if _:
            _simPackage = SimulationPackage(package)
            for i in range(len(self.subscriptions)):
                if _simPackage.topic == self.subscriptions[i].topic:
                    self.subscriptions[i].call(_simPackage.payloadJson)
    
    def Send(self,data,subscription):
        newPackage = {"topic":subscription.topic,"payloadJson":data,"signature":f"{time.time() * 10}"}
        self.udp.SendString(json.dumps(newPackage))  

    def Close(self):     
        self.udp.Close()
        self.active = False
        self.mainThread.join()

    def PrintSubscriptions(self):
        for i in range(len(self.subscriptions)):
            print(self.subscriptions[i].topic)
        
class Subscribtion:
    def __init__(self,Topic,Call):
        self.topic = Topic
        self.call = Call

"""
public class SimulationManager : MonoBehaviour
{
    [SerializeField] int PORT_RECIVE = 8080;
    [SerializeField] int PORT_SEND = 8080;
    [SerializeField] string IP = "127.0.0.1";

    List<Subscribtion> subscribtions = new List<Subscribtion>();
    List<KeyValuePair<string,UnityAction<string>>> listeners = new List<KeyValuePair<string, UnityAction<string>>>();

    PackageReciveEvent packageReciveEvent;
    public SimulationManagerState state = SimulationManagerState.None;

    UDPReceive _UDPReceive;
    UDPSend _UDPSend;
    void Awake()
    {
        _UDPReceive = new UDPReceive(PORT_RECIVE);
        _UDPReceive.init();
        _UDPSend = new UDPSend(PORT_SEND,IP);
        _UDPSend.init();
        state = SimulationManagerState.Ready;
    }

    public void SubscribeToRecive(string Topic, UnityAction<string> Call) //implement subscribtion call
    {
        Subscribtion newSubscription = new Subscribtion(Topic, Call);   
        if(!subscribtions.Contains(newSubscription))
            subscribtions.Add(newSubscription);
    }

    void Update()
    {
        IncomingPackageController();
    }

    void IncomingPackageController()
    {
        if(_UDPReceive.GetNewPackage(out string outPackage))
        {
            SimulationPackage simulationPackage = new SimulationPackage(outPackage);
            if(simulationPackage.state == SimulationPackageState.Invalid)
            {
                Debug.Log("INVALID PACKAGE");
                return;
            }
            
            foreach (Subscribtion subscribtion in subscribtions)
            {
                if(simulationPackage.json.topic == subscribtion.topic)
                {
                    subscribtion.call.Invoke(simulationPackage.json.payloadJson);
                }                  
            }
        }
    }
}

[System.Serializable]
public class PackageReciveEvent : UnityEvent<string>
{

}

public enum SimulationManagerState
{
    None,Ready
}

public class Subscribtion
{
    public string topic {get;set;}
    public UnityAction<string> call {get;set;}
    public Subscribtion(string topic, UnityAction<string> call) { this.call = call; this.topic = topic; }
    public Subscribtion(Subscribtion subscribtion){this.topic = subscribtion.topic;this.call = subscribtion.call; }
}
"""