using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

public class FixedWingSimulationManager : MonoBehaviour
{
    [SerializeField] SimulationManager simulationManager;
    [SerializeField] static string topic = "FixedwingMain";
    [SerializeField] PlaneController planeController;
    [SerializeField] TargetCameraController targetCameraController;
    Subscribtion sub;
    // Start is called before the first frame update
    void Start()
    {
        if(simulationManager.state == SimulationManagerState.None)
            Debug.Log("SIM NOT READY");
        
        UnityEvent test = new UnityEvent();        
        sub = simulationManager.Subscribe(topic, PackageRecived);
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
            SendPayload("command", "testCommand");
        //Debug.Log(planeController.GetAttitudeAngles()[0].Value);
    }   
    public void PackageRecived(string packageJSON_STR)
    {
        FixedWingPayload fwPayloads = JsonUtility.FromJson<FixedWingPayload>(packageJSON_STR);

        if (fwPayloads == null)
            return;
        if (fwPayloads.type == "command")
            commandManager(fwPayloads);
        else
            Debug.Log("PackageRecived:" + fwPayloads.signature);
    }

    public void SendPayload(string type = "", string command = "", string info = "", float[] parameters = null)
    {
        FixedWingPayload payload = new FixedWingPayload() {type=type,command=command,parameters=parameters,info=info,signature = Mathf.RoundToInt(Time.timeSinceLevelLoad * 100) };
        simulationManager.Send(JsonUtility.ToJson(payload),sub);
    }

    void commandManager(FixedWingPayload payload) 
    {
        if(payload.command == "getAttitude")
        {
            SendPayload("command", "getAttitude", "id:todo", new float[] { planeController.angles.x, planeController.angles.y,planeController.angles.z });
        }

        if (payload.command == "iterate")
        {
            planeController.Iterate(Time.deltaTime);
        }


        if (payload.command == "getTargetSpecs")
        {
            SendPayload("command", "getTargetSpecs", "id:todo", new float[] { targetCameraController.posX, targetCameraController.posY,Vector3.Distance(transform.position,targetCameraController.transform.position) });
        }

        if (payload.command == "setControl")
        {

            planeController.controlInput = new Vector3(payload.parameters[0], payload.parameters[1], 0f);

        }
    }
}

[System.Serializable]
public class FixedWingPayload
{
    public string type;
    public string command;
    public float[]  parameters;
    public string info;
    public int signature;
}


