using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;


public class TrainingData
{
    public float posX,posY,distance,rollCnt,pitchCnt, roll,pitch,yaw;
    public TrainingData(float posX, float posY, float distance, float rollCnt, float pitchCnt,float roll,float pitch,float yaw)
    {
        this.posX = posX;
        this.posY = posY;
        this.distance = distance;
        this.rollCnt = rollCnt;
        this.pitchCnt = pitchCnt;
        this.roll = roll;
        this.pitch = pitch;
        this.yaw = yaw;
    }
    
}