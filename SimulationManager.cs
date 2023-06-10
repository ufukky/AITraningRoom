using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.Events;

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

    public void SendString(string data)
    {
        _UDPSend.sendString(data);
    }

    public Subscribtion Subscribe(string Topic, UnityAction<string> Call) //implement subscribtion call
    {
        Subscribtion newSubscription = new Subscribtion(Topic, Call);   
        if(!subscribtions.Contains(newSubscription))
            subscribtions.Add(newSubscription);
        return newSubscription;
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

    public void Send(string data,Subscribtion subscribtion) 
    {
        SimulationPackageJSON jsonPackage = new SimulationPackageJSON();
        jsonPackage.topic = subscribtion.topic;
        jsonPackage.payloadJson = data;
        jsonPackage.signature = (int)Time.time * 100;
        _UDPSend.sendString(JsonUtility.ToJson(jsonPackage));
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
