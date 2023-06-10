using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(TrainingRecorder))]
public class TrainingController : MonoBehaviour
{
    [SerializeField] bool active = true;
    [SerializeField] float trainingBatchLenght = 5f;
    [SerializeField] int traingnBatchCount = 10;
    [SerializeField] float sampleRate = 10f;

    [SerializeField] float maxDistance = 100f;
    [SerializeField] private Vector3 sensitivity = new Vector3(0.2f,0.2f,0.1f);
    [SerializeField] PlaneController planeController;
    [SerializeField] Transform target;
    [SerializeField] Vector3 _controlInput;
    [SerializeField] string path;
    [SerializeField] string filePrefix = "data_";
    [SerializeField] TargetCameraController targetCameraController;

    [SerializeField] PlaneController plane;
    [SerializeField] List<string> labels;
    
    int batchCount = 0;
    float remainingBatchTime = 0f,remainingSampleTime = 0f;
    TrainingRecorder trainingRecorder;

    // Update is called once per frame

    void Start()
    {
        remainingBatchTime = trainingBatchLenght;
        remainingSampleTime = 1f/sampleRate;
        batchCount = 0;
        planeController.controlWith2DInputs = true;
        trainingRecorder = GetComponent<TrainingRecorder>();
    }
    void Update()
    {
        if(planeController == null || target == null)
            return;
        
        Vector3 mousePos = Input.mousePosition;
        Vector3 centerNormalizedMousePos_Pix = mousePos - new Vector3(Screen.width/2,Screen.height/2);
        Vector3 adjustedControl = new Vector3(centerNormalizedMousePos_Pix.x/Screen.width * sensitivity.x,centerNormalizedMousePos_Pix.y/Screen.height * sensitivity.y,0f);
        _controlInput = new Vector3(adjustedControl.x, adjustedControl.y,Input.GetAxis("Horizontal")*sensitivity.z);

        planeController.controlInput = active ? _controlInput : Vector3.zero;
        planeController.Iterate(Time.deltaTime);


        
            if (remainingSampleTime<=0f)
            {
                trainingRecorder.addRecord(new TrainingData(targetCameraController.posX,targetCameraController.posY,
                                                            Vector3.Distance(target.position,targetCameraController.transform.position)/maxDistance,
                                                            _controlInput.x, _controlInput.y, planeController.angles.x, planeController.angles.y, planeController.angles.z));
                remainingSampleTime = 1f/sampleRate;
            }
        
            if (remainingBatchTime<=0f && batchCount<traingnBatchCount)
            {
                string filename = filePrefix + DateTime.Now.ToString("hh.mm.ss.fff") + ".cvs";
                trainingRecorder.saveRecord(path,filename, labels);  
                trainingRecorder.clearRecords();
                remainingBatchTime = trainingBatchLenght;
                batchCount++;
                //todo teleport agent to random screen position
                Debug.Log("Saved:"+filename+" "+batchCount);
            }

        remainingBatchTime -= Time.deltaTime;
        remainingSampleTime -= Time.deltaTime;
    }
}
