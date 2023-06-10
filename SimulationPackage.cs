using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class SimulationPackage
{
    public string jsonString;
    public SimulationPackageJSON json;
    public SimulationPackageState state = SimulationPackageState.None;

    public SimulationPackage(string jsonString)
    {
        this.jsonString = jsonString;
        this.json = JsonUtility.FromJson<SimulationPackageJSON>(jsonString);
        if (this.json == null)
            state = SimulationPackageState.Invalid;
        else
            state = SimulationPackageState.Valid;
    }
}

public enum SimulationPackageState
{
    None,Valid,Invalid
}

[System.Serializable]
public class SimulationPackageJSON
{
    public string topic;
    public string payloadJson;
    public int signature;
}