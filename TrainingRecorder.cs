using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class TrainingRecorder : MonoBehaviour
{
    List<TrainingData> trainingDatas = new List<TrainingData>();

    // Start is called before the first frame update
    void Start()
    {
        
    }

    public void clearRecords(){
        trainingDatas = new List<TrainingData>();
    }
    public void addRecord(TrainingData data)
    {
        trainingDatas.Add(data);
    }

    public int saveRecord(string folderPath, string fileName,List<string> labels)
    {
        string fullPath = folderPath + fileName;
        if (!Directory.Exists(folderPath))
        {
            Directory.CreateDirectory(folderPath);
            Debug.Log(fullPath + " created.");
        }
        string lablesLine = "";
        foreach (string label in labels)
            lablesLine += label + ",";
        lablesLine = lablesLine.Substring(0,lablesLine.Length - 1);
        Debug.Log(lablesLine);
        File.WriteAllText(fullPath, lablesLine+"\n");

        // An array of strings
        string[] strArr = new string[trainingDatas.Count];
        foreach (TrainingData data in trainingDatas)
        {
            string line =  data.posX + "," + data.posY + "," + data.distance +","+data.roll+","+data.pitch+","+data.yaw + "," + data.rollCnt + "," + data.pitchCnt;
            strArr[trainingDatas.IndexOf(data)] = line;
        }
        File.AppendAllLines(fullPath, strArr);
        return trainingDatas.Count;
    }
}
